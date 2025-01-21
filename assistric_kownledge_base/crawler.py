from scrapy.crawler import CrawlerRunner
from assistric_kownledge_base.spider import WebsiteSpider
from multiprocessing import Queue
from twisted.internet import reactor
from scrapy import signals
from scrapy.signalmanager import dispatcher
from billiard.context import Process
from assistric_kownledge_base.models.crawler_result import CrawlerResult
from crawl4ai import AsyncWebCrawler


def run_crawler(url, max_pages, q):
    """
    Run the Scrapy crawler in a separate process.

    Args:
        url (str): The website URL to crawl.
        max_pages (int): Maximum number of pages to crawl.
        q (multiprocessing.Queue): Queue to collect results or exceptions.
    """

    try:
        # 1. Define crawler runner
        runner = CrawlerRunner()
        results = []
        def crawler_results(signal, sender, item, response, spider):
            results.append(item)

        dispatcher.connect(crawler_results, signal=signals.item_scraped)
        deferred = runner.crawl(
            WebsiteSpider,
            url=url,
            max_pages=max_pages
        )
        deferred.addBoth(lambda _: reactor.stop())
        reactor.run()  # This will block until the reactor stops
        q.put(results)
    except Exception as e:
        q.put(e)

def crawl_target_website(url, max_pages=10) -> list[CrawlerResult]:
    """
    Crawl a website programmatically and optionally save results to a file.

    Args:
        url (str): The website URL to crawl.
        max_pages (int): Maximum number of pages to crawl.

    Returns:
        list: List of dictionaries containing crawled data.
    """
    q = Queue()
    p = Process(target=run_crawler, args=(url, max_pages, q))
    p.start()
    results = q.get()
    p.join()

    if isinstance(results, Exception):
        raise results  # Re-raise the exception if one occurred in the process
    
    urls = [ CrawlerResult(url=r['url']) for r in results ]
    return urls

async def scrape_target_website(url: str):
    """
    Scrape a website using a Celery task.

    Args:
        url (str): The website URL to scrape.

    Returns:
        str: A message indicating the task was submitted successfully.
    """
    # Create an instance of AsyncWebCrawler
    async with AsyncWebCrawler() as crawler:
        # Run the crawler on a URL
        result = await crawler.arun(url=url)

        # Print the extracted content
        return result.markdown
    
    return "Crawling task submitted successfully"