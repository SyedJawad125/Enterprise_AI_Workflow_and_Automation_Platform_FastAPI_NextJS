"""
The AI reasoning workflow, built with LangGraph -- and ONLY this reasoning
path. Deterministic steps elsewhere in the platform (workflow state
transitions, notification dispatch) are plain Python/state-machine code in
Workflow Service, not LangGraph, per the architecture's explicit rule:
LangGraph is for AI-oriented reasoning, not a general workflow engine.

Graph:

    INPUT -> intent_analysis -> planning -> tool_selection -> tool_execution
          -> validation -> decision -> END

`decision` sets `requires_approval`; the *pausing* for human approval itself
is NOT modeled inside this graph -- it's a Workflow Service state
(WAITING_FOR_APPROVAL). This graph's job ends the moment it has produced a
validated recommendation; Workflow Service decides what happens next.
"""
from __future__ import annotations

import time
from typing import Any, Literal, TypedDict

from langgraph.graph import StateGraph, END
from pydantic import BaseModel, ValidationError

from app.providers.base import estimate_cost
from app.providers.factory import get_provider
from app.tools import execute_tool
from shared.exceptions import LLMError
from shared.logging.logger import get_logger

logger = get_logger("ai-service.langgraph")


class DecisionOutput(BaseModel):
    """
    The contract every LLM decision must satisfy before Workflow Service is
    allowed to act on it (spec section 21: never blindly trust arbitrary
    JSON from an LLM). If the raw output doesn't validate, we ask the model
    to repair it once; if it still doesn't validate, we fail safe rather
    than guess at the model's intent.
    """
    recommended_action: str
    risk_level: Literal["low", "high"]
    requires_approval: bool
    reasoning: str


class AIFlowState(TypedDict, total=False):
    execution_id: str
    input_text: str
    customer_id: str | None
    order_id: str | None
    intent: dict[str, Any]
    plan: list[str]
    tool_results: dict[str, Any]
    validation_errors: list[str]
    decision: dict[str, Any]
    token_usage: dict[str, Any]


async def node_intent_analysis(state: AIFlowState) -> AIFlowState:
    provider = get_provider()
    result = await provider.generate_structured(
        system_prompt="You classify customer intent. Return JSON with 'intent' and 'confidence'.",
        user_prompt=state["input_text"],
        model="mock-classifier-v1",
    )
    state["intent"] = result.content
    state.setdefault("token_usage", {"input": 0, "output": 0, "provider": result.provider})
    state["token_usage"]["input"] += result.input_tokens
    state["token_usage"]["output"] += result.output_tokens
    logger.info("intent analysis complete", extra={"intent": result.content})
    return state


async def node_planning(state: AIFlowState) -> AIFlowState:
    intent = state["intent"].get("intent", "general_inquiry")
    plan = []
    if state.get("customer_id"):
        plan.append("customer_lookup")
    if state.get("order_id") and intent == "refund_request":
        plan.append("order_lookup")
    state["plan"] = plan
    return state


async def node_tool_selection_and_execution(state: AIFlowState) -> AIFlowState:
    results: dict[str, Any] = {}
    for tool_name in state.get("plan", []):
        try:
            if tool_name == "customer_lookup":
                results[tool_name] = await execute_tool(tool_name, {"customer_id": state["customer_id"]})
            elif tool_name == "order_lookup":
                results[tool_name] = await execute_tool(tool_name, {"order_id": state["order_id"]})
        except Exception as exc:  # noqa: BLE001
            logger.error("tool execution failed", extra={"tool": tool_name, "error": str(exc)})
            results[tool_name] = {"error": str(exc)}
    state["tool_results"] = results
    return state


async def node_validation(state: AIFlowState) -> AIFlowState:
    errors = []
    for tool_name, result in state.get("tool_results", {}).items():
        if isinstance(result, dict) and "error" in result:
            errors.append(f"{tool_name} failed: {result['error']}")
    state["validation_errors"] = errors
    return state


