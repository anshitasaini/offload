from scrapy_crawler.scrapy_crawler.crawler import Crawler
from celery import Celery

# app = Celery("tasks", backend="redis://localhost", broker="redis://localhost")
# app.conf.broker_url = "redis://localhost:6379/0"
# crawler = Crawler()


class CrawledPage:
    def __init__(self, title, url, content):
        self.title = title
        self.url = url
        self.content = content


class CrawlerDriver:
    def __init__(self, start_url):
        self.crawler = Crawler()
        self.crawler.spawn(start_urls=[start_url], base_url=start_url)
        self.crawler.run()

    def get_scraped_items(self):
        return [
            CrawledPage(item.get("title"), item.get("url"), item.get("text"))
            for item in self.crawler.scraped_items
        ]
