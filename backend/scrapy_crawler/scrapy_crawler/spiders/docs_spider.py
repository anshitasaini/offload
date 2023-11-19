import logging
from pathlib import Path
from urllib.parse import urlparse

import scrapy
from bs4 import BeautifulSoup
from w3lib.url import url_query_cleaner
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from w3lib.url import url_query_cleaner
from dotenv import load_dotenv

load_dotenv()
import sys

def process_links(links):
    for link in links:
        link.url = url_query_cleaner(link.url)
        yield link


class DocsSpider(CrawlSpider):
    name = "docs"

    def __init__(self, base_url, *args, **kwargs):
        super().__init__(*args, **kwargs)
        logging.getLogger('scrapy').setLevel(logging.WARNING)
        parsed_uri = urlparse(base_url)

        self.allowed_domains = [parsed_uri.netloc]
        self.start_urls = [base_url]
        self.base_path = parsed_uri.path

        print(f"Starting crawl on {base_url}")
        print(f"Allowed domains: {self.allowed_domains}")
        print(f"Basing crawl on path: {self.base_path}")
        # exit()

        self.rules = (
            Rule(
                LinkExtractor(
                    # allow=self.base_path,
                ),
                process_links=process_links,
                callback="parse",
                follow=True,
            ),
        )

        super()._compile_rules()

    def parse(self, response):
        html = response.body.decode("utf-8")
        soup = BeautifulSoup(html, "html.parser")
        item = {
            "url": response.url,
            "title": soup.title.string,
            "text": soup.get_text().strip(),
        }
        yield self.output_callback(item)
