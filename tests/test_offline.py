"""Offline tests: no OpenAI key, no network. Chainlit handlers are called with stubbed messages."""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import app  # noqa: E402


class FakeMessage:
    sent = []

    def __init__(self, content=""):
        self.content = content

    async def send(self):
        FakeMessage.sent.append(self.content)


def test_has_api_key(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    assert app.has_api_key() is False
    monkeypatch.setenv("OPENAI_API_KEY", "   ")
    assert app.has_api_key() is False
    monkeypatch.setenv("OPENAI_API_KEY", "set")
    assert app.has_api_key() is True


def test_no_key_replies_honestly(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.setattr(app.cl, "Message", FakeMessage)
    monkeypatch.setattr(app.cl.user_session, "get", lambda key: {"model": "gpt-3.5-turbo"})
    FakeMessage.sent.clear()
    asyncio.run(app.main(FakeMessage("hello")))
    assert FakeMessage.sent == [app.NO_KEY_MESSAGE]


def test_templates():
    assert "{input}" in app.user_template
    assert "pleasant tone" in app.system_template
