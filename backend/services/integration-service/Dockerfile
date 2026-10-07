FROM python:3.12-slim
WORKDIR /app
COPY services/integration-service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY shared /app/shared
COPY services/integration-service/app /app/app
ENV PYTHONPATH=/app
ENV SERVICE_NAME=integration-service
EXPOSE 8004
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8004"]
