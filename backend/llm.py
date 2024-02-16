from abc import ABC, abstractmethod
import logging
from langchain.prompts import PromptTemplate

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

import pinecone


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


REPHRASE_TEMPLATE = """\
Given the following conversation and a follow up question, rephrase the follow up \
question to be a standalone question.

Chat History:
{chat_history}
Follow Up Input: {question}
Standalone Question:"""

RESPONSE_TEMPLATE = """
You are an expert tasked with answering any questions about some documentation.
Generate a comprehensive, informative, yet concise answer based solely on the provide search results (URL and content). You must only use information from the provided search results. Use an unbiased and journalistic tone. Combine search results together into a coherent answer. Do not repeat text.\

Reply using properly formatted Markdown. Provide code snippets if relevant.\

If there is nothing in the context relevant to the question at hand, just say "Hmm, I'm not sure." Don't try to make up an answer. \

Anything between the following `context`  html blocks is retrieved from a knowledge \ bank, not part of the conversation with the user.

<context>
    {context}
<context/>


The question is: {question}
Answer:"""


class ChatQuery:
    def __init__(self, source_id: str) -> None:
        self.embeddings = OpenAIEmbeddings(
            client=None,
            model="text-embedding-ada-002",
        )
        self.callback = AsyncIteratorCallbackHandler()
        self.streaming_llm = ChatOpenAI(
            client=None,
            model="gpt-3.5-turbo",
            temperature=0,
            streaming=True,
            callbacks=[self.callback],
        )
        self.non_streaming_llm = ChatOpenAI(
            client=None, model="gpt-3.5-turbo", temperature=0, streaming=False
        )
        namespace = source_id if source_id != "convex" else "convex3"
        self.vectorstore = Pinecone.from_existing_index(
            index_name="langchain-index", embedding=self.embeddings, namespace=namespace
        )
        self.non_streaming_qa = ConversationalRetrievalChain.from_llm(
            llm=self.non_streaming_llm,
            retriever=self.vectorstore.as_retriever(search_kwargs={"k": 6}),
            verbose=True,
            combine_docs_chain_kwargs={
                "prompt": PromptTemplate.from_template(RESPONSE_TEMPLATE),
            },
        )
        self.qa = ConversationalRetrievalChain.from_llm(
            llm=self.streaming_llm,
            condense_question_llm=self.non_streaming_llm,
            retriever=self.vectorstore.as_retriever(search_kwargs={"k": 4}),
            verbose=True,
            combine_docs_chain_kwargs={
                "prompt": PromptTemplate.from_template(RESPONSE_TEMPLATE),
            },
        )

    def ask(self, query: str, history: list) -> str:
        result = self.non_streaming_qa(
            {
                "question": query,
                "chat_history": history,
            }
        )

        # source_doc = (
        #     Document(page_content="", metadata={})
        #     if len(result["source_documents"]) == 0
        #     else result["source_documents"][0]
        # )
        return result["answer"], None

    async def ask_stream(self, query: str, history: list):
        task = asyncio.create_task(
            self.qa.acall(
                {
                    "question": query,
                    "chat_history": history,
                },
                return_only_outputs=True,
            )
        )

        try:
            async for token in self.callback.aiter():
                token = token.replace("\n", "\\n")
                yield "data: " + token + "\n\n"
                # yield token
        except Exception as e:
            print(f"Caught exception: {e}")
        finally:
            self.callback.done.set()

        response = await task

        # source_doc = (
        #     Document(page_content="", metadata={})
        #     if len(response["source_documents"]) == 0
        #     else response["source_documents"][0]
        # )

        # yield json.dumps(
        #     {
        #         "type": "source_docs",
        #         "data": {
        #             "page_content": source_doc.page_content,
        #             "metadata": source_doc.metadata,
        #         },
        #     }
        # )
