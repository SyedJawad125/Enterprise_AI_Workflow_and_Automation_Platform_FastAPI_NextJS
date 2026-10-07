"""
AI evaluation harness (spec section 35). Runs every request in dataset.json
through the same LangGraph flow AI Service uses, and scores:

  - intent classification accuracy
  - structured-output validity (did decision have all required keys?)
  - approval-gating accuracy (did requires_approval match expectation?)
  - invalid-tool-call rate
  - average latency / token usage / estimated cost

This can run with LLM_PROVIDER=mock (default, zero-cost, deterministic) for
CI, or against a real provider by setting LLM_PROVIDER=openai/groq and a key
-- the harness code doesn't change either way, which is the point of the
provider abstraction (ADR-010).

Run from services/ai-service/: PYTHONPATH=.:../.. python ../../eval/run_eval.py
"""
import asyncio
import json
import statistics
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "services" / "ai-service"))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.langgraph_flow import run_ai_flow  # noqa: E402

REQUIRED_DECISION_KEYS = {"recommended_action", "risk_level", "requires_approval", "reasoning"}


async def main():
    dataset_path = Path(__file__).resolve().parent / "dataset.json"
    with open(dataset_path) as f:
        dataset = json.load(f)

    correct_intent = 0
    correct_approval_gate = 0
    valid_structured_output = 0
    invalid_tool_calls = 0
    latencies = []
    total_tokens = 0
    total_cost = 0.0
    failures = []

    for row in dataset:
        try:
            state = await run_ai_flow(
                execution_id=row["id"],
                input_text=row["input_text"],
                customer_id=row["customer_id"],
                order_id=row["order_id"],
            )
        except Exception as exc:  # noqa: BLE001
            failures.append({"id": row["id"], "error": str(exc)})
            continue

        intent = state["intent"].get("intent")
        decision = state["decision"]
        usage = state["token_usage"]

        if intent == row["expected_intent"]:
            correct_intent += 1
        if bool(decision.get("requires_approval", False)) == row["expected_requires_approval"]:
            correct_approval_gate += 1
        if REQUIRED_DECISION_KEYS.issubset(decision.keys()):
            valid_structured_output += 1
        for tool_result in state.get("tool_results", {}).values():
            if isinstance(tool_result, dict) and "error" in tool_result:
                invalid_tool_calls += 1

        latencies.append(usage["latency_ms"])
        total_tokens += usage["input"] + usage["output"]
        total_cost += usage["estimated_cost"]

    n = len(dataset)
    report = {
        "total_requests": n,
        "failed_requests": len(failures),
        "intent_accuracy": round(correct_intent / n, 4),
        "approval_gate_accuracy": round(correct_approval_gate / n, 4),
        "structured_output_validity": round(valid_structured_output / n, 4),
        "invalid_tool_call_count": invalid_tool_calls,
        "avg_latency_ms": round(statistics.mean(latencies), 2) if latencies else None,
        "p95_latency_ms": round(statistics.quantiles(latencies, n=20)[18], 2) if len(latencies) >= 20 else None,
        "total_tokens": total_tokens,
        "estimated_total_cost_usd": round(total_cost, 6),
    }

    out_path = Path(__file__).resolve().parent / "eval_report.json"
    with open(out_path, "w") as f:
        json.dump({"report": report, "failures": failures}, f, indent=2)

    print(json.dumps(report, indent=2))
    print(f"\nFull report written to {out_path}")


if __name__ == "__main__":
    asyncio.run(main())
