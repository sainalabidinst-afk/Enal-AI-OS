import yaml
import logging
from dataclasses import dataclass, field
from typing import Any
from pathlib import Path

logger = logging.getLogger(__name__)


@dataclass
class Skill:
    name: str
    category: str
    description: str
    agent: str
    capabilities: list[str] = field(default_factory=list)
    tools: list[str] = field(default_factory=list)
    cost_weight: float = 1.0
    metadata: dict[str, Any] = field(default_factory=dict)


class SkillRegistry:
    def __init__(self, skills_path: str = "agents/skills.yaml"):
        self.skills: dict[str, Skill] = {}
        self.skills_path = Path(skills_path)
        self._load()

    def _load(self):
        if not self.skills_path.exists():
            logger.warning(f"Skills file not found: {self.skills_path}")
            return
        with open(self.skills_path) as f:
            data = yaml.safe_load(f) or {}
        for item in data.get("skills", []):
            skill = Skill(**item)
            self.skills[skill.name] = skill
        logger.info(f"Loaded {len(self.skills)} skills")

    def find_by_capability(self, capability: str) -> list[Skill]:
        return [s for s in self.skills.values() if capability in s.capabilities]

    def find_by_category(self, category: str) -> list[Skill]:
        return [s for s in self.skills.values() if s.category == category]

    def get(self, name: str) -> Skill | None:
        return self.skills.get(name)

    def list_all(self) -> list[Skill]:
        return list(self.skills.values())


skill_registry = SkillRegistry()
