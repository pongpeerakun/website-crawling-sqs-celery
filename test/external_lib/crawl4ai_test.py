import pytest
from crawl4ai import AsyncWebCrawler

pytest_plugins = ("pytest_asyncio",)


@pytest.mark.asyncio
async def test_simple():
    title = ""
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url="https://example.com/",
        )
        title = result.metadata.get("title")
    
    assert title == "Example Domain"
        