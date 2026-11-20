#!/usr/bin/env python3
"""Detect and stage updates to Anthropic's /security-review for adaptive-security.

Tracked sources are pinned in references/upstream/sources.json:

  public   The MIT-licensed security-review.md published in
           anthropics/claude-code-security-review. It is vendored verbatim with
           its licence; --apply rewrites the vendored copy and the lock.
  builtin  The /security-review prompt bundled in Claude Code. Claude Code is
           proprietary, so its text is never written to this repository or to a
           public log. Only the Claude Code version it was read from and a
           SHA-256 of its normalized body are recorded.

Downloaded code is never executed. Any fetch, integrity, parse or ambiguity
failure is an error (exit 1), never "unchanged".

Exit codes: 0 all checked sources match the lock; 2 at least one source changed
(with --apply the lock and vendored files were updated); 1 error.
"""

import argparse
import base64
import datetime
import difflib
import hashlib
import io
import json
import os
import re
import subprocess
import sys
import tarfile
import tempfile
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOCK_PATH = ROOT / "references" / "upstream" / "sources.json"

# The body of the command is hashed from START through END, inclusive.
START = "You are a senior security engineer conducting a focused security review"
END = "Your final reply must contain the markdown report and nothing else."
MAX_BODY_BYTES = 200_000
MAX_TARBALL_BYTES = 600 * 1024 * 1024
MIT_MARKERS = ("MIT License", "Permission is hereby granted, free of charge")
HTTP_TIMEOUT = 120


class SyncError(Exception):
    pass


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def today():
    return datetime.datetime.now(datetime.timezone.utc).date().isoformat()


def load_lock():
    with open(LOCK_PATH, encoding="utf-8") as f:
        lock = json.load(f)
    if lock.get("schema") != 1:
        raise SyncError(f"unsupported lock schema in {LOCK_PATH}")
    return lock


def save_lock(lock):
    text = json.dumps(lock, indent=2, ensure_ascii=False) + "\n"
    LOCK_PATH.write_text(text, encoding="utf-8")


def http_get(url, limit):
    req = urllib.request.Request(url, headers={"User-Agent": "adaptive-security-upstream-sync"})
    with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT) as resp:
        if resp.status != 200:
            raise SyncError(f"GET {url}: HTTP {resp.status}")
        buf = io.BytesIO()
        while True:
            chunk = resp.read(1024 * 1024)
            if not chunk:
                break
            buf.write(chunk)
            if buf.tell() > limit:
                raise SyncError(f"GET {url}: response exceeds {limit} bytes")
        return buf.getvalue()


def git(cwd, *args):
    result = subprocess.run(
        ["git", *args], cwd=cwd, capture_output=True, timeout=600,
        env={**os.environ, "GIT_TERMINAL_PROMPT": "0", "GIT_LFS_SKIP_SMUDGE": "1"},
    )
    if result.returncode != 0:
        raise SyncError(f"git {' '.join(args)}: {result.stderr.decode(errors='replace').strip()}")
    return result.stdout


# ---------------------------------------------------------------------------
# Prompt normalization and extraction


_PLACEHOLDER = re.compile(r"\$\{[A-Za-z_$][\w$]*\}")


def normalize_body(text):
    """Normalize a command body so bundled and published copies compare equal.

    Undoes JavaScript template-literal escaping, replaces minified ${name}
    interpolations (whose names change between builds) with ${}, and strips
    trailing whitespace from each line.
    """
    text = text.replace("\r\n", "\n").replace("\\`", "`").replace("\\$", "$")
    text = _PLACEHOLDER.sub("${}", text)
    return "\n".join(line.rstrip() for line in text.split("\n"))


def extract_bodies(data):
    """Return the distinct normalized command bodies found in a text or binary."""
    start, end = START.encode(), END.encode()
    bodies = set()
    pos = data.find(start)
    while pos >= 0:
        stop = data.find(end, pos)
        if 0 <= stop and stop - pos <= MAX_BODY_BYTES:
            try:
                bodies.add(normalize_body(data[pos:stop + len(end)].decode("utf-8")))
            except UnicodeDecodeError:
                pass
        pos = data.find(start, pos + 1)
    return bodies


