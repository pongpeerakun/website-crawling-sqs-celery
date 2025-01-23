from celery_app import app
from assistric_kownledge_base.crawler import crawl_target_website
from assistric_kownledge_base.scraper import scrape_target_website
from assistric_kownledge_base.libs.aws import AwsSdk
from assistric_kownledge_base.libs.chroma import ChromaClient
from assistric_kownledge_base.models.scraping_website import ScrapingWebsite
import asyncio
import json

@app.task(name="crawl_website")
def crawl_website(knowledge_base_id: str, url: str) -> str:
    """ Task to crawl a website """
    results = crawl_target_website(url, max_pages=1000)
    message = {
        "action": "CRAWL_WEBSITE",
        "knowledge_base_id": knowledge_base_id
    }
    # AwsSdk.publish_sns_message("Crawling task completed", message)
    return f"Crawling {len(results)} pages"

@app.task(name="scrape_website")
def scrape_website(knowledge_bases: list[ScrapingWebsite]) -> str:
    """ Function to scrape a website """

    if not isinstance(knowledge_bases, list):
        return "URL must be a list of strings"
    
    if len(knowledge_bases) > 10:
        return "Maximum of 10 URLs can be scraped at a time"

    chromaDb = ChromaClient()

    documents = asyncio.run(scrape_target_website(knowledge_bases))
    # for kb in knowledge_bases:
    if documents and len(documents) > 0:
        chromaDb.add_documents(documents)
        knowledge_base_ids = [kb["id"] for kb in knowledge_bases]
        message = {
            "action": "SCRAPE_WEBSITE",
            "knowledge_base_ids": knowledge_base_ids
        }
        AwsSdk.publish_sns_message("Scraping task completed", message)

    return "Crawling task submitted successfully"