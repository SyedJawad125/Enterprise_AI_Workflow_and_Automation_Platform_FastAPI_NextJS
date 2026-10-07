from pydantic import BaseModel, Field


class RefundRequest(BaseModel):
    order_id: str
    amount: float = Field(gt=0)
    reason: str


class RefundResponse(BaseModel):
    payment_id: str
    order_id: str
    amount: float
    status: str
    idempotent_replay: bool = False
