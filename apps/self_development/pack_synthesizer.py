"""
Pack Synthesizer
================

Generates a draft Capability Pack schema from a capability gap proposal.
Outputs are structured artifacts: schemas, engine stub, worker stub, and
golden test scaffold.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from apps.self_development.schemas import CapabilityProposal

logger = logging.getLogger(__name__)


@dataclass
class PackSynthesisResult:
    proposal: CapabilityProposal
    schema_created: bool
    engine_created: bool
    worker_created: bool
    tests_scaffolded: bool
    artifacts: dict[str, Any] = field(default_factory=dict)


class PackSynthesizer:
    """Synthesizes draft capability pack artifacts from a proposal."""

    def __init__(self, output_root: Path | None = None) -> None:
        self.output_root = Path(output_root or Path("apps"))

    def synthesize(self, proposal: CapabilityProposal) -> PackSynthesisResult:
        pack_dir = self.output_root / proposal.domain
        pack_dir.mkdir(parents=True, exist_ok=True)

        schema_created = self._create_schema(pack_dir, proposal)
        engine_created = self._create_engine(pack_dir, proposal)
        worker_created = self._create_worker(pack_dir, proposal)
        tests_scaffolded = self._scaffold_tests(pack_dir, proposal)

        artifacts = {
            "pack_dir": str(pack_dir),
            "schema": str(pack_dir / "schemas.py"),
            "engine": str(pack_dir / "engine.py"),
            "worker": str(pack_dir / "worker.py"),
            "tests": str(pack_dir / "test_scaffold.py"),
        }
        logger.info("Pack synthesized: %s", proposal.domain)
        return PackSynthesisResult(
            proposal=proposal,
            schema_created=schema_created,
            engine_created=engine_created,
            worker_created=worker_created,
            tests_scaffolded=tests_scaffolded,
            artifacts=artifacts,
        )

    def _create_schema(self, pack_dir: Path, proposal: CapabilityProposal) -> bool:
        schema_path = pack_dir / "schemas.py"
        if schema_path.exists():
            return False
        class_name = proposal.name.replace(" ", "")
        content = "\n".join([
            "from pydantic import BaseModel, Field",
            "",
            "",
            f"class {class_name}Request(BaseModel):",
            '    query: str = Field(..., description="User query for ' + proposal.name + '")',
            "    context: dict | None = None",
            "",
            "",
            f"class {class_name}Response(BaseModel):",
            '    result: str',
            "    confidence: float = 0.0",
            "    metadata: dict = Field(default_factory=dict)",
            "",
        ])
        schema_path.write_text(content, encoding="utf-8")
        return True

    def _create_engine(self, pack_dir: Path, proposal: CapabilityProposal) -> bool:
        engine_path = pack_dir / "engine.py"
        if engine_path.exists():
            return False
        class_name = proposal.name.replace(" ", "")
        module_name = proposal.domain.replace("-", "_")
        content = "\n".join([
            f"class {class_name}Engine:",
            "    async def execute(self, request) -> dict:",
            '        return {',
            '            "result": "TODO: implement ' + proposal.name + ' engine",',
            '            "confidence": 0.0,',
            '            "metadata": {},',
            "        }",
            "",
            "",
            f"{module_name}_engine = {class_name}Engine()",
            "",
        ])
        engine_path.write_text(content, encoding="utf-8")
        return True

    def _create_worker(self, pack_dir: Path, proposal: CapabilityProposal) -> bool:
        worker_path = pack_dir / "worker.py"
        if worker_path.exists():
            return False
        class_name = proposal.name.replace(" ", "")
        module_name = proposal.domain.replace("-", "_")
        content = "\n".join([
            f"class {class_name}Worker:",
            "    def __init__(self, engine: object | None = None) -> None:",
            "        self.engine = engine",
            "",
            "    async def run(self, task: dict) -> dict:",
            "        return await self.engine.execute(task)",
            "",
            "",
            f"{module_name}_worker = {class_name}Worker()",
            "",
        ])
        worker_path.write_text(content, encoding="utf-8")
        return True

    def _scaffold_tests(self, pack_dir: Path, proposal: CapabilityProposal) -> bool:
        test_path = pack_dir / "test_scaffold.py"
        if test_path.exists():
            return False
        module_name = proposal.domain.replace("-", "_")
        content = "\n".join([
            f"def test_{module_name}_placeholder() -> None:",
            "    assert True",
            "",
        ])
        test_path.write_text(content, encoding="utf-8")
        return True
