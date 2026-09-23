# Comprehensive coverage and attack-path review

Read this entire catalogue at onboarding and the monthly completeness review.
Read affected domains again for changes, new threats and incidents. It is a
minimum discovery catalogue, not an exhaustive list of possible vulnerabilities.
Expand it for the actual architecture, languages, trust boundaries and threats.
Review adjacent enterprise dependencies; do not test assets outside authorization.

## Coverage contract

Build an asset/data-flow inventory from repository, deployed configuration,
route definitions, schemas, cloud inventory and authorized owner evidence. Include
abandoned versions, preview environments, background jobs and control planes.
Map entry points, principals, data classifications, trust boundaries and outbound
integrations. Reconcile code inventory with deployed inventory; label unknowns.

Create a coverage matrix: domain/control, asset/version, environment, trust
boundary, roles/tenants, test method/ID, dated evidence, actual result, limitation,
owner/next action and next due date. Allowed states: verified pass, verified fail,
partial, not tested, blocked, or not applicable WITH evidence and rationale.
Missing tooling or access means blocked, not not-applicable. A scanner pass cannot
stand in for manual review, authenticated testing or an untested environment.
Never infer compliance or certification from a checklist.

Map applicable requirements to exact IDs in the current stable OWASP ASVS/WSTG,
API guidance and relevant platform standards. Choose and document an ASVS target
level based on sensitivity; Level 2 is a starting point for private portals, with
higher-assurance controls where risk warrants. Verify version and control text;
never invent IDs. Use ATT&CK for adversary paths/detection coverage, not as a
substitute for application verification. Record unsupported or excluded domains.

## Domain catalogue

| Domain | Required review angles when applicable |
| --- | --- |
| Inventory and architecture | Public/private/admin APIs, undocumented or retired routes, debug/metrics endpoints, shadow IT, exposed previews, old origins, missing owners, trust-boundary crossing, fail-open dependencies, secure defaults and attack chains |
| Domain and edge | Registrar/IAM recovery, domain expiry, dangling DNS and subdomain takeover, DNSSEC applicability, TLS chain/hostname/expiry, protocol/cipher policy, HSTS deployment impact, CDN origin bypass, host-header trust, cache keys, WAF/rate-limit gaps and edge/origin policy mismatch |
| Identity lifecycle | Registration/invitation, account enumeration, password/passkey policy, breached-credential controls, MFA enrollment/removal/recovery, account linking, privilege changes, deprovisioning and abandoned service accounts |
| Federation and sessions | OAuth/OIDC/SAML issuer/audience/signature/algorithm validation, key rotation, redirect URI, state/nonce/PKCE, token replay/expiry/revocation, CSRF, fixation, session logout, cookies, device trust, proxy identity headers and confused-deputy paths |
| Authorization and tenancy | Deny by default on every action/object/property, horizontal/vertical escalation, two real synthetic tenants and multiple roles, tenant joins, guessed IDs, bulk actions, exports, attachments, signed URLs, background workers, caches and admin impersonation |
| Input and interpreters | SQL/NoSQL/ORM/LDAP/command/template injection, XSS variants, unsafe deserialization, XML entities, prototype pollution, Unicode/canonicalization discrepancies, parser differentials, parameter pollution, schema/type confusion and mass assignment |
| HTTP and browser boundaries | CSRF/CORS, CSP with actual enforcement, clickjacking, content sniffing, referrer leakage, mixed content, redirects, postMessage origin checks, framing, service-worker scope/cache, browser storage, source maps, client secrets and cross-site information leaks |
| Protocol and intermediary behaviour | Request smuggling/desynchronization, conflicting framing/headers, header injection, cache poisoning/deception, redirects, reverse-proxy trust, HTTP versions, WebSocket handshake/message authorization and streaming cancellation; active tests only in isolation |
| APIs | REST/GraphQL/gRPC/SOAP as present; object/function/property authorization, schema drift, deprecated versions, batching, pagination, query cost/depth, field filtering, content-type/method handling, idempotency, replay, error disclosure and asynchronous status endpoints |
| Files and parsers | File signatures versus extensions/MIME, path traversal, archive extraction/symlinks, decompression bombs in bounded fixtures, polyglots, active content, parser vulnerabilities, antivirus/quarantine, scan bypass, storage ACLs, download authorization, safe disposition and lifecycle deletion |
| Outbound connectivity | SSRF, metadata/internal network reachability, URL normalization, DNS rebinding, redirects after validation, protocol allowlists, egress restrictions, webhook destinations, server-side image/document fetchers and secret forwarding |
| Business logic | Workflow/order bypass, price/currency/rounding, discounts/refunds, entitlement changes, quota circumvention, invitation/referral abuse, automation/fraud, duplicate processing, time windows, cancellation and permission changes mid-operation |
| Concurrency and integrity | Race conditions, TOCTOU, transactions, cross-database/object consistency, partial writes, lost updates, retries, idempotent jobs, dead letters, poison messages, eventual consistency, tombstones and interrupted cleanup/recovery |
| Cryptography and secrets | Approved maintained algorithms/libraries, randomness, key/nonce reuse, encryption at rest/in transit, signing context, key storage/rotation/revocation, certificate validation, secret scope and leaks through logs/builds/backups; no invented cryptography |
| Data and privacy | Minimization, sensitive-field access, masking, retention/deletion including backups, consent/withdrawal/GPC where applicable, analytics leakage, tracking before consent, data residency, export access, test-data sanitization and data classification; legal conclusions require qualified review |
| Databases and storage | Network exposure, authentication/TLS, least privilege, tenant/RLS policies and bypass roles, injection, migrations, object public access, ACL inheritance, signed URL expiry, encryption, snapshots, replication and backup ownership |
| Dependencies and registries | Exact versions and transitive graph, malware advisories, typosquatting/dependency confusion, maintainer takeover, malicious updates, abandoned packages, Git ref drift, lockfile integrity, install hooks, provenance/signatures, native binaries, base images and package lifecycle |
| Source control and CI/CD | Branch/review protections, secret history scanning, workflow token permissions, untrusted PR execution, reusable actions pinned to trusted immutable refs, runner isolation/persistence, artifacts/caches, build signing/SBOM, deploy identity, environment approvals and build-to-live provenance |
| Cloud and infrastructure | IAM/resource policies, organization boundaries, role assumption, workload identity, public services, security groups, control-plane logs, metadata access, secret managers, least-privilege bindings, region/account confusion and configuration drift |
| Hosts, containers and orchestration | Supported OS/runtime, patching, service accounts, root/capabilities, read-only filesystems, mounts/sockets, sandbox escape exposure, network policies, orchestration RBAC, admission controls, image provenance and endpoint protection evidence |
| Serverless, edge and queues | Binding scope, environment separation, shared cache/global state, warm-instance leakage, scheduled jobs, queue producers/consumers, duplicate deliveries, dead-letter handling, platform limits and execution/cost budgets |
| AI, agents and retrieval | Direct/indirect prompt injection, tool/connector permissions, tool-output trust, cross-user memory/RAG isolation, data poisoning, unsafe output execution/rendering, secret/system-context leakage, excessive agency, unsafe deserialization of tool arguments, model supply chain and bounded cost |
| Integrations and vendors | API keys/OAuth scopes, webhook authenticity/replay, email/payment/CRM trust, third-party script compromise, support access, decommissioning, breach notifications, contracts/data flows and vendor outages; do not probe vendors without separate authority |
| Email and human processes | SPF/DKIM/DMARC configuration, mailbox/admin recovery, phishing-resistant MFA, support-assisted reset controls, onboarding/offboarding, insider misuse and approval fraud; review evidence/tabletop by default, no unsolicited phishing campaigns |
| Availability and cost abuse | Bounded resource controls, request/body/upload sizes, regex/query complexity, pagination, stream/time limits, backpressure, cache amplification, storage exhaustion, paid-service spending limits, bot abuse and upstream failure handling; no live load/DoS testing |
| Detection and response | Audit completeness, privilege/data-access events, clock consistency, redaction, tamper protection, log injection, retention, actionable alerts, tested routing, triage ownership, evidence preservation, response runbooks and attacker attempts to blind monitoring |
| Recovery and continuity | Local encrypted backups, separate credentials and offline/immutable recovery where available, restore integrity, RPO/RTO measurement, ransomware/credential compromise, key loss, portable recovery, point-in-time data consistency, rollback with newer data and disaster exercises |
| Governance and physical dependencies | Asset owners, access reviews, risk acceptance expiry, supplier/physical endpoint controls, device loss, key custody, incident contacts and independent human review; record unavailable evidence without claiming technical validation |
| Other surfaces discovered | Mobile/desktop clients, browser extensions, native code/FFI memory safety, IoT/OT, firmware and specialist protocols: record applicability and use relevant standards/qualified testing within explicit scope; do not silently skip or extend authority |

