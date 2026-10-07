FROM python:3.12-slim
WORKDIR /app
COPY services/workflow-service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY shared /app/shared
COPY services/workflow-service/app /app/app
COPY services/workflow-service/alembic /app/alembic
COPY services/workflow-service/alembic.ini /app/alembic.ini
ENV PYTHONPATH=/app
ENV SERVICE_NAME=workflow-service
EXPOSE 8002
# Migrations are the source of truth for schema changes (see ADR-011);
# `alembic upgrade head` runs once at container start, then the app boots.
# If it fails, the container fails to start rather than serving traffic
# against a schema it doesn't match.
CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8002"]
