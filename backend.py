"""
FastAPI backend for the LLM chat application.
Provides REST API endpoints that replicate the Chainlit functionality.
"""

import os
from typing import AsyncGenerator
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from openai import AsyncOpenAI
from dotenv import load_dotenv
import json

load_dotenv()

app = FastAPI(title="LLM Chat API", version="1.0.0")

# Configure CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # React dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# OpenAI client
client = AsyncOpenAI()

# Chat templates (from original Chainlit app)
SYSTEM_TEMPLATE = "You are a helpful assistant who always speaks in a pleasant tone!"
USER_TEMPLATE = "{input}\nThink through your response step by step."

# Default OpenAI settings (from original Chainlit app)
DEFAULT_SETTINGS = {
    "model": "gpt-3.5-turbo",
    "temperature": 0,
    "max_tokens": 500,
    "top_p": 1,
    "frequency_penalty": 0,
    "presence_penalty": 0,
}


class ChatMessage(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str


@app.get("/")
async def root():
    """Health check endpoint."""
    return {"status": "ok", "message": "LLM Chat API is running"}


@app.post("/chat")
async def chat_completion(chat_message: ChatMessage) -> ChatResponse:
    """
    Non-streaming chat completion endpoint.
    """
    try:
        messages = [
            {"role": "system", "content": SYSTEM_TEMPLATE},
            {"role": "user", "content": USER_TEMPLATE.format(input=chat_message.message)}
        ]

        response = await client.chat.completions.create(
            messages=messages,
            **DEFAULT_SETTINGS
        )

        return ChatResponse(response=response.choices[0].message.content)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating response: {str(e)}")


@app.post("/chat/stream")
async def chat_stream(chat_message: ChatMessage):
    """
    Streaming chat completion endpoint.
    Returns Server-Sent Events (SSE) format for real-time streaming.
    """
    async def generate_stream() -> AsyncGenerator[str, None]:
        try:
            messages = [
                {"role": "system", "content": SYSTEM_TEMPLATE},
                {"role": "user", "content": USER_TEMPLATE.format(input=chat_message.message)}
            ]

            stream = await client.chat.completions.create(
                messages=messages,
                stream=True,
                **DEFAULT_SETTINGS
            )

            async for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    # Format as Server-Sent Events
                    data = json.dumps({"content": chunk.choices[0].delta.content})
                    yield f"data: {data}\n\n"
            
            # Send end-of-stream marker
            yield "data: [DONE]\n\n"

        except Exception as e:
            error_data = json.dumps({"error": str(e)})
            yield f"data: {error_data}\n\n"

    return StreamingResponse(
        generate_stream(),
        media_type="text/plain",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    )


@app.get("/config")
async def get_config():
    """
    Get current configuration settings.
    """
    return {
        "model_settings": DEFAULT_SETTINGS,
        "system_template": SYSTEM_TEMPLATE,
        "user_template": USER_TEMPLATE
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)