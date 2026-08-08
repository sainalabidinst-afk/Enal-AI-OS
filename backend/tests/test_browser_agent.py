import pytest

from backend.app.core.browser_agent import BrowserAgent, BrowserResult


class FakeResponse:
    def __init__(self, text, content_type="text/html"):
        self._text = text
        self.content_type = content_type

    async def text(self):
        return self._text

    async def json(self):
        return {"key": "value"}

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass


class FakeSession:
    def __init__(self, response):
        self._response = response
        self.closed = False

    def get(self, url, **kwargs):
        return _AsyncCM(self._response)

    def post(self, url, **kwargs):
        return _AsyncCM(self._response)

    async def close(self):
        self.closed = True


class _AsyncCM:
    def __init__(self, response):
        self._response = response

    async def __aenter__(self):
        return self._response

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass


class TestBrowserResult:
    def test_defaults(self):
        result = BrowserResult(url="http://example.com", title="Example", content="hello")
        assert result.links == []
        assert result.images == []
        assert result.metadata == {}
        assert result.evidence_score == 0.5
        assert result.fetched_at is not None


class TestBrowserAgent:
    @pytest.mark.asyncio
    async def test_browse_stub_without_session(self, monkeypatch):
        import backend.app.core.browser_agent as ba_module

        async def fake_ensure(self):
            self.session = None

        monkeypatch.setattr(ba_module.BrowserAgent, "_ensure_session", fake_ensure)
        agent = BrowserAgent()
        result = await agent.browse("http://example.com")
        assert result.title == "Stub"
        assert result.content == "Browser not available"

    @pytest.mark.asyncio
    async def test_browse_blocks_private_ips(self, monkeypatch):
        import backend.app.core.browser_agent as ba_module

        class FakeSession:
            pass

        async def fake_ensure(self):
            self.session = FakeSession()

        monkeypatch.setattr(ba_module.BrowserAgent, "_ensure_session", fake_ensure)
        agent = BrowserAgent()
        result = await agent.browse("http://127.0.0.1/test")
        assert result.title == "Blocked"
        assert result.content == "SSRF blocked"
        assert result.evidence_score == 0.0

    @pytest.mark.asyncio
    async def test_browse_parses_html(self, monkeypatch):
        import backend.app.core.browser_agent as ba_module

        html = "<html><head><title>Test Page</title></head><body><a href='http://example.com'>link</a><img src='http://img.com/x.png'/></body></html>"
        response = FakeResponse(html)

        async def fake_ensure(self):
            self.session = FakeSession(response)

        monkeypatch.setattr(ba_module.BrowserAgent, "_ensure_session", fake_ensure)
        agent = BrowserAgent()
        result = await agent.browse("http://example.com")
        assert result.title == "Test Page"
        assert "http://example.com" in result.links

    @pytest.mark.asyncio
    async def test_search_returns_results(self, monkeypatch):
        import backend.app.core.browser_agent as ba_module

        html = "<html><body>http://result1.com http://result2.com</body></html>"
        response = FakeResponse(html)

        async def fake_ensure(self):
            self.session = FakeSession(response)

        monkeypatch.setattr(ba_module.BrowserAgent, "_ensure_session", fake_ensure)
        agent = BrowserAgent()
        results = await agent.search("query")
        assert len(results) <= 5

    @pytest.mark.asyncio
    async def test_extract_evidence_returns_dict(self, monkeypatch):
        import backend.app.core.browser_agent as ba_module

        html = "<html><head><title>T</title></head><body>content</body></html>"
        response = FakeResponse(html)

        async def fake_ensure(self):
            self.session = FakeSession(response)

        monkeypatch.setattr(ba_module.BrowserAgent, "_ensure_session", fake_ensure)
        agent = BrowserAgent()
        evidence = await agent.extract_evidence("http://example.com")
        assert "url" in evidence
        assert "citation" in evidence
        assert "evidence_score" in evidence

    @pytest.mark.asyncio
    async def test_call_api_get_returns_json(self, monkeypatch):
        import backend.app.core.browser_agent as ba_module

        response = FakeResponse('{"key": "value"}', content_type="application/json")

        async def fake_ensure(self):
            self.session = FakeSession(response)

        monkeypatch.setattr(ba_module.BrowserAgent, "_ensure_session", fake_ensure)
        agent = BrowserAgent()
        result = await agent.call_api("http://api.example.com/data")
        assert result == {"key": "value"}

    @pytest.mark.asyncio
    async def test_call_api_post_returns_json(self, monkeypatch):
        import backend.app.core.browser_agent as ba_module

        response = FakeResponse('{"key": "value"}', content_type="application/json")

        async def fake_ensure(self):
            self.session = FakeSession(response)

        monkeypatch.setattr(ba_module.BrowserAgent, "_ensure_session", fake_ensure)
        agent = BrowserAgent()
        result = await agent.call_api("http://api.example.com/data", method="POST", data={"x": 1})
        assert result == {"key": "value"}
