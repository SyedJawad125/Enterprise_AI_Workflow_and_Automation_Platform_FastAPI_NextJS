FROM python:3.12-slim
WORKDIR /app
COPY services/ai-service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY shared /app/shared
COPY services/ai-service/app /app/app
ENV PYTHONPATH=/app
ENV SERVICE_NAME=ai-service
EXPOSE 8003
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8003"]
