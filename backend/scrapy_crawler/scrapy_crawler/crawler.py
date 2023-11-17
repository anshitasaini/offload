from scrapy.crawler import CrawlerProcess
from .spiders.docs_spider import DocsSpider

class Crawler:
    def __init__(self):
        self.process = CrawlerProcess()
        self.scraped_items = []

    def process_item(self, item):
        self.scraped_items.append(item)
        return item

    def spawn(self, **kwargs):
        self.process.crawl(DocsSpider, output_callback=self.process_item, **kwargs)

    def run(self):
        self.process.start()
