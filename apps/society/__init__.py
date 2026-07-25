"""
Society Runtime
===============

Top-level container for AI organizations.
Combines Organization Runtime, Team Builder, Communication, Collective Memory, and Metrics.

Usage:
    from apps.society import create_society, SocietyRuntime

    society = create_society("My AI Company")
    society.register_agent(CEOA(...))
    society.assign_role("ceo-1", AgentRole.CEO, Department.ENGINEERING)
    society.assign_role("cto-1", AgentRole.DIRECTOR, Department.ENGINEERING, manager_id="ceo-1")

    team = society.form_team_for_task("Build a web application")
    result = await society.run_project("proj-1", team.team_id, {"type": "build", "target": "webapp"})

Or, using the intent-router main entry point:
    result = await society.process_user_request("Build a REST API")
"""

from apps.society.society import (
    Project,
    SocietyConfig,
    SocietyRuntime,
    create_society,
)

__all__ = [
    "Project",
    "SocietyConfig",
    "SocietyRuntime",
    "create_society",
]
