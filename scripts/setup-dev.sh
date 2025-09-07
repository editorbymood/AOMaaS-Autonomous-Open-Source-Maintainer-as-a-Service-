#!/bin/bash
# Development environment setup script

set -e

echo "🛠️ Setting up AOMaaS development environment..."

# Colors
GREEN='[0;32m'
BLUE='[0;34m'
YELLOW='[1;33m'
NC='[0m'

log() {
    echo -e "[2025-08-31 00:18:14] "
}

info() {
    echo -e "[INFO] "
}

warn() {
    echo -e "[WARNING] "
}

# Check Python version
log "Checking Python version..."
if ! command -v python3.11 &> /dev/null; then
    if ! command -v python3 &> /dev/null; then
        error "Python 3.11+ is required but not found."
    fi
    PYTHON_VERSION=
    if [[ "" < "3.11" ]]; then
        warn "Python 3.11+ is recommended. Found: "
    fi
    PYTHON_CMD="python3"
else
    PYTHON_CMD="python3.11"
fi

log "Using Python: "

# Create virtual environment
if [[ ! -d "venv" ]]; then
    log "Creating virtual environment..."
     -m venv venv
fi

# Activate virtual environment
log "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
log "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
log "Installing Python dependencies..."
pip install -e ".[dev]"

# Create .env file if it doesn't exist
if [[ ! -f ".env" ]]; then
    log "Creating .env file from template..."
    cp .env.example .env
    warn "Please edit .env file with your configuration"
fi

# Set up pre-commit hooks
log "Setting up pre-commit hooks..."
pre-commit install

# Create necessary directories
log "Creating necessary directories..."
mkdir -p logs repos artifacts temp

# Start development services
log "Starting development services with Docker Compose..."
if command -v docker-compose &> /dev/null; then
    docker-compose -f docker-compose.yml up -d postgres redis qdrant minio
else
    docker compose -f docker-compose.yml up -d postgres redis qdrant minio
fi

# Wait for services
log "Waiting for services to start..."
sleep 5

# Run initial setup
log "Running initial database setup..."
# TODO: Add database migration commands here
# alembic upgrade head

log "🎉 Development environment setup complete!"
echo -e ""
echo "To activate the environment: source venv/bin/activate"
echo "To start the API server: uvicorn aomass.api.main:app --reload"
echo "To start a Celery worker: celery -A aomass.core.worker worker --loglevel=info"
echo "To run tests: pytest"
echo "To format code: black src/ tests/"
echo "To lint code: ruff src/ tests/"
echo -e ""

info "Services running:"
info "- PostgreSQL: localhost:5432"
info "- Redis: localhost:6379"
info "- Qdrant: localhost:6333"
info "- MinIO: localhost:9000 (console: localhost:9001)"
