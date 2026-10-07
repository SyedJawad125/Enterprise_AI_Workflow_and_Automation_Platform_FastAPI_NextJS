FROM python:3.12-slim
WORKDIR /app
COPY services/audit-service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY shared /app/shared
COPY services/audit-service/app /app/app
ENV PYTHONPATH=/app
ENV SERVICE_NAME=audit-service
EXPOSE 8006
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8006"]
