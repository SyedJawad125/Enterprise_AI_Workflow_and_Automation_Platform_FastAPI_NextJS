from pydantic import BaseModel


class AIExecuteRequest(BaseModel):
    execution_id: str
    input_text: str
    customer_id: str | None = None
    order_id: str | None = None


class AIExecuteResponse(BaseModel):
    execution_id: str
    intent: dict
    decision: dict
    tool_results: dict
    requires_approval: bool
    tokens_used: int
    estimated_cost: float
    latency_ms: int
