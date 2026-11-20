# Adaptive Security

A portable AI skill for backup-first security review, recurring checks and
evidence-driven improvements on authorized websites and applications.

It guides an assistant through code, dependencies and malicious-package
advisories, secrets, identity and authorization, APIs, uploads, infrastructure,
privacy, integrations, AI trust boundaries, recovery and other applicable risks.
The coverage catalogue spans 29 domains. It requires verified backups before
remediation, verification after changes, and redacted Git records for every run.

## What this package provides

Markdown instructions and templates for an assistant with appropriate tools.
It is not a standalone scanner, scheduler, hosted service or autonomous daemon.
Installing it does not schedule jobs, grant access, execute tests or fix a site.
The assistant must configure and verify those capabilities in the target project.

Default planning intervals: daily checks; weekly release and coverage review;
monthly deeper testing; quarterly infrastructure and recovery review; annual
independent-assessment review. Owners configure timezone, scope and execution.

Change review runs Anthropic's `/security-review`: the Claude Code built-in where
it is available, otherwise a verbatim, MIT-licensed copy vendored in
[references/upstream/](references/upstream/). Precedence rules, attribution and
deliberate scope adaptations are documented in
[SECURITY-REVIEW.md](references/SECURITY-REVIEW.md). No Anthropic account or paid
API is required for the vendored path. This project is not affiliated with or
endorsed by Anthropic, OpenAI or the referenced standards organizations.

## Install in Claude Code

This repository is also a Claude Code plugin marketplace. Install it once and
updates arrive as new commits land on `main`:

    /plugin install adaptive-security --marketplace mbtsmo/adaptive-security

On Claude Code before 2.1.275, run `/plugin marketplace add mbtsmo/adaptive-security`
and then `/plugin install adaptive-security@adaptive-security`. Third-party
marketplaces do not auto-update by default: open `/plugin`, choose
**Marketplaces → adaptive-security**, and enable auto-update. The skill is then
available as `/adaptive-security:adaptive-security` in every project.

Cloud sessions on claude.ai/code do not load your local plugins. Add these
lines to the cloud environment's **Setup script** so new sessions install the
current version. Each line is safe to rerun, and the updates matter when the
environment is reused:

    claude plugin marketplace add mbtsmo/adaptive-security
    claude plugin marketplace update adaptive-security
    claude plugin install adaptive-security@adaptive-security --scope user
    claude plugin update adaptive-security@adaptive-security --scope user

## Use it in other assistants

1. Download this repository using GitHub's **Code → Download ZIP**, or clone it.
2. Place the folder containing `SKILL.md` and `references/` in your assistant's
   supported skill location. See [portability guidance](references/PORTABILITY.md).
3. For assistants without skills, provide `SKILL.md` and the reference documents
   as project knowledge, subject to their context and file capabilities.
4. Start with an authorized repository and give the assistant this instruction:

> Use adaptive-security for this project. Read existing policies and schedules,
> establish scope, and run available checks. Back up before remediation, verify
> changes, and record redacted results in Git. Keep blocked checks visible and
> preserve my existing production release boundaries.

Before unattended use, evaluate the acceptance scenarios in PORTABILITY.md,
RUNNER-ASSURANCE.md and SECURITY-REVIEW.md in an isolated disposable project.
Behaviour varies by model and host; this package has not been validated across
all assistants. Missing tools or access must be reported, never treated as passes.

## Keeping up with Anthropic's /security-review

Anthropic can change `/security-review` in its public repository or in the copy
bundled with Claude Code, and the two already differ.
[upstream-security-review.yml](.github/workflows/upstream-security-review.yml)
runs [scripts/upstream_sync.py](scripts/upstream_sync.py) daily and proposes
any change as the `upstream-sync/security-review` pull request, for review under
*Upstream tracking* in SECURITY-REVIEW.md. Failures open an issue. Claude Code
is proprietary, so only a hash of its bundled prompt is stored here.

To let the workflow open pull requests, enable **Settings → Actions → General →
Workflow permissions → Allow GitHub Actions to create and approve pull requests**
(off by default for repositories in a personal account; turn it off again to
undo). Without it, the workflow opens an issue that links the proposed branch.
GitHub disables scheduled workflows in public repositories after 60 days without
repository activity; re-enable it from the Actions tab. To check by hand, run
`python3 scripts/upstream_sync.py check`.

## Sharing and data handling

The distributed package contains guidance plus its upstream-tracking script and
workflows: no site source, environment files, credentials, customer data, backups
or private findings. Store project
configuration, raw evidence and backups separately. Review your own changes before
redistribution; keep sensitive information out of public issues and commits.

Active tests belong in isolated authorized environments. Backup-first remediation
does not override production release approval. No workflow can guarantee finding
every vulnerability or undisclosed zero-day, or replace an independent assessment.

## License

Original package content is provided under the [MIT License](LICENSE).
Anthropic's `security-review.md` is included verbatim under its own
[MIT License](references/upstream/claude-code-security-review/LICENSE)
(Copyright (c) 2025 Anthropic). Other linked third-party projects retain their
own licenses; their software and full skill prompts are not bundled here.
