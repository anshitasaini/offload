from scrapy_crawler.scrapy_crawler.crawler import Crawler
from celery import Celery

app = Celery("tasks", backend='redis://localhost',broker="redis://localhost")
app.conf.broker_url = 'redis://localhost:6379/0'
crawler = Crawler()

class CrawledPage:
    def __init__(self, title, url, content):
        self.title = title
        self.url = url 
        self.content = content

@app.task
def start_task(start_url):
    # crawler = Crawler()
    crawler.spawn(start_urls=[start_url])
    crawler.run()
    return crawler.scraped_items     

class CrawlerDriver:
    def __init__(self, start_url):
        self.start_url = start_url
        result = start_task.delay(start_url)
        while not result.ready():
            pass
        print("Done")
        self.scraped_items = result.get()
        
    def get_scraped_items(self):
        return [CrawledPage(item.get("title"), item.get("url"), item.get("text")) for item in self.scraped_items]