"""
Unit tests for the mock LLM provider -- the AI Service's decision logic must
be testable deterministically, independent of a live LLM's variance.

Run from services/ai-service/: PYTHONPATH=.:../.. pytest tests/ -v
(the repo-root Makefile's `make test` wires this up per-service.)
"""
import asyncio

from app.providers.mock_provider import MockProvider


def run(coro):
    return asyncio.get_event_loop().run_until_complete(coro)


def test_intent_classifies_refund():
    provider = MockProvider()
    result = run(provider.generate_structured(
        system_prompt="Classify the intent", user_prompt="I want a refund for the wrong item", model="m"
    ))
    assert result.content["intent"] == "refund_request"


def test_decision_flags_high_risk_amount():
    provider = MockProvider()
    result = run(provider.generate_structured(
        system_prompt="Make a decision", user_prompt="refund 150.00", model="m"
    ))
    assert result.content["risk_level"] == "high"
    assert result.content["requires_approval"] is True


def test_decision_low_risk_amount_auto_approvable():
    provider = MockProvider()
    result = run(provider.generate_structured(
        system_prompt="Make a decision", user_prompt="refund 20.00", model="m"
    ))
    assert result.content["risk_level"] == "low"
    assert result.content["requires_approval"] is False
