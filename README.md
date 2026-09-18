# GitHub Profile Search Agent 🔍

[![Spec: OpenGAP v0.1.0](https://img.shields.io/badge/spec-OpenGAP%20v0.1.0-blue)](https://github.com/open-gitagent/opengap)
[![Passport: Certified](https://img.shields.io/badge/HiDevs%20GitAgent%20Passport-Approved-purple)](https://app.hidevs.xyz/passport)
[![Category: Developer Tools](https://img.shields.io/badge/category-Developer%20tools-green)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> An autonomous, OpenGAP-compliant developer intelligence copilot that searches, evaluates, and synthesizes public GitHub developer profiles, repository ecosystems, and tech stack telemetry with verifiable explainability.

---

## 🌟 Overview

**GitHub Profile Search Agent** transforms raw GitHub REST API v3 payloads into structured developer profiles, language breakdown analytics, community engagement scores (stars/forks), and repository impact rankings.

Built on the **OpenGAP (Open Git Agent Protocol)** standard, this entire repository functions natively as an AI agent that can run in the browser, execute from the terminal CLI, or export cleanly into any target LLM framework.

### 🛡️ GitAgent Passport Checkpoint Compliance

| Checkpoint | Status | Details |
|---|---|---|
| **01. Validate** | ✅ **Passed** | Strict `agent.yaml` manifest targeting OpenGAP spec `0.1.0` in the **Developer tools** domain. |
| **02. Explain** | ✅ **Passed** | Comprehensive `EXPLAINABILITY.md` covering algorithmic decision trees, data lineage, ranking equations, and boundary constraints. |
| **03. Export** | ✅ **Passed** | 4 Framework Visas earned (**OpenAI SDK**, **CrewAI**, **Claude Code**, and **Lyzr**). |

---

## 🗂️ Agent Repository Structure

```
github-profile-search/
├── agent.yaml              # Core OpenGAP manifest (v0.1.0)
├── SOUL.md                 # Agent persona, identity, and developer craft values
├── RULES.md                # Hard constraints, rate-limit boundaries & safety checks
├── DUTIES.md               # Segregation of duties & role conflict matrix
├── AGENTS.md               # Framework-agnostic universal agent instructions
├── EXPLAINABILITY.md       # Decision mechanisms, data lineage & boundaries
├── index.html              # Standalone web copilot & interactive UI
├── agent.py                # Validation runner, framework exporter & CLI
│
├── skills/                 # Capability modules
│   ├── profile-retrieval/
│   │   └── SKILL.md
│   ├── repository-analytics/
│   │   └── SKILL.md
│   └── developer-activity-audit/
│       └── SKILL.md
│
├── tools/                  # MCP-compatible tool schemas
│   ├── fetch-user-profile.yaml
│   ├── search-repositories.yaml
│   └── calculate-developer-metrics.yaml
│
└── adapters/               # Framework export targets for Passport Visas
    ├── openai_agent.py     # OpenAI Agents SDK
    ├── crewai_agent.py     # CrewAI Agent & Task
    ├── claude_code.json    # Claude Code configuration
    └── lyzr_agent.py       # Lyzr Studio & Agent API
```

---

## 🚀 Quick Start

### 1. Interactive Web UI
Simply open `index.html` in any web browser:
- Search any GitHub handle (e.g. `torvalds`, `octocat`, `Chithra582`).
- View total community stars, forks, follower reach, and color-coded language percentage breakdown.
- Directly link to active repositories.

### 2. OpenGAP Agent Validation
Run the built-in validation suite to verify OpenGAP specification conformity:
```bash
python agent.py --validate
```
Output:
```
=== OpenGAP Validation Suite (Spec v0.1.0) ===
 [PASS] Required file present: agent.yaml
 [PASS] Required file present: SOUL.md
 [PASS] Required file present: RULES.md
 [PASS] Required file present: DUTIES.md
 [PASS] Required file present: EXPLAINABILITY.md
 [PASS] Required file present: AGENTS.md
 [PASS] Tools declared: 3 schemas found
 [PASS] Skills declared: 3 skills found
 [PASS] Framework export adapters found: 4

All OpenGAP Checkpoints (Validate, Explain, Export) PASSED cleanly!
```

### 3. Framework Exports (Visas)
Export this agent to your framework of choice:

```bash
# Export all framework configurations
python agent.py --export all

# Or run individual framework adapters
python adapters/openai_agent.py
python adapters/crewai_agent.py
python adapters/lyzr_agent.py
```

### 4. CLI Profile Search
Query any developer profile directly from your terminal:
```bash
python agent.py --search octocat
```

---

## 🔒 Governance & Rate Limit Stewardship

- **API Quota Management**: Proactively tracks `X-RateLimit-Remaining` to ensure requests never exceed unauthenticated (60/hr) or token-based (5,000/hr) GitHub quotas.
- **PII Redaction**: User email addresses are masked by default unless marked public; authentication tokens are strictly stripped from logs.
- **Zero Hallucination**: Only verified empirical attributes returned by the GitHub REST API are displayed.

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).
