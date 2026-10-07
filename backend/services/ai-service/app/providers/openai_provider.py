"""
OpenAI-compatible provider. Also works against any OpenAI-compatible
endpoint (vLLM, LM Studio, Azure OpenAI with the right base_url) by changing
OPENAI_BASE_URL -- that's the point of the interface: this class, and only
this class, knows the OpenAI wire format.
"""
from __future__ import annotations

import json
import os
import time

from openai import AsyncOpenAI

from app.providers.base import LLMProvider, LLMResult


class OpenAIProvider(LLMProvider):
    name = "openai"

    def __init__(self) -> None:
        self._client = AsyncOpenAI(
            api_key=os.environ.get("OPENAI_API_KEY", ""),
            base_url=os.environ.get("OPENAI_BASE_URL") or None,
        )

    async def generate_structured(self, system_prompt: str, user_prompt: str, model: str) -> LLMResult:
        start = time.time()
        response = await self._client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt + "\nRespond ONLY with valid JSON."},
                {"role": "user", "content": user_prompt},
            ],
            response_format={"type": "json_object"},
        )
        latency_ms = int((time.time() - start) * 1000)
        choice = response.choices[0].message.content or "{}"
        content = json.loads(choice)
        usage = response.usage
        return LLMResult(
            content=content,
            raw_text=choice,
            input_tokens=usage.prompt_tokens if usage else 0,
            output_tokens=usage.completion_tokens if usage else 0,
            latency_ms=latency_ms,
            model=model,
            provider=self.name,
        )
