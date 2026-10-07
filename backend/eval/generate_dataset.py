"""
Generates a synthetic evaluation dataset of customer requests (spec section
35). 100 requests across 3 intents with varying refund amounts, so the eval
run below can measure intent-classification accuracy, tool-selection
correctness, and how often the risk gate fires -- all deterministically
against MockProvider, without needing a paid LLM key for the harness to run
in CI.
"""
import json
import random

random.seed(42)

REFUND_TEMPLATES = [
    "I received the wrong product and want a refund of ${amount}.",
    "This item arrived broken, please refund ${amount}.",
    "I'd like to return this and get ${amount} back.",
]
SUPPORT_TEMPLATES = [
    "My order hasn't shipped yet, can you check the ticket?",
    "I have an issue with my account, opening a support ticket.",
    "There's a problem with my last order, please help via ticket.",
]
GENERAL_TEMPLATES = [
    "What are your business hours?",
    "Do you ship internationally?",
    "How long does standard shipping take?",
]

CUSTOMERS = ["cust_1001", "cust_1002"]
ORDERS = ["ord_5001", "ord_5002"]


def build_dataset(n=100):
    rows = []
    for i in range(n):
        bucket = random.choices(["refund", "support", "general"], weights=[0.5, 0.3, 0.2])[0]
        if bucket == "refund":
            amount = round(random.choice([15, 25, 45, 80, 120, 250, 500]), 2)
            text = random.choice(REFUND_TEMPLATES).format(amount=amount)
            expected_intent = "refund_request"
            expected_requires_approval = amount >= 100
        elif bucket == "support":
            text = random.choice(SUPPORT_TEMPLATES)
            expected_intent = "support_request"
            expected_requires_approval = False
        else:
            text = random.choice(GENERAL_TEMPLATES)
            expected_intent = "general_inquiry"
            expected_requires_approval = False

        rows.append({
            "id": f"req_{i:03d}",
            "input_text": text,
            "customer_id": random.choice(CUSTOMERS),
            "order_id": random.choice(ORDERS) if bucket == "refund" else None,
            "expected_intent": expected_intent,
            "expected_requires_approval": expected_requires_approval,
        })
    return rows


if __name__ == "__main__":
    dataset = build_dataset(100)
    with open("dataset.json", "w") as f:
        json.dump(dataset, f, indent=2)
    print(f"Wrote {len(dataset)} synthetic requests to dataset.json")
