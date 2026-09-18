# EXPLAINABILITY.md

This document explains the internal mechanisms, data lineage, and operational boundaries of **GitHub Profile Search** in accordance with the OpenGAP specification.

---

## How the Agent Decides

GitHub Profile Search makes decisions through a deterministic, multi-stage retrieval and telemetry analysis pipeline that queries the official GitHub REST API v3, evaluates repository portfolios, and computes developer insights.

### 1. Decision Architecture
The decision process flows through sequential stages:

```
User Query / Input Handle
    │
    ▼
[Stage 1: Handle Normalization & Syntax Validation]
    │  - Normalizes input string: trims '@' prefix, full URL prefixes, and trailing slashes
    │  - Validates handle against GitHub username standard: /^[a-z\d](?:[a-z\d]|-(?=[a-z\d])){0,38}$/i
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
    │  - Classifies repositories: original codebases vs. forks
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
```

### 2. Retrieval Criteria & Ranking Rubric
When prioritizing repositories for display, the agent evaluates both community reach and active maintenance using a multi-factor ranking formula:

$$\text{Score}(R) = (\text{Stars} \times 0.50) + (\text{Forks} \times 0.25) + (\text{RecencyScore} \times 0.25)$$

Where $\text{RecencyScore} = \max\left(0, 100 - \frac{\text{Days since last push}}{3}\right)$.

- **Stargazers Count (50% Weight)**: Validates community adoption and historical impact.
- **Forks Count (25% Weight)**: Measures developer reuse, downstream contributions, and ecosystem utility.
- **Recency of Updates (25% Weight)**: Prioritizes active projects over stale or abandoned codebases.

### 3. Thresholding & Refusal Decision Criteria
- **404 Not Found Handling**: If GitHub responds with HTTP status 404, the agent halts further execution and deterministically returns an explicit refusal message: *"User not found. Please verify the handle and try again."* It never hallucinates fictitious developers or repositories.
- **Rate-Limit Thresholding**: If `X-RateLimit-Remaining` reaches 0 (or response code is HTTP 403), the agent terminates requests and returns a rate-limit alert with the exact UTC reset timestamp.

### 4. Client-Side Guardrail Decision Gates
Before any telemetry is displayed or exported:
- **PII Redaction Gate**: Developer email addresses are masked unless explicitly flagged as public in the account profile.
- **Secret Redaction Gate**: Authorization tokens matching GitHub Personal Access Token patterns (`ghp_*`, `github_pat_*`, OAuth bearer tokens) are immediately stripped and redacted as `[REDACTED_GITHUB_TOKEN]`.

### 5. Fallback & Offline Decision Mechanism
- When offline or during GitHub outages, the agent serves cached profile telemetry if available.
- If no cache is present, the agent informs the user with an actionable offline status message rather than hanging or returning corrupted data.

### 6. Human-in-the-Loop Governance
- **Zero Silent Modification**: The agent never mutates, forks, or stars repositories on behalf of the user without explicit interactive authorization.
- **Inspectable Telemetry**: Every data point is linkable directly to the canonical source on GitHub.

---

## The Data It Uses

GitHub Profile Search operates strictly under transparent data governance, extracting telemetry exclusively from public GitHub endpoints.

### 1. Ingested Input Data
The agent consumes public developer metadata:
- **User Profile Attributes**: Username, display name, avatar URL, bio text, public email (if shared), location, company affiliation, blog/website URL, twitter username, account creation timestamp.
- **Account Reach Metrics**: Total public repositories count, public gists count, follower count, following count.
- **Repository Telemetry**: Repository names, descriptions, primary programming language, star counts, fork counts, watchers, license classification, push timestamps, open issues count.
- **Organization Affiliations**: Public memberships in engineering organizations and open-source foundations.

### 2. In-Memory Chunking & Storage Architecture
- **In-Memory Aggregation**: Language distribution maps and total engagement calculations are computed on-the-fly in local memory.
- **Ephemeral Session State**: No profile data is stored on remote servers; all telemetry remains confined to client browser memory or local process execution.
- **0-Byte Raw Egress Guarantee**: Retrieved profile data is never uploaded to unauthorized third-party trackers or marketing databases.