def extract_single_body(data, label):
    bodies = extract_bodies(data)
    if not bodies:
        raise SyncError(
            f"{label}: /security-review prompt not found. It may have been renamed, "
            "rewritten or moved to a plugin; review manually before trusting the lock."
        )
    if len(bodies) > 1:
        raise SyncError(f"{label}: {len(bodies)} different /security-review prompts found; cannot choose one")
    return bodies.pop()


# ---------------------------------------------------------------------------
# Public MIT source


def fetch_public(src):
    with tempfile.TemporaryDirectory() as tmp:
        url = f"https://github.com/{src['repository']}.git"
        git(tmp, "clone", "--quiet", "--filter=blob:none", "--no-checkout", url, "repo")
        repo = os.path.join(tmp, "repo")
        commit = git(repo, "log", "-1", "--format=%H", "HEAD", "--", src["path"]).decode().strip()
        if not commit:
            raise SyncError(f"public: {src['path']} has no history in {src['repository']}")
        try:
            content = git(repo, "show", f"HEAD:{src['path']}")
        except SyncError:
            raise SyncError(f"public: {src['path']} is absent at upstream HEAD; it may have moved")
        licence = git(repo, "show", f"HEAD:{src['license_path']}")
    licence_text = licence.decode("utf-8", errors="replace")
    if not all(marker in licence_text for marker in MIT_MARKERS):
        raise SyncError("public: upstream licence is no longer recognisably MIT; review before vendoring")
    return {"commit": commit, "content": content, "licence": licence}


def check_public(src, apply, notes):
    new = fetch_public(src)
    vendored = ROOT / src["vendored_path"]
    vendored_licence = ROOT / src["vendored_license_path"]
    changed = (
        sha256_bytes(new["content"]) != src["sha256"]
        or sha256_bytes(new["licence"]) != src["license_sha256"]
    )
    if not changed:
        notes.append(f"- public: unchanged (file last changed in `{src['commit'][:12]}`).")
        return False

    old_text = vendored.read_text(encoding="utf-8") if vendored.exists() else ""
    diff = "".join(difflib.unified_diff(
        old_text.splitlines(keepends=True),
        new["content"].decode("utf-8", errors="replace").splitlines(keepends=True),
        fromfile=f"security-review.md@{src['commit'][:12]}",
        tofile=f"security-review.md@{new['commit'][:12]}",
    ))
    compare = f"https://github.com/{src['repository']}/compare/{src['commit']}...{new['commit']}"
    notes.append(f"- public: **changed** `{src['commit'][:12]}` → `{new['commit'][:12]}` ([compare]({compare})).")
    if sha256_bytes(new["licence"]) != src["license_sha256"]:
        notes.append("  - Upstream LICENSE text changed (still MIT); review the new notice.")
    if diff:
        notes.append("\n<details><summary>security-review.md diff</summary>\n\n```diff\n"
                     + diff[:40000] + ("\n… truncated\n" if len(diff) > 40000 else "")
                     + "```\n</details>\n")

    if apply:
        vendored.parent.mkdir(parents=True, exist_ok=True)
        vendored.write_bytes(new["content"])
        vendored_licence.write_bytes(new["licence"])
        src.update({
            "commit": new["commit"],
            "sha256": sha256_bytes(new["content"]),
            "license_sha256": sha256_bytes(new["licence"]),
            "retrieved": today(),
        })
    return True


# ---------------------------------------------------------------------------
# Built-in Claude Code source


def fetch_builtin_binary(src):
    pkg = src["npm_package"]
    meta = json.loads(http_get(f"https://registry.npmjs.org/{pkg}/latest", 5 * 1024 * 1024))
    version, tarball_url, integrity = meta["version"], meta["dist"]["tarball"], meta["dist"]["integrity"]
    algo, _, expected = integrity.partition("-")
    if algo != "sha512":
        raise SyncError(f"builtin: unsupported npm integrity algorithm {algo!r}")
    tarball = http_get(tarball_url, MAX_TARBALL_BYTES)
    if base64.b64encode(hashlib.sha512(tarball).digest()).decode() != expected:
        raise SyncError(f"builtin: {pkg}@{version} tarball failed npm integrity check")
    candidates = []
    with tarfile.open(fileobj=io.BytesIO(tarball), mode="r:gz") as tar:
        for member in tar.getmembers():
            if member.isfile() and member.size > 1024 * 1024:
                data = tar.extractfile(member).read()
                if START.encode() in data:
                    candidates.append(data)
    if not candidates:
        raise SyncError(f"builtin: no file in {pkg}@{version} contains the /security-review prompt")
    return version, b"".join(candidates)


