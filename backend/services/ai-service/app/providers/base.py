"""
LLMProvider: the interface every provider implements. Nothing else in the
codebase imports `openai`, `groq`, or a Gemini SDK directly -- everything
goes through this interface, selected once by config (`LLM_PROVIDER` env
var) in providers/factory.py. Adding a new provider means implementing this
one class; it never touches the LangGraph flow, the AI Service routes, or
the workers.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any


@dataclass
class LLMResult:
    content: dict[str, Any]     # parsed structured output
    raw_text: str
    input_tokens: int
    output_tokens: int
    latency_ms: int
    model: str
    provider: str


# Rough $ per 1K tokens, for cost estimation only -- not billing-accurate.
COST_PER_1K_TOKENS = {
    "mock": {"input": 0.0, "output": 0.0},
    "openai": {"input": 0.0005, "output": 0.0015},
    "groq": {"input": 0.0002, "output": 0.0002},
    "gemini": {"input": 0.0003, "output": 0.0006},
}


def estimate_cost(provider: str, input_tokens: int, output_tokens: int) -> float:
    rates = COST_PER_1K_TOKENS.get(provider, COST_PER_1K_TOKENS["mock"])
    return round((input_tokens / 1000) * rates["input"] + (output_tokens / 1000) * rates["output"], 6)


class LLMProvider(ABC):
    name: str = "base"

    @abstractmethod
    async def generate_structured(self, system_prompt: str, user_prompt: str, model: str) -> LLMResult:
        """Call the underlying LLM and return a structured (JSON-parsed) result.

        Every provider MUST return valid parsed JSON in `.content` or raise
        LLMError -- callers should never have to guess whether `.content`
        is a dict or a raw string.
        """
        raise NotImplementedError