### 3. External Relay Data & Redaction Patterns
When profile analytics are exported into framework runtimes (OpenAI SDK, CrewAI, Claude Code, Lyzr):
- Payloads contain strictly structured, sanitized developer summaries.
- **Masked PII Patterns**:
  - Private / Unlisted Emails: `[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}` $\rightarrow$ `c***@***.com`
  - GitHub Personal Access Tokens: `ghp_[a-zA-Z0-9]{36}` $\rightarrow$ `[REDACTED_GITHUB_TOKEN]`
  - Fine-grained PATs: `github_pat_[a-zA-Z0-9_]{82}` $\rightarrow$ `[REDACTED_PAT]`

### 4. Data Privacy, Storage, and Retention
- **Stateless Operation**: Query results are discarded upon session close unless explicitly saved in local browser storage.
- **Compliance Alignment**: Complies with GDPR Article 28 data minimization principles by querying only the public data necessary for developer footprint evaluation.

---

## Limitations

Understanding the operational boundaries and constraints of GitHub Profile Search is critical for reliable usage.

### 1. In-Memory Scale and Capacity Constraints
- **Unauthenticated Rate Limit**: Default queries are bound by GitHub's unauthenticated rate limit of **60 requests per hour per IP address**.
- **Page Size Limits**: To maintain sub-second response times, repository queries are capped at the top 30 most recently updated repositories per user.

### 2. Compute and Cold-Start Profile
- **Network Bound Retrieval**: Analysis speed depends on GitHub REST API latency (typically 100ms - 400ms per endpoint).
- **No Local Compute Overhead**: The agent performs lightweight aggregations without requiring heavy GPU or machine learning compute.

### 3. Connectivity and Synthesis Boundaries
- **Public Internet Dependency**: Real-time queries require an active internet connection to communicate with `api.github.com`.
- **Offline Limitations**: In full offline mode, queries cannot be resolved unless previously stored in local cache.

### 4. Scope and Grounding Boundaries
- **No Private Repository Access**: The agent has zero visibility into private repositories, internal enterprise codebases, or uncommitted work.
- **Contribution Graph Heatmap**: The graphical 365-day green contribution calendar is rendered on GitHub through internal GraphQL/SVG endpoints and is not accessible as a raw matrix via unauthenticated REST API.

### 5. Media and Formatting Constraints
- **Text-Focused Extraction**: The agent processes text metadata; it does not perform deep static analysis on binary files, compiled assets, or container images inside repositories.

### 6. Security and Guardrail Edge Cases
- **Self-Reported Data**: Profile metadata such as location, company, and bio are user-declared fields on GitHub and cannot be independently verified as legal truth.
- **Fork Discrepancies**: If a user primarily contributes via forks without starring or pinning, standard repository listings may under-represent their contributions unless fork inclusion is enabled.

---

## Summary & Compliance Checklist

| Checkpoint 2 Requirement | Corresponding Section | Status |
| :--- | :--- | :---: |
| **How the agent decides** | [How the Agent Decides](#how-the-agent-decides) | **Covered** |
| - Decision architecture & 6-stage pipeline | Section 1 | Verified |
| - Retrieval criteria & ranking rubric | Section 2 | Verified |
| - Thresholding, refusal & missing data logic | Section 3 | Verified |
| - Guardrail decision gates & PII masking | Section 4 | Verified |
| - Fallback & offline mechanism | Section 5 | Verified |
| - Human-in-the-loop governance | Section 6 | Verified |
| **The data it uses** | [The Data It Uses](#the-data-it-uses) | **Covered** |
| - Ingested input data & attributes | Section 1 | Verified |
| - In-memory processing & 0-byte egress | Section 2 | Verified |
| - External relay data & token redaction | Section 3 | Verified |
| - Data privacy & retention | Section 4 | Verified |
| **Its limitations** | [Limitations](#limitations) | **Covered** |
| - API rate limits & quota constraints | Section 1 | Verified |
| - Compute profile & network bounds | Section 2 | Verified |
| - Connectivity & live API dependencies | Section 3 | Verified |
| - Scope boundaries & private repo invisibility | Section 4 | Verified |
| - Media & self-reported data edge cases | Section 5 & 6 | Verified |
