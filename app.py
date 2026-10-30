# You can find this code for Chainlit python streaming here (https://docs.chainlit.io/concepts/streaming/python)

# OpenAI Chat completion
import os
from openai import AsyncOpenAI, AuthenticationError  # importing openai for API usage
import chainlit as cl  # importing chainlit for our app
from chainlit.prompt import Prompt, PromptMessage  # importing prompt tools
from chainlit.playground.providers import ChatOpenAI  # importing ChatOpenAI tools
from dotenv import load_dotenv

load_dotenv()

# ChatOpenAI Templates
system_template = """You are a helpful assistant who always speaks in a pleasant tone!
"""

user_template = """{input}
Think through your response step by step.
"""

NO_KEY_MESSAGE = (
    "No OpenAI API key is configured, so no reply was generated. "
    "Set OPENAI_API_KEY in .env and restart the app."
)
REJECTED_KEY_MESSAGE = "OpenAI rejected the configured API key, so no reply was generated."


def has_api_key() -> bool:
    return bool(os.environ.get("OPENAI_API_KEY", "").strip())


@cl.on_chat_start  # marks a function that will be executed at the start of a user session
async def start_chat():
    settings = {
        "model": "gpt-3.5-turbo",
        "temperature": 0,
        "max_tokens": 500,
        "top_p": 1,
        "frequency_penalty": 0,
        "presence_penalty": 0,
    }

    cl.user_session.set("settings", settings)


@cl.on_message  # marks a function that should be run each time the chatbot receives a message from a user
async def main(message: cl.Message):
    settings = cl.user_session.get("settings")

    # Honest no-key state: say so instead of failing with a stack trace.
    if not has_api_key():
        await cl.Message(content=NO_KEY_MESSAGE).send()
        return

    client = AsyncOpenAI()

    print(message.content)

    prompt = Prompt(
        provider=ChatOpenAI.id,
        messages=[
            PromptMessage(
                role="system",
                template=system_template,
                formatted=system_template,
            ),
            PromptMessage(
                role="user",
                template=user_template,
                formatted=user_template.format(input=message.content),
            ),
        ],
        inputs={"input": message.content},
        settings=settings,
    )

    print([m.to_openai() for m in prompt.messages])

    msg = cl.Message(content="")

    # Call OpenAI
    try:
        stream = await client.chat.completions.create(
            messages=[m.to_openai() for m in prompt.messages], stream=True, **settings
        )
    except AuthenticationError:
        await cl.Message(content=REJECTED_KEY_MESSAGE).send()
        return
    async for stream_resp in stream:
        token = stream_resp.choices[0].delta.content if stream_resp.choices else ""
        if not token:
            token = ""
        await msg.stream_token(token)

    # Update the prompt object with the completion
    prompt.completion = msg.content
    msg.prompt = prompt

    # Send and close the message stream
    await msg.send()
