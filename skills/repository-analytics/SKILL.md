---
name: repository-analytics
description: Analyzes developer repositories, calculating language distributions, star popularity, and fork metrics
---

# Repository Analytics Skill

## Purpose
Evaluate and quantify a developer's public repository portfolio to uncover tech stack proficiencies and project impact.

## Capabilities
- Ingest repository arrays from /users/{username}/repos.
- Calculate primary programming language percentage shares across all public codebases.
- Aggregate total star count and community fork numbers.
- Score and prioritize top repositories based on stars and recent push activity.

## Execution Guidelines
1. Fetch repository collection sorted by updated timestamp.
2. Aggregate language occurrences into weighted frequency maps.
3. Filter out archived or empty repositories when computing active stack.
4. Produce top-10 ranked repository showcase with star badges and license indicators.
