from celery_app import app

@app.task(name="crawl_website")
def crawl_website(url: str) -> str:
    """ Task to crawl a website """
    print(f"Crawling {url}")
    return f"Crawling {url}"