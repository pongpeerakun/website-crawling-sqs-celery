from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import CloseSpider
from urllib.parse import urlparse

class WebsiteSpider(CrawlSpider):
    name = 'website_spider'
    
    def __init__(self, url=None, max_pages=100, *args, **kwargs):
        super(WebsiteSpider, self).__init__(*args, **kwargs)
        # Set the start URL and allowed domains
        if url:
            self.start_urls = [url]
            parsed_uri = urlparse(url)
            self.allowed_domains = [parsed_uri.netloc]
            
        self.max_pages = int(max_pages)
        self.pages_crawled = 0
        
        # Define the link extraction rules
        self.rules = (
            Rule(
                LinkExtractor(
                    deny=('\.(pdf|jpg|jpeg|png|gif|doc|docx|xls|xlsx|zip|rar|txt)$',),
                    unique=True
                ),
                callback='parse_page',
                follow=True
            ),
        )
        
        super(WebsiteSpider, self)._compile_rules()

    def parse_page(self, response):
        """Parse each page and extract links."""

        self.pages_crawled += 1
        
        if self.pages_crawled > self.max_pages:
            raise CloseSpider('Reached maximum number of pages')
        
        # Extract all links from the page
        # all_links = response.css('a::attr(href)').getall()
        return {
            'url': response.url,
            # 'title': response.css('title::text').get(),
            # 'links': all_links
        }