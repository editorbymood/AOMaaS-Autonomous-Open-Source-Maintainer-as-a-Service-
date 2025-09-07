# Production Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y     git     gcc     g++     && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY pyproject.toml ./
COPY requirements.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -e .

# Copy source code
COPY src/ ./src/
COPY configs/ ./configs/

# Create non-root user
RUN useradd --create-home --shell /bin/bash aomass
RUN chown -R aomass:aomass /app
USER aomass

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3     CMD curl -f http://localhost:8000/health || exit 1

# Default command
CMD ["uvicorn", "aomass.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