async def node_decision(state: AIFlowState) -> AIFlowState:
    if state.get("validation_errors"):
        # A failed customer/order lookup means the AI's recommendation would
        # be built on missing data. Escalating that to a human for approval
        # would ask them to approve a decision with no evidence behind it --
        # the correct behavior is to fail the step cleanly, not paper over
        # a data problem with a human-approval workaround.
        state["decision"] = {
            "recommended_action": "fail",
            "risk_level": "high",
            "requires_approval": False,
            "reasoning": "Tool execution produced validation errors: " + "; ".join(state["validation_errors"]),
        }
        return state

    order = state.get("tool_results", {}).get("order_lookup", {})
    amount = order.get("amount", 0) if isinstance(order, dict) else 0

    provider = get_provider()
    system_prompt = (
        "You make a decision recommendation. Return JSON with 'recommended_action', "
        "'risk_level' (must be exactly 'low' or 'high'), 'requires_approval' (boolean), 'reasoning'."
    )
    user_prompt = f"{state['input_text']} amount={amount}"

    result = await provider.generate_structured(system_prompt=system_prompt, user_prompt=user_prompt, model="mock-decision-v1")
    state["token_usage"]["input"] += result.input_tokens
    state["token_usage"]["output"] += result.output_tokens

    validated = _validate_decision(result.content)
    if validated is None:
        # Repair attempt: tell the model exactly what was wrong and ask again,
        # once. This is cheaper than failing outright on a model that just
        # slightly malformed its first response (e.g. wrong casing on an enum).
        logger.warning("decision output failed validation, attempting repair", extra={"raw_output": result.content})
        repair_prompt = (
            f"{user_prompt}\n\nYour previous response was invalid: {result.content}. "
            "Return ONLY valid JSON with EXACTLY these keys: recommended_action (string), "
            "risk_level ('low' or 'high'), requires_approval (true/false), reasoning (string)."
        )
        repair_result = await provider.generate_structured(system_prompt=system_prompt, user_prompt=repair_prompt, model="mock-decision-v1")
        state["token_usage"]["input"] += repair_result.input_tokens
        state["token_usage"]["output"] += repair_result.output_tokens
        validated = _validate_decision(repair_result.content)

    if validated is None:
        logger.error("decision output still invalid after repair attempt, failing safe")
        state["decision"] = {
            "recommended_action": "fail",
            "risk_level": "high",
            "requires_approval": False,
            "reasoning": "AI produced invalid structured output after a repair attempt; failing safe rather than acting on unvalidated data.",
        }
        return state

    state["decision"] = validated.model_dump()
    return state


def _validate_decision(raw: dict[str, Any]) -> DecisionOutput | None:
    try:
        return DecisionOutput(**raw)
    except ValidationError:
        return None


def build_graph():
    graph = StateGraph(AIFlowState)
    graph.add_node("intent_analysis", node_intent_analysis)
    graph.add_node("planning", node_planning)
    graph.add_node("tool_execution", node_tool_selection_and_execution)
    graph.add_node("validation", node_validation)
    graph.add_node("decide", node_decision)

    graph.set_entry_point("intent_analysis")
    graph.add_edge("intent_analysis", "planning")
    graph.add_edge("planning", "tool_execution")
    graph.add_edge("tool_execution", "validation")
    graph.add_edge("validation", "decide")
    graph.add_edge("decide", END)

    return graph.compile()


_compiled_graph = None


def get_graph():
    global _compiled_graph
    if _compiled_graph is None:
        _compiled_graph = build_graph()
    return _compiled_graph


async def run_ai_flow(
    execution_id: str, input_text: str, customer_id: str | None, order_id: str | None
) -> AIFlowState:
    start = time.time()
    initial_state: AIFlowState = {
        "execution_id": execution_id,
        "input_text": input_text,
        "customer_id": customer_id,
        "order_id": order_id,
    }
    graph = get_graph()
    final_state = await graph.ainvoke(initial_state)
    duration_ms = int((time.time() - start) * 1000)
    final_state["token_usage"]["latency_ms"] = duration_ms
    final_state["token_usage"]["estimated_cost"] = estimate_cost(
        final_state["token_usage"].get("provider", "mock"),
        final_state["token_usage"]["input"],
        final_state["token_usage"]["output"],
    )
    return final_state
