"""
Groq provider -- Groq's API is OpenAI-compatible, so this subclasses
OpenAIProvider and only overrides the base URL / key / name. This is a
concrete illustration of "add a provider without rewriting the service":
~10 lines, not a new integration.
"""
from __future__ import annotations

import os

from openai import AsyncOpenAI

from app.providers.openai_provider import OpenAIProvider


class GroqProvider(OpenAIProvider):
    name = "groq"

    def __init__(self) -> None:
        self._client = AsyncOpenAI(
            api_key=os.environ.get("GROQ_API_KEY", ""),
            base_url="https://api.groq.com/openai/v1",
        )
