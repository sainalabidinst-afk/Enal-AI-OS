"""
Tests for Template Registry
============================

Tests for template loading, lookup, filtering, searching, and cloning.
"""

import json
import os

from backend.app.core.template_registry import (
    AgentTemplate,
    TemplateMetadata,
    TemplateRegistry,
)


class TestTemplateRegistry:
    """Tests for TemplateRegistry."""

    def test_load_templates_count(self):
        """Test that at least 10 templates are loaded."""
        registry = TemplateRegistry()
        templates = registry.list_templates()
        assert len(templates) >= 10

    def test_template_structure(self):
        """Test that each template has required fields."""
        registry = TemplateRegistry()
        for template in registry.list_templates():
            assert template.id
            assert template.name
            assert template.description
            assert template.category
            assert isinstance(template.tags, list)
            assert isinstance(template.config, dict)

    def test_get_template(self):
        """Test retrieving a specific template by ID."""
        registry = TemplateRegistry()
        templates = registry.list_templates()
        if templates:
            first = templates[0]
            retrieved = registry.get_template(first.id)
            assert retrieved is not None
            assert retrieved.id == first.id
            assert retrieved.name == first.name

    def test_get_template_not_found(self):
        """Test that getting a non-existent template returns None."""
        registry = TemplateRegistry()
        assert registry.get_template("non-existent-id") is None

    def test_filter_by_category(self):
        """Test filtering templates by category."""
        registry = TemplateRegistry()
        categories = set(t.category for t in registry.list_templates())
        for cat in categories:
            filtered = registry.list_by_category(cat)
            assert len(filtered) > 0
            for t in filtered:
                assert t.category.lower() == cat.lower()

    def test_search(self):
        """Test searching templates."""
        registry = TemplateRegistry()
        templates = registry.list_templates()
        if templates:
            first = templates[0]
            query = first.name.lower()[:3]
            results = registry.search(query)
            assert len(results) > 0

    def test_search_empty_query(self):
        """Test searching with empty query returns all templates."""
        registry = TemplateRegistry()
        results = registry.search("")
        assert len(results) == len(registry.list_templates())

    def test_clone_template(self):
        """Test cloning a template."""
        registry = TemplateRegistry()
        templates = registry.list_templates()
        assert len(templates) > 0

        first = templates[0]
        clone = registry.clone_template(first.id)
        assert clone is not None
        assert clone["template_id"] == first.id
        assert clone["name"].endswith("(Clone)")
        assert clone["id"] != first.id

    def test_clone_nonexistent(self):
        """Test cloning a non-existent template returns None."""
        registry = TemplateRegistry()
        assert registry.clone_template("non-existent") is None

    def test_custom_template_dir(self):
        """Test loading templates from a custom directory."""
        import tempfile

        with tempfile.TemporaryDirectory() as tmpdir:
            template_data = {
                "id": "test-template",
                "name": "Test Template",
                "description": "A test template",
                "category": "testing",
                "tags": ["test"],
                "type": "agent",
                "config": {"key": "value"},
                "metadata": {
                    "author": "tester",
                    "version": "2.0.0",
                    "rating": 4.5,
                    "clones": 5,
                    "created_at": "2024-01-01",
                    "updated_at": "2024-01-02",
                },
            }
            filepath = os.path.join(tmpdir, "test-template.json")
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(template_data, f)

            registry = TemplateRegistry(template_dir=tmpdir)
            template = registry.get_template("test-template")
            assert template is not None
            assert template.name == "Test Template"
            assert template.metadata.author == "tester"
            assert template.metadata.rating == 4.5
            assert template.metadata.clones == 5

    def test_template_to_dict(self):
        """Test template serialization to dict."""
        metadata = TemplateMetadata(
            author="test-author",
            version="1.0.0",
            rating=4.5,
            clones=10,
            created_at="2024-01-01",
            updated_at="2024-01-02",
        )
        template = AgentTemplate(
            id="test-id",
            name="Test",
            description="Test template",
            category="test",
            tags=["test"],
            type="agent",
            config={"foo": "bar"},
            metadata=metadata,
        )
        d = template.to_dict()
        assert d["id"] == "test-id"
        assert d["name"] == "Test"
        assert d["author"] == "test-author"
        assert d["rating"] == 4.5
        assert d["clones"] == 10
        assert d["config"] == {"foo": "bar"}
