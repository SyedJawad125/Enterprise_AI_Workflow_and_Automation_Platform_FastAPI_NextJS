FROM python:3.12-slim
WORKDIR /app
COPY services/notification-service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY shared /app/shared
COPY services/notification-service/app /app/app
ENV PYTHONPATH=/app
ENV SERVICE_NAME=notification-service
EXPOSE 8005
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8005"]
