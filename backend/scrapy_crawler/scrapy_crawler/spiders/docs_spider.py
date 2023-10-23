from pathlib import Path

import scrapy
from bs4 import BeautifulSoup
from w3lib.url import url_query_cleaner
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from w3lib.url import url_query_cleaner

def process_links(links):
    for link in links:
        link.url = url_query_cleaner(link.url)
        yield link

class DocsSpider(CrawlSpider):
    name = "docs"
    allowed_domains = ["docs.convex.dev"]
    start_urls = [
        "https://docs.convex.dev/functions",
    ]
    rules = (
        Rule(
            LinkExtractor(
                deny=[],
            ), 
            process_links=process_links,
            callback='parse',
            follow=True
        ),
    )

    def parse(self, response):
        html = response.body.decode("utf-8")
        soup = BeautifulSoup(html, "html.parser")
        item = {
            'url': response.url,
            'title': soup.title.string,
            'text': soup.get_text().strip(),
        }
        yield self.output_callback(item)
        # yield soup.get_text().strip()