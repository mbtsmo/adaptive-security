# Configuration and evidence templates

Copy/adapt these into the target project when establishing the programme. Do not
embed credentials or site-specific infrastructure IDs into the reusable skill.

## Programme configuration

- Owned targets and excluded third parties:
- Approved live source/artifact identity; staging isolation evidence:
- Authorized local changes, staging actions and production release boundaries:
- Timezone and scheduler/run time; host execution prerequisites:
- Daily/weekly/monthly/quarterly/annual cadence and last successful completion:
- Non-disruptive production request bounds and stop conditions:
- Available tools; unavailable capabilities and exact dependent blockers:
- Local protected backup root, encryption/recovery method and retention:
- Database/object coverage; restore procedure and excluded resources:
- Required release gates and rollback authorization:
- Evidence/Git paths, repository ownership and notification preferences:
- Last source refresh and next prioritized coverage improvement:

## Run record

- UTC run ID, local reporting time, trigger, start/final commit IDs in runner state.
- Status: in progress / complete within stated scope / partial / failed / blocked.
- Tested commit/artifact hash and initial dirty/staged work; preserve unrelated work.
- Each check: cadence layer, exact scope, tool/source version, retrieved timestamp,
  actual result, sanitized evidence reference, and coverage limitation.
- Threats: identifiers, package/version or component, exposure by environment,
  confidence/severity, first seen, deadline, verification and remaining work.
- Backup BEFORE changes: location, scope, hashes, restore evidence and exclusions.
- Changes: explicit paths/resources, why, regression before/after and gate results.
- Local/staged/deployed identities; rollback if any and post-action verification.
- Catalogue improvement actually completed, unchanged tests, gaps and next priority.
- Source/feed failures, skipped checks, independent work completed and blockers.
- Next due layers based on successful completion, not an attempted partial run.
- Notification decision and reason; healthy quiet runs still receive Git commits.

Append a concise changelog entry for every execution. Use explicit owned paths
when committing. If no Git repository exists, prepare records locally and ask for
only the missing repository decision; do not invent remote access or claim commits.

## Threat-to-test register

| Threat/source/date | Component and affected versions | Applicability/exposure | Test ID/environment | Evidence/result | Gap/next action/priority | Status/deadline |
| --- | --- | --- | --- | --- | --- | --- |

## Completion contract

Maintain separate truth for discovered, reproduced, fixed locally, verified,
staged, deployed and closed. A finding is closed only after verification in the
relevant authorized target; a deployment blocker leaves the live finding open.
Keep raw sensitive evidence and backups outside Git with protected access.
