FROM python:3.12-slim
WORKDIR /app
COPY services/api-gateway/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY shared /app/shared
COPY services/api-gateway/app /app/app
ENV PYTHONPATH=/app
ENV SERVICE_NAME=api-gateway
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
