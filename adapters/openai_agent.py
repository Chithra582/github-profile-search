"""
OpenAI SDK Export Adapter for GitHub Profile Search Agent
Generated in compliance with OpenGAP spec v0.1.0
"""

import json
import os
from typing import Any, Dict

SYSTEM_PROMPT = """You are GitHub Profile Search Agent, an autonomous developer intelligence copilot.
Your job is to search, retrieve, evaluate, and synthesize public GitHub engineering profiles and repository ecosystems.
Always ground your answers in official GitHub REST API data. Respect rate limits and redact sensitive PII."""

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "fetch_user_profile",
            "description": "Retrieves public profile metadata and account metrics for a given GitHub username",
            "parameters": {
                "type": "object",
                "properties": {
                    "username": {
                        "type": "string",
                        "description": "GitHub username handle"
                    }
                },
                "required": ["username"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_repositories",
            "description": "Queries public repositories belonging to a GitHub user",
            "parameters": {
                "type": "object",
                "properties": {
                    "username": {"type": "string", "description": "GitHub handle"},
                    "sort": {"type": "string", "enum": ["updated", "stars", "created", "pushed"], "default": "updated"},
                    "per_page": {"type": "integer", "default": 12}
                },
                "required": ["username"]
            }
        }
    }
]

def export_openai_spec() -> Dict[str, Any]:
    """Exports agent configuration into OpenAI Agent / ChatCompletion payload format."""
    return {
        "model": "gpt-4o-mini",
        "temperature": 0.2,
        "max_tokens": 4096,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT}
        ],
        "tools": TOOLS
    }

if __name__ == "__main__":
    spec = export_openai_spec()
    print("[SUCCESS] Exported GitHub Profile Search for OpenAI SDK:")
    print(json.dumps(spec, indent=2))

