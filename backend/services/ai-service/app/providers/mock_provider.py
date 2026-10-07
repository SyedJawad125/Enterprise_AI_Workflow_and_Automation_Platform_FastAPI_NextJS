"""
Deterministic, zero-cost provider used by default (LLM_PROVIDER=mock) so the
whole platform -- including the demo scenarios and the eval harness -- runs
without any paid API key. It applies simple, explainable heuristics instead
of calling a real model, which also makes the AI Service's *workflow*
(structured output validation, tool use, human-in-the-loop gating) testable
deterministically, independent of a live LLM's variance.
"""
from __future__ import annotations

import time

from app.providers.base import LLMProvider, LLMResult, estimate_cost


class MockProvider(LLMProvider):
    name = "mock"

    async def generate_structured(self, system_prompt: str, user_prompt: str, model: str) -> LLMResult:
        start = time.time()
        text = user_prompt.lower()

        if "intent" in system_prompt.lower():
            if "refund" in text or "wrong" in text or "return" in text:
                content = {"intent": "refund_request", "confidence": 0.92}
            elif "ticket" in text or "issue" in text or "support" in text:
                content = {"intent": "support_request", "confidence": 0.85}
            else:
                content = {"intent": "general_inquiry", "confidence": 0.6}

        elif "decision" in system_prompt.lower():
            amount = 0.0
            for token in text.replace("$", " ").split():
                try:
                    amount = float(token)
                    break
                except ValueError:
                    continue
            risk = "high" if amount >= 100 else "low"
            content = {
                "recommended_action": "refund" if "refund" in text else "escalate_to_human",
                "risk_level": risk,
                "requires_approval": risk == "high",
                "reasoning": (
                    f"Requested amount ${amount:.2f} classified as {risk} risk; "
                    f"{'approval required above $100' if risk == 'high' else 'auto-approvable'}."
                ),
            }
        else:
            content = {"result": "ok", "notes": "mock provider generic response"}

        latency_ms = int((time.time() - start) * 1000) + 40  # simulate a little latency
        input_tokens = max(len(system_prompt.split()) + len(user_prompt.split()), 1)
        output_tokens = max(len(str(content).split()), 1)
        return LLMResult(
            content=content,
            raw_text=str(content),
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            latency_ms=latency_ms,
            model=model,
            provider=self.name,
        )
