import json
from urllib.parse import urlparse
from pydantic import BaseModel
from llm import DocsUploadSource
import os
import pinecone

class DocToCrawl(BaseModel):
    name: str
    crawlerStart: str

    @property
    def source_id(self) -> str:
        return self.name.lower().replace(" ", "-")

    @property
    def netloc(self) -> str:
        parsed_uri = urlparse(self.crawlerStart)
        return parsed_uri.netloc


def read_json_docs() -> list[DocToCrawl]:
    with open("docs.jsonl", "r") as f:
        lines = f.readlines()
        docs_to_crawl = [DocToCrawl(**json.loads(line)) for line in lines]
        return docs_to_crawl


def do_it():
    docs_to_crawl = read_json_docs()
    # temporary filter
    docs_to_crawl = [doc for doc in docs_to_crawl if doc.name not in ["React", "Convex", "CodeMirror"]]

    upload_sources = [
        DocsUploadSource(doc.crawlerStart, doc.source_id) for doc in docs_to_crawl
    ]

    for source in upload_sources:
        source.ingest()


if __name__ == "__main__":
    pinecone.init(
    api_key=os.getenv("PINECONE_API_KEY"), environment=os.getenv("PINECONE_ENV")
    )
    do_it()
