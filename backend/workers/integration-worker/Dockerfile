FROM python:3.12-slim
WORKDIR /app
COPY workers/integration-worker/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY shared /app/shared
COPY workers/integration-worker/tasks.py /app/tasks.py
ENV PYTHONPATH=/app
ENV SERVICE_NAME=integration-worker
CMD ["celery", "-A", "tasks", "worker", "--loglevel=info", "-Q", "integration.processing.queue", "-n", "integration-worker@%h"]
