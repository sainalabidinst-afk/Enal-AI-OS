"""
Tests for Browser Agent
======================
Tests for web browsing, data extraction, and API interaction.
"""

import pytest


class TestBrowserAgent:
    """Tests for BrowserAgent."""

    @pytest.mark.asyncio
    async def test_browse_stub(self):
        from backend.app.core.browser_agent import BrowserAgent
        agent = BrowserAgent()
        result = await agent.browse("https://httpbin.org/html")
        assert result.url == "https://httpbin.org/html"
        assert result.evidence_score >= 0

    def test_parse_html(self):
        from backend.app.core.browser_agent import BrowserAgent
        agent = BrowserAgent()
        html = '<html><head><title>Test Page</title></head><body><p>Hello</p><a href="https://example.com">Link</a></body></html>'
        result = agent._parse_html("https://test.com", html)
        assert result.title == "Test Page"
        assert "https://example.com" in result.links

    @pytest.mark.asyncio
    async def test_extract_evidence(self):
        from backend.app.core.browser_agent import BrowserAgent
        agent = BrowserAgent()
        result = await agent.extract_evidence("https://example.com")
        assert "url" in result
        assert "citation" in result

    def test_search_history(self):
        from backend.app.core.browser_agent import BrowserAgent
        agent = BrowserAgent()
        assert isinstance(agent._search_history, list)


class TestBrowserAgentAPI:
    """Tests for API interaction."""

    @pytest.mark.asyncio
    async def test_call_api_stub(self):
        from backend.app.core.browser_agent import BrowserAgent
        agent = BrowserAgent()
        result = await agent.call_api("https://httpbin.org/get")
        assert result is not None