def check_builtin(src, public_src, apply, notes, binary=None, show_diff=False):
    if binary:
        data = Path(binary).read_bytes()
        version = f"local file {Path(binary).name}"
    else:
        version, data = fetch_builtin_binary(src)
    body = extract_single_body(data, f"builtin ({version})")
    body_sha = sha256_bytes(body.encode("utf-8"))

    vendored = (ROOT / public_src["vendored_path"]).read_bytes()
    public_body = extract_single_body(vendored, "vendored public copy")
    matches_public = body == public_body

    if show_diff:
        if os.environ.get("GITHUB_ACTIONS") == "true":
            raise SyncError("--show-diff is refused in GitHub Actions: logs of a public repository are public")
        sys.stdout.writelines(difflib.unified_diff(
            public_body.splitlines(keepends=True), body.splitlines(keepends=True),
            fromfile="vendored public body", tofile=f"built-in body ({version})",
        ))
        print()

    if body_sha == src["body_sha256"]:
        if apply and not binary:
            src["matches_public"] = matches_public  # the public copy may have changed
        notes.append(f"- builtin: unchanged in Claude Code {version} "
                     f"({'matches' if matches_public else 'differs from'} the vendored public copy).")
        return False

    notes.append(
        f"- builtin: **changed** since Claude Code {src['version']}; now read from {version}. "
        f"It {'matches' if matches_public else 'differs from'} the vendored public copy. "
        "The text is not reproduced here (Claude Code is proprietary). Run "
        "`python3 scripts/upstream_sync.py check --source builtin --show-diff` locally to review it, "
        "then update `known_differences_from_public` in the lock."
    )
    if apply and not binary:
        src.update({
            "version": version,
            "body_sha256": body_sha,
            "matches_public": matches_public,
            "retrieved": today(),
        })
    return True


# ---------------------------------------------------------------------------
# Offline verification


def verify(lock):
    src = lock["sources"]["public"]
    for key, path_key in (("sha256", "vendored_path"), ("license_sha256", "vendored_license_path")):
        path = ROOT / src[path_key]
        if sha256_bytes(path.read_bytes()) != src[key]:
            raise SyncError(f"{src[path_key]} does not match its pinned SHA-256; vendored files must stay verbatim")
    extract_single_body((ROOT / src["vendored_path"]).read_bytes(), "vendored public copy")
    print("verify: vendored upstream files match sources.json")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    check = sub.add_parser("check", help="compare upstream sources with the lock")
    check.add_argument("--source", choices=("public", "builtin", "all"), default="all")
    check.add_argument("--apply", action="store_true", help="update the lock and vendored files on change")
    check.add_argument("--summary", help="write a Markdown summary to this file")
    check.add_argument("--binary", help="read the built-in prompt from this local Claude Code file instead of npm")
    check.add_argument("--show-diff", action="store_true",
                       help="print the built-in body diff to stdout (local use only; never in public CI)")
    sub.add_parser("verify", help="check vendored files against the lock (offline)")
    args = parser.parse_args(argv)

    try:
        lock = load_lock()
        if args.command == "verify":
            verify(lock)
            return 0
        sources = lock["sources"]
        notes, changed = [], False
        if args.source in ("public", "all"):
            changed |= check_public(sources["public"], args.apply, notes)
        if args.source in ("builtin", "all"):
            changed |= check_builtin(sources["builtin"], sources["public"], args.apply, notes,
                                     binary=args.binary, show_diff=args.show_diff)
        if changed and args.apply:
            save_lock(lock)
        summary = "\n".join(notes) + "\n"
        print(summary, end="")
        if args.summary:
            Path(args.summary).write_text(summary, encoding="utf-8")
        return 2 if changed else 0
    except (SyncError, OSError, ValueError, KeyError, tarfile.TarError, subprocess.SubprocessError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
