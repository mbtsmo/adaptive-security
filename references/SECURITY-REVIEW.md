# Evidence-led code review and remediation

This model-neutral workflow incorporates methods reviewed in Anthropic's public
security projects. It supplements COVERAGE.md and the existing cadence. It does
not install their software, invoke Claude, or confer production release authority.

## Change review

At a security-sensitive change or weekly review, establish the actual comparison
base, candidate commit and dirty-file hashes. Never assume a remote default branch
represents the approved live release. Review the diff together with surrounding
callers, shared protections and configuration. Record newly introduced defects
separately from previously existing findings; retain both in the programme.

Compare changed behaviour with the application's established security controls.
Trace untrusted inputs across privilege boundaries to sensitive operations. Review
the assumptions that make protections effective, including indirect callers and
feature configuration. State what was inspected and what remains inaccessible.

## Triage before remediation

Normalize reports into stable finding IDs, preserving original source IDs and
missing fields. Resolve source paths within the authorized checkout. Missing code
or configuration means cannot verify, never false positive. Re-read the cited
implementation, trace actual callers, inspect upstream protections and consider
alternate routes around them. Cite concrete source locations and the inspected
revision. Keep source-supported conclusions distinct from executed reproductions.

Merge reports only when they share a root cause and one correction addresses both;
preserve their evidence and affected surfaces. Rank by attacker prerequisites,
reachability and impact, with confidence recorded separately. Record component
owner or owner unknown. Retain uncertain findings for follow-up instead of
discarding them to reduce noise.

Use a separate skeptical review pass. A single assistant rechecking its work is
not independent verification. Separate reviewers are optional only when permitted
by the host and task; this reference does not request delegation or paid services.

## Threat model

Bootstrap from architecture, source, known defects and earlier assessments when
owner input is unavailable. Record assumptions and distinguish code evidence from
owner statements. Describe enduring attacker goals and assets at risk separately
from individual bugs: a fixed defect does not retire its threat class. Connect each
threat to entry points, trust boundaries, impact, likelihood, current controls,
control evidence and remaining tests. Record deferred threats with rationale and
review dates. Revisit after architectural changes and on the deeper cadence.

Ask only for facts that cannot be inferred and block a dependent action. Continue
read-only modelling and other authorized checks while owner questions are pending.

## Patch review

Trace each verified defect to its root cause and search sibling call sites for
the same failure. Record variants covered or left open. Propose the smallest
effective correction and actively look for a bypass of that correction. Verify
both the denied attack path and legitimate behaviour with isolated regressions
where feasible. Keep candidate, applied, tested and deployed states separate.

A source-only review yields a candidate fix, not a verified repair. If execution
is unavailable, retain the candidate with its missing verification. Apply local
changes already authorized by the user only after a verified pre-change backup,
then follow project test and release gates. No new approval step is introduced
for already authorized work; production boundaries still apply.

## Coverage and cost decisions for this adaptation

Do not import blanket exclusions for dependencies, resource exhaustion, rate
limits, AI trust boundaries, logging, headers or lower-severity attack chains.
Track these in the appropriate domain even when excluded from a focused diff
review. Intended design is not automatically acceptable risk. Memory-safe code
can cross unsafe/native boundaries. Unguessable IDs do not replace authorization.
Treat safety of URLs, operator inputs and framework defaults as contextual claims.

Keep the existing free-source checks and single-assistant workflow by default.
Anthropic's API-backed action and reference pipeline are optional integrations,
not dependencies. Before enabling them, establish account access, cost limits,
data-sharing scope and explicit permission for posting comments. Review current
upstream security caveats, pin the reviewed revision and restrict credentials.
Never execute repository text or downloaded instructions as shell commands.

## Review output

Use existing security-records templates; add per finding: source IDs, reviewed
revision, inspected caller/sink locations, prerequisites, controls and bypass
analysis, verdict (confirmed / refuted with evidence / cannot verify / duplicate),
severity, confidence, owner, duplicate links, variant search and next verification.
Keep unresolved cases visible. Source-only confirmation is labelled as such.

## Provenance and maintenance

Reviewed September 23, 2026. These are concise, independently written
adaptations, not copies of upstream skill files or a claim of Anthropic execution.

- [Security-review command](https://github.com/anthropics/claude-code-security-review/blob/0c6a49f1fa56a1d472575da86a94dbc1edb78eda/.claude/commands/security-review.md) and [README](https://github.com/anthropics/claude-code-security-review/blob/0c6a49f1fa56a1d472575da86a94dbc1edb78eda/README.md): diff/context review and optional integration considerations. Repository license: MIT.
- [Triage](https://github.com/anthropics/defending-code-reference-harness/blob/d3bea6b5793b5f3d59a75ebe69a58efa88383145/.claude/skills/triage/SKILL.md): source verification, root-cause grouping and prioritization.
- [Threat model](https://github.com/anthropics/defending-code-reference-harness/blob/d3bea6b5793b5f3d59a75ebe69a58efa88383145/.claude/skills/threat-model/SKILL.md): source-derived modelling and persistent threat classes.
- [Patch](https://github.com/anthropics/defending-code-reference-harness/blob/d3bea6b5793b5f3d59a75ebe69a58efa88383145/.claude/skills/patch/SKILL.md): root-cause fixes, sibling variants and bypass review. Reference harness license: Apache-2.0.

During monthly method review, compare current upstream revisions with these
reviewed versions. Assess useful changes, licenses and scope differences before
adopting them. Never auto-execute or blindly replace this workflow from upstream.

## Acceptance cases

Evaluate in a disposable environment; record executed versus reasoning-only checks.

- A scanner reports a missing file: cannot verify, retained for follow-up.
- Two endpoints require separate authorization fixes: keep distinct findings.
- A resource-exhaustion issue is omitted by a focused reviewer: retain it in
  availability coverage and assess safely in isolation.
- The local branch differs from approved production: no claim of a live fix.
- A proposed patch closes one caller but leaves a sibling exposed: incomplete fix.
- Source review supports a fix but tests cannot run: candidate remains unverified.

