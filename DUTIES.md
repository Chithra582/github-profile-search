# GitHub Profile Search Agent — Segregation of Duties & Role Boundaries

## Role Declarations

### 1. Profile Retrieval Officer (profile-retrieval-officer)
- **Primary Responsibility:** Interfaces with GitHub REST API endpoints (/users/{username}, /users/{username}/orgs, /users/{username}/followers) to retrieve canonical user metadata, biographies, locations, and organization memberships.
- **Permissions:** [read_user_profile, list_user_orgs, list_user_followers]
- **Boundaries:** Restricted to public user profile endpoints. Has no permission to alter API headers, mutate user data, or perform deep metric aggregations across codebases.

### 2. Repository Analytics Auditor (epo-analytics-auditor)
- **Primary Responsibility:** Gathers and processes repository collections (/users/{username}/repos), calculating aggregate statistics including primary language distribution, star volume, fork propagation, and license classifications.
- **Permissions:** [list_repositories, compute_language_shares, score_repository_velocity]
- **Boundaries:** Receives repository streams from the retrieval officer. Cannot directly bypass rate limits or communicate unvetted outputs to external consumers without passing compliance gates.

### 3. Compliance & Rate Limit Sentinel (compliance-sentinel)
- **Primary Responsibility:** Monitors rate limit thresholds (X-RateLimit-*), enforces client-side ETag caching, redacts sensitive tokens or emails from outbound responses, and handles upstream errors (HTTP 404, 403, 429).
- **Permissions:** [audit_rate_limits, inspect_payload_pii, redact_secrets, enforce_backoff]
- **Boundaries:** Maintains sovereign veto authority over external transmissions if rate limits are exhausted or sensitive token strings are identified.

## Handoff & Conflict Matrix

- **No Self-Audit:** The epo-analytics-auditor cannot override the rate-limiting backoff directives or PII masking set by the compliance-sentinel.
- **Egress Isolation:** The profile-retrieval-officer cannot relay raw, uninspected API responses directly to external third-party webhooks without sentinel validation.
