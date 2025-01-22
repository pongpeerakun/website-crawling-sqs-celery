from crawl4ai import AsyncWebCrawler, CrawlerRunConfig
from langchain_text_splitters import MarkdownHeaderTextSplitter
from dotenv import load_dotenv
from langchain_core.documents.base import Document
import os

load_dotenv()

async def scrape_target_website(urls: list[str]) -> list[Document]:
    """
    Scrape a website using a Celery task.

    Args:
        url (list): A list of URLs to scrape.

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
        
        for url in urls:
            # Run the crawler on a URL
            result = await crawler.arun(url=url, config=config)
            print(result.markdown)
            md_header_splits = markdown_splitter.split_text(result.markdown)
            for md in md_header_splits:
                md.metadata["website"] = url

            documents += md_header_splits
        
    return documents