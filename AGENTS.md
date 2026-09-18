# AGENTS.md — GitHub Profile Search Universal Agent Instructions

## Overview
GitHub Profile Search is an open-source, OpenGAP-compliant developer intelligence copilot. It queries the official GitHub REST API v3 to retrieve, summarize, and analyze developer profiles, repository statistics, and open-source contributions.

## Operational Workflow

When interacting with GitHub Profile Search in any agent runtime (Claude Code, OpenAI, CrewAI, Lyzr):
1. **Target Identification:** Parse the user query for target GitHub handles (e.g., octocat, 	orvalds, or organizational handles like acebook, google).
2. **Execute Verified Retrieval:** Query the GitHub REST API (GET https://api.github.com/users/{username}) and fetch recent repositories (GET https://api.github.com/users/{username}/repos?sort=updated&per_page=12).
3. **Audit Rate Limits & Sanitize:** Inspect response headers (X-RateLimit-Remaining). Ensure no private API tokens or unmasked contact data leave the runtime.
4. **Synthesize Analytics:** Calculate language distribution percentages, total stars, forks, and sort top repositories by stars and recent activity.
5. **Acknowledge Data Boundaries:** If a user account does not exist or has zero public repositories, explicitly notify the user rather than guessing or interpolating facts.
