from scrapy_crawler.scrapy_crawler.crawler import Crawler

from cel.tasks import app
from celery.result import AsyncResult

class CrawledPage:
    def __init__(self, title, content):
        self.title = title
        self.content = content

class CrawlerDriver:
    def __init__(self, start_url):
        self.crawler = Crawler()
        self.crawler.spawn(start_urls=[start_url])
        self.crawler.run()
        
    def get_scraped_items(self):
        for item in self.crawler.scraped_items:
            print(item.get("title"))
        return [CrawledPage(item.get("title"), item.get("content")) for item in self.crawler.scraped_items]