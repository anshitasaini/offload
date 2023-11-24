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
from langchain.callbacks.base import BaseCallbackHandler
from langchain.callbacks import AsyncIteratorCallbackHandler
import json
import asyncio

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

class MyCallbackHandler(BaseCallbackHandler):
    def __init__(self, chat_query):
        self.chat_query = chat_query

    def on_new_token(self, token):
        self.chat_query.handle_llm_new_token(token)

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
        self.callback = AsyncIteratorCallbackHandler()
        self.streaming_llm = ChatOpenAI(client=None, model="gpt-3.5-turbo", temperature=0, streaming=True, callbacks=[self.callback])
        self.non_streaming_llm = ChatOpenAI(client=None, model="gpt-3.5-turbo", temperature=0, streaming=False)
        self.vectorstore = Pinecone.from_existing_index(
            index_name="langchain-index", embedding=self.embeddings, namespace=source_id
        )    
        self.qa = ConversationalRetrievalChain.from_llm(
            llm=self.streaming_llm,
            retriever=self.vectorstore.as_retriever(),
            return_source_documents=True,
        )    

    async def ask(self, query: str, history: list):
        task = asyncio.create_task(
                self.qa.acall(
                    {
                        "question": query,
                        "chat_history": history,
                    }
                )
            )

        try:
            async for token in self.callback.aiter():
                yield token
        except Exception as e:
            print(f"Caught exception: {e}")
        finally:
            self.callback.done.set()

        response = await task
        
        source_doc = (
            Document(page_content="", metadata={})
            if len(response["source_documents"]) == 0
            else response["source_documents"][0]
        )

        yield json.dumps({"type": "source_docs", "data": {"page_content": source_doc.page_content, "metadata": source_doc.metadata}})