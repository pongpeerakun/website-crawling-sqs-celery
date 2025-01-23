from crawl4ai import AsyncWebCrawler, CrawlerRunConfig
from langchain_text_splitters import MarkdownHeaderTextSplitter
from langchain_core.documents.base import Document
from assistric_kownledge_base.models.scraping_website import ScrapingWebsite


async def scrape_target_website(knowledge_bases: list[ScrapingWebsite]) -> list[Document]:
    """
    Scrape a website using a Celery task.

    Args:
        knowledge_bases (list[ScrapingWebsite]): A list of ScrapingWebsite objects.

    Returns:
        str: A message indicating the task was submitted successfully.
    """

    config = CrawlerRunConfig(
        excluded_tags=["nav", "footer"],
        exclude_external_links=True,
        exclude_social_media_links=True,
        exclude_external_images=True,
        wait_for_images=False
    )

    headers_to_split_on = [
        ("#", "Header 1"),
        ("##", "Header 2"),
        ("###", "Header 3"),
    ]
    markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on)
    documents: list[Document] = []
    # Create an instance of AsyncWebCrawler
    async with AsyncWebCrawler() as crawler:
        for kb in knowledge_bases:
            # Run the crawler on a URL
            url = kb["url"]
            result = await crawler.arun(url=url, config=config)
            md_header_splits = markdown_splitter.split_text(result.markdown)
            for md in md_header_splits:
                md.metadata["website"] = url
                md.metadata["linkId"] = kb["id"]
            documents += md_header_splits
        
    return documents