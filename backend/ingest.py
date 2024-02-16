import asyncio
from sqlalchemy.orm import Session
import models
import aiohttp
from bs4 import BeautifulSoup
from pydantic import BaseModel
from xml.etree import ElementTree as ET


class PageDetails(BaseModel):
    url: str
    title: str
    content: str


async def fetch_sitemap_urls(sitemap_url: str) -> list[str]:
    async with aiohttp.ClientSession() as session:
        async with session.get(sitemap_url) as response:
            text = await response.text()
            soup = BeautifulSoup(text, "xml")
            return [loc.get_text(strip=True) for loc in soup.find_all("loc")]


async def fetch_page_details(url: str) -> PageDetails:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            text = await response.text()
            soup = BeautifulSoup(text, "html.parser")
            title = soup.find("title").get_text(strip=True)
            content = soup.get_text()
            return PageDetails(url=url, title=title, content=content)


async def crawl_and_store_sitemap(sitemap_url: str, source_name: str, db: Session):
    urls = await fetch_sitemap_urls(sitemap_url)
    responses: list[PageDetails] = await asyncio.gather(
        *[fetch_page_details(url) for url in urls]
    )

    source = models.Source(
        type=models.sourceTypeEnum.website,
        data={"sitemapUrl": sitemap_url},
        name=source_name,
    )
    db.add(source)
    db.commit()
    db.refresh(source)

    # Batch add files
    batch_size = 100
    files = [
        models.File(
            title=response.title,
            raw_content=response.content,
            markdown=response.content,
            source_id=source.id,
        )
        for response in responses
    ]
    for i in range(0, len(files), batch_size):
        db.add_all(files[i : i + batch_size])
        db.commit()

    db.refresh(source)

    return source
