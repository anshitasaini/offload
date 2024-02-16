import openai
import requests
from bs4 import BeautifulSoup
import html2text
import os
import pinecone
from langchain.embeddings import OpenAIEmbeddings

from langchain.text_splitter import RecursiveCharacterTextSplitter, Language
from langchain.vectorstores import Pinecone
from dotenv import load_dotenv

load_dotenv()


# Fetch the sitemap
sitemap_url = "https://docs.convex.dev/sitemap.xml"
response = requests.get(sitemap_url)

# Parse the sitemap
soup = BeautifulSoup(response.content, "lxml")

# Find all URLs in the sitemap
urls = [element.text for element in soup.findAll("loc")]

md_splitter = RecursiveCharacterTextSplitter.from_language(
    language=Language.MARKDOWN, chunk_size=800, chunk_overlap=100
)

openai.api_key = os.getenv("OPENAI_API_KEY")
model_name = "text-embedding-ada-002"

index_name = "langchain-index"
pinecone.init(
    api_key=os.getenv("PINECONE_API_KEY"), environment=os.getenv("PINECONE_ENV")  # type: ignore
)

# Initialize the HTML to Markdown converter
converter = html2text.HTML2Text()
converter.ignore_links = True

# Crawl each URL
for url in urls:
    response = requests.get(url)
    html = response.text

    soup = BeautifulSoup(html, "lxml")
    title = soup.title.string if soup.title else "Convex Docs"

    # Convert HTML to Markdown
    markdown = converter.handle(html)
    sections = md_splitter.create_documents(
        [markdown],
        [
            {
                "url": url,
                "title": title,
            }
        ],
    )

    embeddings = OpenAIEmbeddings(
        client=None,
        model="text-embedding-ada-002",
    )

    Pinecone.from_documents(
        documents=sections,
        embedding=embeddings,
        index_name="langchain-index",
        namespace="convex3",
    )
