"""
Tests for backend/app/core/skills_registry.py — RFC-0001 Skills Registry.
"""

import textwrap

import pytest
import yaml

from backend.app.core.skills_registry import SkillsRegistry


class TestSkillsRegistry:
    @pytest.fixture
    def registry(self):
        reg = SkillsRegistry()
        yield reg
        reg.clear()

    @pytest.fixture
    def sample_manifest_dir(self, tmp_path):
        pack_dir = tmp_path / "test_pack"
        pack_dir.mkdir()
        manifest = {
            "capability_pack": {
                "id": "test_pack",
                "version": "1.0.0",
                "display_name": "Test Pack",
                "description": "A test pack",
                "entry_point": "apps.test_pack.engine.TestPackEngine",
                "category": "testing",
                "maturity_level": 3,
                "quality_target": "A",
                "capabilities": [
                    {
                        "id": "do_thing",
                        "name": "Do Thing",
                        "description": "Does a thing",
                        "input_schema": "ThingRequest",
                        "output_schema": "ThingResult",
                    }
                ],
                "dependencies": {
                    "capabilities": ["execution_runtime"],
                    "external": [{"name": "numpy", "version": ">=1.0.0"}],
                },
                "pipeline": [
                    {"stage": "parse", "capability": "test_pack.parse"},
                    {"stage": "analyze", "capability": "test_pack.analyze"},
                ],
                "metadata": {"author": "Test Team"},
            }
        }
        with open(pack_dir / "skills.yaml", "w") as f:
            yaml.dump(manifest, f)
        return tmp_path

    def test_load_manifest_valid(self, registry, sample_manifest_dir):
        manifest_path = str(sample_manifest_dir / "test_pack" / "skills.yaml")
        cfg = registry.load_manifest(manifest_path)
        assert cfg is not None
        assert cfg.id == "test_pack"
        assert len(cfg.capabilities) == 1
        assert cfg.capabilities[0].id == "do_thing"

    def test_load_pack_from_directory(self, registry, sample_manifest_dir):
        cfg = registry.load_pack(str(sample_manifest_dir / "test_pack"))
        assert cfg is not None
        assert cfg.id == "test_pack"
        assert "test_pack" in registry.list_packs()

    def test_get_pack(self, registry, sample_manifest_dir):
        registry.load_pack(str(sample_manifest_dir / "test_pack"))
        pack = registry.get_pack("test_pack")
        assert pack is not None
        assert pack.display_name == "Test Pack"

    def test_get_capability(self, registry, sample_manifest_dir):
        registry.load_pack(str(sample_manifest_dir / "test_pack"))
        cap = registry.get_capability("do_thing")
        assert cap is not None
        assert cap.name == "Do Thing"

    def test_get_pack_for_capability(self, registry, sample_manifest_dir):
        registry.load_pack(str(sample_manifest_dir / "test_pack"))
        pack = registry.get_pack_for_capability("do_thing")
        assert pack is not None
        assert pack.id == "test_pack"

    def test_get_pipeline(self, registry, sample_manifest_dir):
        registry.load_pack(str(sample_manifest_dir / "test_pack"))
        pipeline = registry.get_pipeline("test_pack")
        assert len(pipeline) == 2
        assert pipeline[0].stage == "parse"
        assert pipeline[0].capability == "test_pack.parse"

    def test_get_dependencies(self, registry, sample_manifest_dir):
        registry.load_pack(str(sample_manifest_dir / "test_pack"))
        deps = registry.get_dependencies("test_pack")
        assert deps == ["execution_runtime"]

    def test_discover(self, registry, sample_manifest_dir):
        registry.configure([str(sample_manifest_dir)])
        packs = registry.discover()
        assert "test_pack" in packs

    def test_has_manifest(self, registry, sample_manifest_dir):
        assert SkillsRegistry.has_manifest(str(sample_manifest_dir / "test_pack"))
        assert not SkillsRegistry.has_manifest(str(sample_manifest_dir))

    def test_load_all(self, registry, sample_manifest_dir):
        registry.configure([str(sample_manifest_dir)])
        packs = registry.load_all()
        assert "test_pack" in packs

    def test_list_capabilities(self, registry, sample_manifest_dir):
        registry.load_pack(str(sample_manifest_dir / "test_pack"))
        caps = registry.list_capabilities()
        assert "do_thing" in caps

    def test_validate_manifest_valid(self, registry, sample_manifest_dir):
        manifest_path = str(sample_manifest_dir / "test_pack" / "skills.yaml")
        report = registry.validate_manifest(manifest_path)
        assert report.passes is True
        assert report.pack_id == "test_pack"
        assert len(report.errors) == 0

    def test_validate_manifest_missing_id(self, registry, tmp_path):
        pack_dir = tmp_path / "bad_pack"
        pack_dir.mkdir()
        with open(pack_dir / "skills.yaml", "w") as f:
            yaml.dump({"capability_pack": {"version": "1.0.0"}}, f)

        manifest_path = str(pack_dir / "skills.yaml")
        report = registry.validate_manifest(manifest_path)
        assert report.passes is False
        assert any("id" in e for e in report.errors)

    def test_validate_manifest_missing_capability_pack_key(self, registry, tmp_path):
        pack_dir = tmp_path / "bad_pack2"
        pack_dir.mkdir()
        with open(pack_dir / "skills.yaml", "w") as f:
            yaml.dump({"foo": "bar"}, f)

        manifest_path = str(pack_dir / "skills.yaml")
        report = registry.validate_manifest(manifest_path)
        assert report.passes is False
        assert "capability_pack" in report.errors[0]

    def test_detect_no_circular_dependencies(self, registry, sample_manifest_dir):
        registry.load_pack(str(sample_manifest_dir / "test_pack"))
        cycles = registry.detect_circular_dependencies()
        assert cycles == []

    def test_detect_circular_dependencies(self, registry, tmp_path):
        pack_a = tmp_path / "pack_a"
        pack_a.mkdir()
        (pack_a / "skills.yaml").write_text(
            textwrap.dedent("""
            capability_pack:
              id: pack_a
              version: "1.0.0"
              entry_point: "apps.pack_a.engine"
              capabilities:
                - id: cap_a
                  name: "A"
                  description: "A capability"
              dependencies:
                capabilities: ["cap_b"]
              pipeline: []
        """)
        )

        pack_b = tmp_path / "pack_b"
        pack_b.mkdir()
        (pack_b / "skills.yaml").write_text(
            textwrap.dedent("""
            capability_pack:
              id: pack_b
              version: "1.0.0"
              entry_point: "apps.pack_b.engine"
              capabilities:
                - id: cap_b
                  name: "B"
                  description: "B capability"
              dependencies:
                capabilities: ["cap_a"]
              pipeline: []
        """)
        )

        registry.load_pack(str(pack_a))
        registry.load_pack(str(pack_b))
        cycles = registry.detect_circular_dependencies()
        assert len(cycles) > 0
        cycle = cycles[0]
        assert "pack_a" in cycle
        assert "pack_b" in cycle
