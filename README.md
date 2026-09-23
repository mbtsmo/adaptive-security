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

Public Anthropic security-review methods inform the code review workflow. Pinned
sources, attribution and deliberate scope adaptations are documented in
[SECURITY-REVIEW.md](references/SECURITY-REVIEW.md). No Anthropic account or paid
API is required for these instructions. This project is not affiliated with or
endorsed by Anthropic, OpenAI or the referenced standards organizations.

## Use it

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

## Sharing and data handling

The distributed package contains guidance only: no site source, environment
files, credentials, customer data, backups or private findings. Store project
configuration, raw evidence and backups separately. Review your own changes before
redistribution; keep sensitive information out of public issues and commits.

Active tests belong in isolated authorized environments. Backup-first remediation
does not override production release approval. No workflow can guarantee finding
every vulnerability or undisclosed zero-day, or replace an independent assessment.

## License

Original package content is provided under the [MIT License](LICENSE).
Linked third-party projects retain their own licenses; their software and full
skill prompts are not bundled here.
