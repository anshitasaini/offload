from abc import ABC, abstractmethod
import logging

from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Pinecone
from langchain.schema import Document
import openai
from crawler_driver import CrawlerDriver


class AbstractUploadSource(ABC):
    def __init__(self) -> None:
        openai.util.logger.setLevel(logging.WARNING)
        self.embeddings = OpenAIEmbeddings(
            client=None,
            model="text-embedding-ada-002",
        )
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=400,
            chunk_overlap=20,
            length_function=len,
            separators=["\n\n", "\n", " ", ""],
        )
        self.source_id: str | None = None

    def ingest(self) -> str:
        if self.source_id is None:
            raise ValueError("Source ID is None")
        split_documents = self.create_documents()

        print("Uploading documents to Pinecone...")
        print(f"Uploading {len(split_documents)} documents")
        print(f"Source ID: {self.source_id}")
        Pinecone.from_documents(
            documents=split_documents,
            embedding=self.embeddings,
            index_name="langchain-index",
            namespace=self.source_id,
            environment="us-west1-gcp-free",
        )
        return self.source_id

    @abstractmethod
    def create_documents(self) -> list[Document]:
        pass


class DocsUploadSource(AbstractUploadSource):
    def __init__(self, url: str, source_id: str) -> None:
        super().__init__()
        self.base_url = url
        self.source_id = source_id

    def fetch_contents(self, base_url):
        crawler = CrawlerDriver(base_url)
        scraped_items = crawler.get_scraped_items()
        docs_data = [[], []]
        for item in scraped_items:
            docs_data[0].append(item.content)
            docs_data[1].append({"page_title": item.title, "page_url": item.url})
        return docs_data

    def create_documents(self) -> list[Document]:
        docs_data = self.fetch_contents(self.base_url)
        return self.text_splitter.create_documents(
            texts=docs_data[0], metadatas=docs_data[1]
        )


class ChatQuery:
    def __init__(self, source_id: str) -> None:
        self.embeddings = OpenAIEmbeddings(
            client=None,
            model="text-embedding-ada-002",
        )
        self.llm = ChatOpenAI(client=None, model="gpt-3.5-turbo", temperature=0)
        self.vectorstore = Pinecone.from_existing_index(
            index_name="langchain-index", embedding=self.embeddings, namespace=source_id
        )
        self.qa = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.vectorstore.as_retriever(),
            return_source_documents=True,
        )

    def ask(self, query: str, history: list) -> str:
        result = self.qa(
            {
                "question": query,
                "chat_history": history,
            }
        )

        source_doc = (
            Document(page_content="", metadata={})
            if len(result["source_documents"]) == 0
            else result["source_documents"][0]
        )
        return result["answer"], source_doc
