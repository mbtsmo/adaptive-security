# Operating defaults and threat sources

Configure these choices per project; preserve an existing accepted cadence.
Intervals are risk-based defaults, not OWASP mandates.

| Interval | Work |
| --- | --- |
| Daily | Current threats and malware advisories; dependency/source/secret scans; changed attack surface; bounded live checks; available security telemetry; outstanding findings; backup freshness and integrity |
| 7 days | Full release/security gate, dependency provenance changes, retest fixes and complete a coverage improvement |
| 30 days | Applicable current stable OWASP ASVS/WSTG assessment and authenticated exploratory tests; refresh catalogue and methods |
| 90 days | Threat model, IAM/MFA, WAF/rate limits, secrets, cloud permissions, recovery rehearsal, retention and incident response |
| 365 days | Independent human assessment status and scope review; do not purchase or book automatically |
| Significant change or relevant urgent threat | Bring affected deeper checks forward at the next available execution; use an existing authorized event trigger where available |

Set an explicit owner-approved IANA timezone and local run time. Preserve the
project's existing schedule; configure these values when establishing a new one.
Keep immutable audit IDs in UTC and reporting/deadlines in configured local time.
A single daily scheduler may dispatch layers using their last SUCCESSFUL finish.
Partial work does not reset the success clock. Document execution availability,
missed runs and lack of true continuous monitoring. Preserve notification intent.

Default production bounds when none exist: one concurrent read-only request,
at most one request/second and 100 requests/run, allowlisted owned hosts only,
no cross-host redirect following, stop on throttling or degradation. These bounds
do not authorize destructive probes. Stage authenticated, authorization, upload,
injection, SSRF, malformed-body, race and business-logic tests in verified isolation.
Include privacy consent, cache leaks, webhook signatures/replays, AI trust boundaries
and resource limits where applicable. Mock email, CRM, payments and paid AI calls.
Avoid denial-of-service, brute force, third-party testing and real-data extraction.

Threat sources (verify current APIs, limits and freshness; prefer free access):
- Vendor/maintainer security advisories for the observed deployed/build stack.
- https://www.cisa.gov/known-exploited-vulnerabilities-catalog
- https://github.com/advisories — malware is a separate category, include type:malware.
- https://docs.github.com/en/code-security/how-tos/report-and-fix-vulnerabilities/fix-reported-vulnerabilities/browse-advisory-database
- https://osv.dev/ and https://google.github.io/osv.dev/data/
- https://github.com/ossf/malicious-packages
- https://owasp.org/www-project-application-security-verification-standard/
- https://owasp.org/www-project-web-security-testing-guide/stable/
- https://owasp.org/www-project-api-security/ and https://genai.owasp.org/

No single list is exhaustive. Deduplicate overlapping CVE/GHSA/OSV identifiers;
retain original sources and distinguish withdrawn/uncertain reports. Do not send
private code, secrets or private package names to public APIs without authorization.
Use local/private matching where needed. Do not turn partial pagination or an
unavailable feed into zero findings. Record build-only versus runtime exposure.

Keep protected backups in a configured local directory, excluded from source
control. Verify hashes plus appropriate restore checks, including database
integrity in isolation. Inventory-only object backups cover data only if storage
is verified empty. Record missing static assets, secrets and recovery keys. Use
secure encryption suitable for the host; host-bound encryption alone is not
portable disaster recovery. Do not purge backups without an agreed retention rule.

Suggested response targets: reachable exploited/critical immediately, high within
7 days, medium within 30 and low within 90. Tune to the project and impact; these
are operating targets, not compliance guarantees. Escalate newly overdue work.