## Exercise complete paths, not isolated checkboxes

For applicable flows, test successful and denied access across anonymous, normal,
privileged, disabled and expired identities; include two synthetic users/tenants.
Cover reads, writes, deletes, exports, downloads and asynchronous work. Include
malformed, boundary-sized, replayed, duplicate, interrupted and concurrent inputs.
Check confidentiality, integrity, availability, privacy and financial/resource
impact. Trace plausible chains across two or more trust boundaries, including
low-severity issues that combine into a serious path, without crossing scope.

Combine code/configuration review, static/secret/dependency scans, authenticated
local dynamic tests, bounded fuzz/property-based tests, manual business-logic
review, controlled failure injection, backup restoration and detection exercises.
Select methods by applicability, not tool count. A blocked method remains a gap.
Use reviewed synthetic fixtures; never download malware to production. Purely
read-only operations can still be expensive: retain request/time/cost bounds.

On suspected active compromise, preserve evidence and switch to the incident
runbook. Do not auto-delete suspicious files or rotate all keys: those actions
can destroy evidence or recovery access. Containment follows existing authority.

## Measure whether coverage is improving

Track applicable/verified/partial/blocked/not-tested controls, overdue findings,
oldest evidence, feed freshness, regression escapes, remediation/retest time and
restore success. Show denominator and scope; never call a checklist percentage
an overall security score. Reopen coverage after relevant code/config changes,
new bypass evidence or changed deployment. Explain infeasible tests and the next
best compensating check. Carry unresolved high-risk work into the next run.

Primary mapping sources (check current stable versions at review time):
- https://owasp.org/projects/asvs
- https://owasp.org/www-project-web-security-testing-guide/stable/
- https://owasp.org/www-project-api-security/
- https://attack.mitre.org/matrices/enterprise/
- https://www.cisa.gov/cross-sector-cybersecurity-performance-goals
- https://owasp.org/projects/artificial-intelligence-security-verification-standard-aisvs-docs
- https://cwe.mitre.org/ for weakness classification, not proof of test coverage.
