from scrapy_crawler.scrapy_crawler.crawler import Crawler

crawler = Crawler()
crawler.spawn(start_urls=["https://docs.convex.dev/functions"])
crawler.run()
for item in crawler.scraped_items:
    print(item.get("title"))