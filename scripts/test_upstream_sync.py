"""Offline tests for upstream_sync.py. Run: python3 -m unittest discover -s scripts"""

import hashlib
import json
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import upstream_sync as u

BODY = f"{u.START} of the changes.\n\nDIFF:\n!`git diff origin/HEAD...`\n\n{u.END}"


def sha(text):
    return hashlib.sha256(text.encode() if isinstance(text, str) else text).hexdigest()


class NormalizeAndExtract(unittest.TestCase):
    def test_js_template_escaping_and_placeholders_normalize_to_published_text(self):
        bundled = f"{u.START}\n\\`git status\\` ${{_1o}}  \r\n{u.END}"
        self.assertEqual(u.normalize_body(bundled), f"{u.START}\n`git status` ${{}}\n{u.END}")

    def test_single_body_found_in_binary_noise(self):
        data = b"\x00\xff" + BODY.encode() + b"\x00junk"
        self.assertEqual(u.extract_single_body(data, "t"), u.normalize_body(BODY))

    def test_identical_copies_count_once(self):
        self.assertEqual(len(u.extract_bodies((BODY + "\0" + BODY).encode())), 1)

    def test_missing_prompt_is_an_error_not_unchanged(self):
        with self.assertRaisesRegex(u.SyncError, "not found"):
            u.extract_single_body(b"no prompt here", "t")

    def test_two_different_prompts_are_ambiguous(self):
        other = BODY.replace("origin/HEAD...", "--merge-base origin/HEAD")
        with self.assertRaisesRegex(u.SyncError, "different"):
            u.extract_single_body((BODY + "\0" + other).encode(), "t")

    def test_start_without_end_is_ignored(self):
        self.assertEqual(u.extract_bodies(u.START.encode() + b" truncated"), set())

    def test_undecodable_copy_is_skipped(self):
        broken = BODY.encode().replace(b"DIFF", b"\xff\xfe")
        self.assertEqual(u.extract_bodies(broken + b"\0" + BODY.encode()), {u.normalize_body(BODY)})


class LockHandling(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp)
        vend = self.tmp / "vend"
        vend.mkdir()
        (vend / "security-review.md").write_text(BODY)
        (vend / "LICENSE").write_text("MIT License\nPermission is hereby granted, free of charge\n")
        self.lock = {"schema": 1, "sources": {
            "public": {
                "repository": "example/upstream", "path": "cmd.md", "license_path": "LICENSE",
                "commit": "a" * 40, "sha256": sha(BODY),
                "license_sha256": sha((vend / "LICENSE").read_bytes()),
                "vendored_path": "vend/security-review.md", "vendored_license_path": "vend/LICENSE",
                "retrieved": "2026-01-01",
            },
            "builtin": {"npm_package": "pkg", "version": "1.0.0", "body_sha256": sha(u.normalize_body(BODY)),
                        "matches_public": True, "retrieved": "2026-01-01"},
        }}
        lock_path = self.tmp / "sources.json"
        lock_path.write_text(json.dumps(self.lock))
        for name, value in (("ROOT", self.tmp), ("LOCK_PATH", lock_path)):
            patcher = mock.patch.object(u, name, value)
            patcher.start()
            self.addCleanup(patcher.stop)

    def test_verify_detects_edited_vendored_copy(self):
        u.verify(self.lock)
        (self.tmp / "vend" / "security-review.md").write_text(BODY + "\nlocal edit\n")
        with self.assertRaisesRegex(u.SyncError, "verbatim"):
            u.verify(self.lock)

    def test_public_update_is_applied_verbatim(self):
        new_body = BODY.replace("of the changes", "of this branch")
        fetched = {"commit": "b" * 40, "content": new_body.encode(),
                   "licence": (self.tmp / "vend" / "LICENSE").read_bytes()}
        notes = []
        with mock.patch.object(u, "fetch_public", return_value=fetched):
            self.assertTrue(u.check_public(self.lock["sources"]["public"], True, notes))
        self.assertEqual((self.tmp / "vend" / "security-review.md").read_text(), new_body)
        self.assertEqual(self.lock["sources"]["public"]["commit"], "b" * 40)
        self.assertIn("```diff", "\n".join(notes))
        u.verify(self.lock)

    def test_unchanged_public_source_reports_no_change(self):
        fetched = {"commit": "a" * 40, "content": BODY.encode(),
                   "licence": (self.tmp / "vend" / "LICENSE").read_bytes()}
        with mock.patch.object(u, "fetch_public", return_value=fetched):
            self.assertFalse(u.check_public(self.lock["sources"]["public"], True, []))

    def test_builtin_change_records_only_a_hash(self):
        secret_wording = BODY.replace("of the changes", "PROPRIETARY WORDING")
        notes = []
        with mock.patch.object(u, "fetch_builtin_binary", return_value=("2.0.0", secret_wording.encode())):
            self.assertTrue(u.check_builtin(self.lock["sources"]["builtin"], self.lock["sources"]["public"],
                                            True, notes))
        builtin = self.lock["sources"]["builtin"]
        self.assertEqual(builtin["version"], "2.0.0")
        self.assertEqual(builtin["body_sha256"], sha(u.normalize_body(secret_wording)))
        self.assertFalse(builtin["matches_public"])
        self.assertNotIn("PROPRIETARY", json.dumps(self.lock) + "\n".join(notes))

    def test_show_diff_refused_in_github_actions(self):
        with mock.patch.dict(u.os.environ, {"GITHUB_ACTIONS": "true"}), \
                mock.patch.object(u, "fetch_builtin_binary", return_value=("1.0.0", BODY.encode())):
            with self.assertRaisesRegex(u.SyncError, "refused"):
                u.check_builtin(self.lock["sources"]["builtin"], self.lock["sources"]["public"],
                                False, [], show_diff=True)


if __name__ == "__main__":
    unittest.main()
