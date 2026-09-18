# EXPLAINABILITY.md

This document explains the internal mechanisms, data lineage, algorithmic decisions, and operational boundaries of **GitHub Profile Search** in accordance with the OpenGAP specification (spec version 0.1.0).

---

## 1. How the Agent Decides

GitHub Profile Search makes decisions through a deterministic, multi-stage telemetry pipeline that retrieves public engineering footprints from GitHub's REST API and synthesizes them into structured developer analytics.

### Decision Architecture Workflow

`
User Query / Input Handle
    │
    ▼
[Stage 1: Handle Normalization & Sanitization]
    │  - Strips leading '@', URL prefixes (https://github.com/), and whitespace
    │  - Enforces GitHub username constraints: /^[a-z\d](?:[a-z\d]|-(?=[a-z\d])){0,38}$/i
    ▼
[Stage 2: Rate-Limit Check & Cache Validation]
    │  - Inspects local cache / ETag headers for cached user state
    │  - Verifies X-RateLimit-Remaining > 1 before firing outbound HTTP calls
    ▼
[Stage 3: Canonical Profile Retrieval]
    │  - Queries GET https://api.github.com/users/{username}
    │
    ├── [HTTP 404: User Not Found] ──► Deterministic refusal; displays 'User Not Found'
    ├── [HTTP 403: Rate Exceeded]  ──► Throttling alert; computes reset duration
    └── [HTTP 200: Success]        ──► Proceed to Stage 4
    ▼
[Stage 4: Repository Telemetry & Activity Gathering]
    │  - Queries GET https://api.github.com/users/{username}/repos?sort=updated&per_page=30
    │  - Filters forks (optional) and identifies original vs contributed projects
    ▼
[Stage 5: Algorithmic Ranking & Metrics Computation]
    │  - Primary Language Aggregation: counts occurrences and calculates percentage shares
    │  - Star & Fork Aggregation: sums total community engagement metrics
    │  - Repository Impact Score: evaluates stars, recency of last push, and fork velocity
    ▼
[Stage 6: Output Presentation & Citation Formatting]
    │  - Produces structured cards, direct canonical links, and OpenGAP metadata
    ▼
Output Delivered to User / Consuming Agent
`

### Repository Ranking Algorithm

When prioritizing repositories for display, the agent uses a weighted scoring formula rather than simple star counts:

\text{Score}(R) = (\text{Stars} \times 0.50) + (\text{Forks} \times 0.25) + (\text{RecencyScore} \times 0.25)

Where $\text{RecencyScore} = \max\left(0, 100 - \frac{\text{Days since last push}}{3}\right)$.

This ensures active, recently updated repositories are surfaced alongside historically popular repositories, preventing stale projects from dominating developer insights.

---

## 2. The Data It Uses & Data Lineage

All intelligence synthesized by GitHub Profile Search originates exclusively from verified GitHub REST API v3 endpoints.

### API Endpoints & Lineage

| Endpoint | Method | Data Harvested | Usage in Decision Making |
|---|---|---|---|
| /users/{username} | GET | Name, bio, avatar URL, public repos count, followers, following, creation date, company, location, blog | Identity establishment, baseline activity scale, community reach |
| /users/{username}/repos | GET | Repository names, descriptions, primary languages, stargazers count, forks, updated timestamps, open issues | Language distribution, developer focus areas, repository health |
| /users/{username}/orgs | GET | Public organization affiliations, logos, descriptions | Team collaboration, enterprise open-source participation |

### Data Authenticity & Verification
- **Zero Third-Party Scraping:** Telemetry is gathered only via official JSON APIs; no unauthenticated HTML scraping is used.
- **ETag Validation:** Responses store ETag headers. Subsequent requests send If-None-Match headers to minimize network payload and avoid counting against GitHub rate quotas when content is unchanged.

---

## 3. Guardrails, Governance & Security Boundaries

### 1. Rate-Limit Governance
The agent monitors GitHub's HTTP rate limiting headers:
- X-RateLimit-Limit: Maximum requests permitted within the window (60 for unauthenticated, 5,000 for authenticated).
- X-RateLimit-Remaining: Available calls remaining in the current window.
- X-RateLimit-Reset: Unix epoch timestamp at which the rate window resets.

When X-RateLimit-Remaining drops below 3, the agent halts background polling, logs a rate warning, and reports the exact time until the quota refreshes.

### 2. PII & Secret Redaction
- **Email Redaction:** GitHub user emails are masked by default (c***@***.com) unless the user explicitly enables public email sharing in their profile settings.
- **Token Shielding:** The agent never renders or logs authorization tokens (ghp_*, github_pat_*). Any accidental string matching GitHub token patterns in URLs or commits is redacted immediately ([REDACTED_GITHUB_TOKEN]).

---

## 4. Limitations & Operational Boundaries

1. **Private Repositories:** The agent has zero visibility into private repositories, internal enterprise organizations, or hidden commit history. Analytics reflect solely public open-source contributions.
2. **Unauthenticated Rate Limits:** In the default standalone browser mode without a GitHub Personal Access Token (PAT), queries are constrained to 60 requests per hour per IP address.
3. **Contribution Graph Graphicals:** The contribution heatmap grid (the green squares) is rendered on GitHub via private internal GraphQL/SVG endpoints; the REST API provides total commit metrics via event streams rather than full 365-day SVG grids.
4. **Organization Accounts vs Individual Users:** Organizations return 	ype: "Organization" and have zero followers/following count (they have members); the agent detects this and dynamically adjusts the metrics layout.

---

## 5. Verification & Audit Trail

Every transaction executed by the agent can be verified against the official GitHub API:
- **Canonical URLs:** Every card links directly to https://github.com/{username} and https://github.com/{username}/{repo}.
- **Structured Telemetry Schema:** Exports and logs are formatted in JSON matching the OpenGAP specification.
- **Reproducibility:** Re-querying the GitHub API with the same parameters yields identical results (subject to upstream updates by the user).
