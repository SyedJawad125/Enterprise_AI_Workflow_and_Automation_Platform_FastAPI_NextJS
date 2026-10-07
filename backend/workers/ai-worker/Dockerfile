FROM python:3.12-slim
WORKDIR /app
COPY workers/ai-worker/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY shared /app/shared
COPY workers/ai-worker/tasks.py /app/tasks.py
ENV PYTHONPATH=/app
ENV SERVICE_NAME=ai-worker
CMD ["celery", "-A", "tasks", "worker", "--loglevel=info", "-Q", "ai.processing.queue", "-n", "ai-worker@%h"]
