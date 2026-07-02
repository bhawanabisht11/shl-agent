from fastapi import FastAPI
from pydantic import BaseModel

from rag.rag_pipeline import rag_chat

app = FastAPI(
    title="SHL Conversational Agent",
    version="1.0.0"
)


class ChatRequest(BaseModel):
    query: str


@app.get("/")
def root():
    return {
        "message": "Welcome to the SHL Conversational Agent API"
    }


@app.get("/health")
def health():
    return {
        "status": "ok"
    }


@app.post("/chat")
def chat(request: ChatRequest):
    response = rag_chat(request.query)

    return {
        "response": response
    }