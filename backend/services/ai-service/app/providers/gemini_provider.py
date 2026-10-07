"""
Gemini provider stub. Kept minimal/未连线 by default (no google-generativeai
dependency installed) to avoid bloating the image for a portfolio project;
the shape shows exactly what plugging in a genuinely different SDK (not
OpenAI-compatible) looks like against the same LLMProvider interface.
"""
from __future__ import annotations

import time

from app.providers.base import LLMProvider, LLMResult
from shared.exceptions import LLMError


class GeminiProvider(LLMProvider):
    name = "gemini"

    async def generate_structured(self, system_prompt: str, user_prompt: str, model: str) -> LLMResult:
        raise LLMError(
            "Gemini provider is a structural stub in this build -- install google-generativeai "
            "and implement generate_structured() following the OpenAIProvider pattern to activate it.",
        )
