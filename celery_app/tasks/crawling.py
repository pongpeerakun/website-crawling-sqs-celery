from celery_app import app
from assistric_kownledge_base.crawler import crawl_target_website
from assistric_kownledge_base.scraper import scrape_target_website
from assistric_kownledge_base.libs.aws import AwsSdk
from assistric_kownledge_base.libs.chroma import ChromaClient
import asyncio

@app.task(name="crawl_website")
def crawl_website(knowledge_base_id: str, url: str) -> str:
    """ Task to crawl a website """
    results = crawl_target_website(url, max_pages=30)
    message = {
        "action": "CRAWL_WEBSITE",
        "knowledge_base_id": knowledge_base_id
    }
    AwsSdk.publish_sns_message("Crawling task completed", message)
    return f"Crawling {len(results)} pages"

@app.task(name="scrap_website")
def scrap_website(knowledge_base_id: str, url: list[str]) -> str:
    """ Function to scrape a website """
    if not url:
        return "No URL provided"
    
    if not isinstance(url, list):
        return "URL must be a list of strings"
    
    if len(url) > 10:
        return "Maximum of 10 URLs can be scraped at a time"

    documents = asyncio.run(scrape_target_website(url))
    if len(documents) == 0:
        return "No documents found"
    
    chromaDb = ChromaClient()
    chromaDb.add_documents(documents)

    message = {
        "action": "SCRAP_WEBSITE",
        "knowledge_base_id": knowledge_base_id
    }
    AwsSdk.publish_sns_message("Scraping task completed", message)
    return "Crawling task submitted successfully"