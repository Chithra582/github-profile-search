---
name: developer-activity-audit
description: Audits repository commit recency, license governance, and open-source contribution patterns
---

# Developer Activity Audit Skill

## Purpose
Inspect developer activity velocity, maintenance cadence, and open-source licensing compliance.

## Capabilities
- Identify active vs stale projects based on last commit timestamps.
- Audit open-source license adherence (MIT, Apache 2.0, GPL, Unlicensed).
- Detect presence of repository documentation (README, descriptions, homepages).
- Flag potential abandoned repositories.

## Execution Guidelines
1. Traverse repository metadata focusing on pushed_at, license, and has_issues.
2. Compute days elapsed since last commit across the portfolio.
3. Categorize developer portfolio health into Active, Maintained, or Inactive tiers.
4. Output structured audit summary.
