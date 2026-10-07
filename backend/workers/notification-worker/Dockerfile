FROM python:3.12-slim
WORKDIR /app
COPY workers/notification-worker/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY shared /app/shared
COPY workers/notification-worker/tasks.py /app/tasks.py
ENV PYTHONPATH=/app
ENV SERVICE_NAME=notification-worker
CMD ["celery", "-A", "tasks", "worker", "--loglevel=info", "-Q", "notification.queue", "-n", "notification-worker@%h"]
