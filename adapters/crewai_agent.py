"""
CrewAI Export Adapter for GitHub Profile Search Agent
Generated in compliance with OpenGAP spec v0.1.0
"""

import json
from typing import Any, Dict

def export_crewai_agent() -> Dict[str, Any]:
    """Exports agent parameters for CrewAI Agent declaration."""
    return {
        "role": "GitHub Profile Intelligence Officer",
        "goal": "Retrieve, analyze, and synthesize public developer profiles and open-source footprints with verifiable accuracy",
        "backstory": (
            "You are an expert developer intelligence agent. "
            "You analyze GitHub portfolios, evaluate language proficiencies, quantify star velocities, "
            "and identify top-tier engineering talent without bias or hallucination."
        ),
        "verbose": True,
        "allow_delegation": False,
        "tools": [
            "fetch_user_profile",
            "search_repositories",
            "calculate_developer_metrics"
        ],
        "compliance": {
            "rate_limit_monitoring": True,
            "pii_redaction": True
        }
    }

if __name__ == "__main__":
    agent_config = export_crewai_agent()
    print("[SUCCESS] Exported GitHub Profile Search for CrewAI:")
    print(json.dumps(agent_config, indent=2))

