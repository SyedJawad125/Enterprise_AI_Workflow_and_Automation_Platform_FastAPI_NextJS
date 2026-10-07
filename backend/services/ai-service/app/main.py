from fastapi import Depends, FastAPI
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from shared.exceptions import install_exception_handlers
from shared.health import check_postgres
from shared.logging.logger import RequestContextMiddleware, get_logger

from app.core.config import LLM_PROVIDER
from app.db import get_db, init_models, engine
from app.langgraph_flow import run_ai_flow
from app.models import AIRequest, AIResponse, TokenUsage
from app.schemas import AIExecuteRequest, AIExecuteResponse

logger = get_logger("ai-service")

app = FastAPI(title="AI Service")
app.add_middleware(RequestContextMiddleware)
install_exception_handlers(app)


@app.on_event("startup")
async def on_startup():
    await init_models()
    logger.info("ai-service started", extra={"provider": LLM_PROVIDER})


@app.get("/health")
async def health():
    return {"status": "ok", "service": "ai-service", "provider": LLM_PROVIDER}


@app.get("/ready")
async def ready():
    postgres_status = await check_postgres(engine)
    status = "ready" if postgres_status == "healthy" else "not_ready"
    return JSONResponse(
        status_code=200 if status == "ready" else 503,
        content={"status": status, "service": "ai-service", "dependencies": {"postgres": postgres_status}},
    )


@app.post("/ai/execute", response_model=AIExecuteResponse)
async def execute(payload: AIExecuteRequest, db: AsyncSession = Depends(get_db)):
    request_row = AIRequest(execution_id=payload.execution_id, input_data=payload.model_dump())
    db.add(request_row)
    await db.flush()

    final_state = await run_ai_flow(
        execution_id=payload.execution_id,
        input_text=payload.input_text,
        customer_id=payload.customer_id,
        order_id=payload.order_id,
    )

    decision = final_state["decision"]
    usage = final_state["token_usage"]

    response_row = AIResponse(
        request_id=request_row.id,
        execution_id=payload.execution_id,
        decision=decision,
        requires_approval=bool(decision.get("requires_approval", False)),
    )
    db.add(response_row)

    db.add(TokenUsage(
        execution_id=payload.execution_id,
        provider=usage.get("provider", "mock"),
        model="mock-decision-v1",
        input_tokens=usage["input"],
        output_tokens=usage["output"],
        total_tokens=usage["input"] + usage["output"],
        latency_ms=usage["latency_ms"],
        estimated_cost=usage["estimated_cost"],
    ))
    await db.commit()

    logger.info(
        "ai execution complete",
        extra={
            "execution_id": payload.execution_id,
            "requires_approval": decision.get("requires_approval"),
            "estimated_cost": usage["estimated_cost"],
        },
    )

    return AIExecuteResponse(
        execution_id=payload.execution_id,
        intent=final_state["intent"],
        decision=decision,
        tool_results=final_state.get("tool_results", {}),
        requires_approval=bool(decision.get("requires_approval", False)),
        tokens_used=usage["input"] + usage["output"],
        estimated_cost=usage["estimated_cost"],
        latency_ms=usage["latency_ms"],
    )
