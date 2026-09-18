---
name: profile-retrieval
description: Fetches canonical GitHub user profile information, biographical metadata, and community reach stats
---

# Profile Retrieval Skill

## Purpose
Retrieve and normalize canonical GitHub user and organization account information from official endpoints.

## Capabilities
- Parse handle from input text, URLs, or mention tags.
- Query /users/{username} for core metadata (name, bio, location, blog, company, public repo count, followers, following).
- Handle 404 missing user conditions and unauthenticated rate-limit warnings gracefully.
- Sanitize output strings and redact sensitive private information.

## Execution Guidelines
1. Ingest input username handle.
2. Validate handle syntax against GitHub naming conventions.
3. Issue HTTP GET to https://api.github.com/users/{username}.
4. If HTTP status is 404, report clear user-not-found message.
5. If HTTP status is 200, format payload into structured developer profile card.
