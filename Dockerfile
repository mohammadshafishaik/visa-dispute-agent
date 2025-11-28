FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency files
COPY pyproject.toml ./

# Install dependencies directly with pip (let pip resolve versions)
RUN pip install --no-cache-dir \
    "numpy<2.0" \
    fastapi \
    uvicorn[standard] \
    sqlalchemy \
    alembic \
    psycopg2-binary \
    asyncpg \
    chromadb==0.4.24 \
    langchain-ollama \
    langgraph \
    pydantic \
    pydantic-settings \
    python-dotenv \
    httpx \
    requests

# Copy application code
COPY app/ ./app/
COPY alembic/ ./alembic/
COPY alembic.ini ./
COPY scripts/ ./scripts/

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')"

# Run the application
CMD ["uvicorn", "app.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
