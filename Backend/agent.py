from agents import (
    Agent,
    Runner,
    OpenAIChatCompletionsModel,
    set_tracing_disabled,
    function_tool,
    enable_verbose_stdout_logging,
)
from openai import AsyncOpenAI

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import os
from dotenv import load_dotenv

import cohere
from qdrant_client import QdrantClient

# ------------------------------------------------------------------
# LOGGING / ENV
# ------------------------------------------------------------------

enable_verbose_stdout_logging()
load_dotenv()
set_tracing_disabled(disabled=True)

# ------------------------------------------------------------------
# MODEL (GEMINI via OPENAI COMPAT)
# ------------------------------------------------------------------

gemini_api_key = os.getenv("GEMINI_API_KEY")

provider = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=provider,
)

# ------------------------------------------------------------------
# COHERE + QDRANT
# ------------------------------------------------------------------

cohere_client = cohere.Client(os.getenv("COHERE_API_KEY"))

qdrant = QdrantClient(
    url=os.getenv("QDRANT_BASE_URL"),
    api_key=os.getenv("QDRANT_API"),
)

COLLECTION_NAME = os.getenv(
    "QDRANT_COLLECTION_NAME",
    "testing-rag-chatbot",
)

# ------------------------------------------------------------------
# FASTAPI
# ------------------------------------------------------------------

app = FastAPI(title="Physical AI RAG Chatbot")

# -----------------
# 3. CORS Configuration
# -----------------

# origins = [
#     # IMPORTANT: Change this to your React development port if different from 3000
#     "http://localhost:5173",
#     "http://127.0.0.1:8000/",
# ]

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

# ------------------------------------------------------------------
# REQUEST / RESPONSE SCHEMAS
# ------------------------------------------------------------------


class ChatRequest(BaseModel):
    question: str


class ChatResponse(BaseModel):
    answer: str


# ------------------------------------------------------------------
# EMBEDDING
# ------------------------------------------------------------------


def get_embedding(text: str):
    response = cohere_client.embed(
        model="embed-english-v3.0",
        input_type="search_query",
        texts=[text],
    )
    return response.embeddings[0]


# ------------------------------------------------------------------
# RETRIEVAL TOOL (USED BY AGENT)
# ------------------------------------------------------------------


@function_tool
def retrieve(query: str):
    embedding = get_embedding(query)

    result = qdrant.query_points(
        collection_name=COLLECTION_NAME,
        query=embedding,
        limit=5,
    )

    return [point.payload["text"] for point in result.points]


# ------------------------------------------------------------------
# AGENT
# ------------------------------------------------------------------

agent = Agent(
    name="Assistant",
    instructions="""
You are an AI tutor for the Physical AI & Humanoid Robotics textbook.

To answer the user question:
1. First call the tool `retrieve` with the user query.
2. Use ONLY the returned content from `retrieve`.
3. If the answer is not present, say "I don't know".
""",
    model=model,
    tools=[retrieve],
)


# ------------------------------------------------------------------
# API ENDPOINT
# ------------------------------------------------------------------
@app.get("/")
def root():
    return {"message": "Hello, World!"}


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    result = Runner.run_sync(
        agent,
        input=req.question,
    )

    return {
        "answer": result.final_output,
    }
