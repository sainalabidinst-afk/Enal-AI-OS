"""
Browser Agent
=============

Provides web browsing, data extraction, and API interaction capabilities.

Uses: aiohttp for HTTP requests, BeautifulSoup-like parsing for content extraction.
"""

import logging
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any
from urllib.parse import urlparse

logger = logging.getLogger(__name__)


@dataclass
class BrowserResult:
    url: str
    title: str
    content: str
    links: list[str] = field(default_factory=list)
    images: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    fetched_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    evidence_score: float = 0.5


class BrowserAgent:
    def __init__(self):
        self.session = None
        self._search_history: list[dict] = []

    async def _ensure_session(self):
        if self.session is None:
            try:
                import aiohttp
                self.session = aiohttp.ClientSession(
                    timeout=aiohttp.ClientTimeout(total=30),
                    headers={"User-Agent": "Mozilla/5.0 (compatible; ECP-Bot/1.0)"},
                )
            except ImportError:
                logger.warning("aiohttp not installed, browser agent will use stub mode")

    async def browse(self, url: str) -> BrowserResult:
        await self._ensure_session()
        if self.session is None:
            return BrowserResult(url=url, title="Stub", content="Browser not available", evidence_score=0.3)

        parsed = urlparse(url)
        hostname = parsed.hostname or ""
        blocked_hosts = {"127.0.0.1", "localhost", "0.0.0.0", "169.254.169.254", "[::1]"}
        if hostname.lower() in blocked_hosts or hostname.startswith("10.") or hostname.startswith("192.168.") or hostname.startswith("172."):
            return BrowserResult(url=url, title="Blocked", content="SSRF blocked", evidence_score=0.0)

        try:
            async with self.session.get(url) as response:
                html = await response.text()
                return self._parse_html(url, html)
        except Exception as e:
            logger.error(f"Browse failed for {url}: {e}")
            return BrowserResult(url=url, title="Error", content=f"Error: {e}", evidence_score=0.1)

    def _parse_html(self, url: str, html: str) -> BrowserResult:
        title = ""
        content = ""
        links = []
        images = []

        # Simple HTML parsing without BeautifulSoup
        import re
        for line in html.split("\n"):
            if "<title>" in line:
                match = re.search(r"<title>(.*?)</title>", line, re.IGNORECASE)
                if match:
                    title = match.group(1).strip()
            if 'href="' in line or "href='" in line:
                match = re.search(r'href=["\']([^"\']+)["\']', line)
                if match:
                    href = match.group(1)
                    if href.startswith("http"):
                        links.append(href)
            if "<img" in line:
                match = re.search(r'src=["\']([^"\']+)["\']', line)
                if match and match.group(1).startswith("http"):
                    images.append(match.group(1))

        # Extract text content (basic)
        import re
        text = re.sub(r"<script[^>]*>.*?</script>", "", html, flags=re.DOTALL | re.IGNORECASE)
        text = re.sub(r"<style[^>]*>.*?</style>", "", text, flags=re.DOTALL | re.IGNORECASE)
        text = re.sub(r"<[^>]+>", " ", text)
        content = " ".join(text.split())[:5000]

        return BrowserResult(
            url=url,
            title=title or urlparse(url).netloc,
            content=content,
            links=links[:50],
            images=images[:20],
        )

    async def search(self, query: str, max_results: int = 5) -> list[dict[str, Any]]:
        await self._ensure_session()
        results = []

        # Try DuckDuckGo HTML search
        search_url = f"https://html.duckduckgo.com/html/?q={query}"
        result = await self.browse(search_url)
        if result.content:
            import re
            # Extract result URLs from DuckDuckGo
            urls = re.findall(r'https?://[^\s"\'<>]+\.[^\s"\'<>]+', result.content)
            for url in urls[:max_results]:
                if "duckduckgo" not in url.lower():
                    results.append({
                        "url": url,
                        "title": url,
                        "snippet": url,
                        "source": "duckduckgo",
                    })

        self._search_history.append({"query": query, "results": len(results)})
        return results

    async def extract_evidence(self, url: str) -> dict[str, Any]:
        result = await self.browse(url)
        return {
            "url": result.url,
            "title": result.title,
            "content": result.content,
            "citation": f"Retrieved from {url} on {result.fetched_at.isoformat()}",
            "evidence_score": result.evidence_score,
        }

    async def compare_and_summarize(self, sources: list[str]) -> dict[str, Any]:
        results = []
        for url in sources:
            result = await self.browse(url)
            results.append({
                "url": result.url,
                "title": result.title,
                "content": result.content[:1000],
            })

        # Basic summarization
        all_content = " ".join(r["content"] for r in results)
        summary = all_content[:2000] + "..." if len(all_content) > 2000 else all_content

        return {
            "sources": [r["url"] for r in results],
            "summary": summary,
            "citations": [f"Source: {r['url']}" for r in results],
        }

    async def call_api(self, endpoint: str, method: str = "GET", data: dict | None = None) -> Any:
        await self._ensure_session()
        if self.session is None:
            return {"error": "Browser not available"}

        try:
            if method.upper() == "GET":
                async with self.session.get(endpoint, params=data) as response:
                    return await response.json() if "json" in response.content_type else await response.text()
            else:
                async with self.session.post(endpoint, json=data) as response:
                    return await response.json() if "json" in response.content_type else await response.text()
        except Exception as e:
            return {"error": str(e)}


browser_agent = BrowserAgent()
