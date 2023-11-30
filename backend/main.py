import asyncio
from llm import ChatQuery
from urllib.parse import urlparse
import openai
import os
import pinecone
import requests
from typing import AsyncIterable, Union
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
from langchain.callbacks import AsyncIteratorCallbackHandler
from dotenv import load_dotenv
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from llm import ChatQuery
from uuid import uuid4
from fastapi.routing import APIRoute

load_dotenv()


def custom_generate_unique_id(route: APIRoute):
    return f"{route.tags[0]}-{route.name}"


app = FastAPI(
    generate_unique_id_function=custom_generate_unique_id,
    servers=[{"url": "http://127.0.0.1:8000", "description": "Local dev server"}],
)

origins = [
    "http://localhost:3000",
    "http://localhost:3001",
    "http://localhost:3001/chat/",
    "http://localhost:3001/chat/code/",
    "http://localhost:1420",
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

openai.api_key = os.getenv("OPENAI_API_KEY")
model_name = "text-embedding-ada-002"

index_name = "langchain-index"
pinecone.init(
    api_key=os.getenv("PINECONE_API_KEY"), environment=os.getenv("PINECONE_ENV")  # type: ignore
)


def initialize_db_if_needed():
    if index_name not in pinecone.list_indexes():
        pinecone.create_index(name=index_name, metric="dotproduct", dimension=1536)


class ChatMessageSchema(BaseModel):
    message: str
    sender: str


class ChatInSchema(BaseModel):
    query: str
    current_url: str
    history: list[ChatMessageSchema]


class ChatResponse(BaseModel):
    answer: str
    source_content: str
    source_metadata: dict


from crawl import read_json_docs

docs_to_crawl = read_json_docs()
url_to_doc = {doc.netloc: doc for doc in docs_to_crawl}
    
@app.post("/chat/", tags=["chat"], response_model=ChatResponse)
def send_message(chat_in: ChatInSchema):
    current_netloc = urlparse(chat_in.current_url).netloc
    try:
        doc = url_to_doc[current_netloc]
    except KeyError:
        return ChatResponse(
            answer="Sorry, I don't know anything about this document.",
            source_content="",
            source_metadata={},
        )

    print(doc)
    source_id = doc.source_id
    history = chat_in.history
    query_obj = ChatQuery(source_id)
    chat_history = [
        (history[i].message, history[i + 1].message)
        for i in range(1, len(history) - 1, 2)
    ]
    answer, source = query_obj.ask(chat_in.query, chat_history)
    return ChatResponse(
        answer=answer,
        source_content=source.page_content,
        source_metadata=source.metadata,
    )


@app.post("/chat-stream/", tags=["chat"], response_model=None)
async def send_message_stream(chat_in: ChatInSchema):
    print(chat_in.query)
    
    current_netloc = urlparse(chat_in.current_url).netloc
    try:
        doc = url_to_doc[current_netloc]
    except KeyError:
        def empty_generator():
            yield
        return StreamingResponse(empty_generator(), media_type="text/event-stream")

    history = chat_in.history
    chat_history = [
        (history[i].message, history[i + 1].message)
        for i in range(1, len(history) - 1, 2)
    ]
    
    query_obj = ChatQuery(doc.source_id)
    generator = query_obj.ask_stream(chat_in.query, chat_history)
    return StreamingResponse(generator, media_type="text/event-stream")


class GetSourceRequest(BaseModel):
    url: str


class GetSourceResponse(BaseModel):
    source_id: str | None


@app.post("/source/", response_model=GetSourceResponse, tags=["source"])
def get_source(get_source_request: GetSourceRequest):
    url = get_source_request.url
    doc = url_to_doc.get(url, None)
    source_id = doc.source_id if doc else None
    return GetSourceResponse(source_id=source_id)


@app.get("/", tags=["root"])
async def main():
    return {"message": "Hello World"}
