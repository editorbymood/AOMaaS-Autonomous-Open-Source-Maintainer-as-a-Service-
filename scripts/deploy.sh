#!/bin/bash
# Deployment script for AOMaaS

set -e  # Exit on any error

echo "🚀 Starting AOMaaS deployment..."

# Configuration
ENVIRONMENT=${ENVIRONMENT:-production}
DOCKER_COMPOSE_FILE=${DOCKER_COMPOSE_FILE:-docker-compose.yml}
ENV_FILE=${ENV_FILE:-.env}

# Colors for output
RED='[0;31m'
GREEN='[0;32m'
YELLOW='[1;33m'
BLUE='[0;34m'
NC='[0m' # No Color

log() {
    echo -e "[2025-08-31 00:17:44] "
}

warn() {
    echo -e "[WARNING] "
}

error() {
    echo -e "[ERROR] "
    exit 1
}

# Pre-deployment checks
log "Running pre-deployment checks..."

# Check if Docker is installed and running
if ! command -v docker &> /dev/null; then
    error "Docker is not installed. Please install Docker first."
fi

if ! docker info &> /dev/null; then
    error "Docker is not running. Please start Docker."
fi

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null; then
    warn "docker-compose not found, trying docker compose plugin..."
    if ! docker compose version &> /dev/null; then
        error "Neither docker-compose nor docker compose plugin is available."
    fi
    COMPOSE_CMD="docker compose"
else
    COMPOSE_CMD="docker-compose"
fi

# Check if environment file exists
if [[ ! -f "" ]]; then
    warn "Environment file  not found. Using defaults."
    if [[ -f ".env.example" ]]; then
        log "Copying .env.example to "
        cp .env.example ""
    fi
fi

# Build and start services
log "Building Docker images..."
 -f "" build

log "Starting services..."
 -f "" up -d

# Wait for services to be healthy
log "Waiting for services to be ready..."
sleep 10

# Health checks
log "Running health checks..."
check_service() {
    local service=
    local url=
    local max_attempts=30
    local attempt=1
    
    while [[  -le  ]]; do
        if curl -f -s "" > /dev/null 2>&1; then
            log "✅  is healthy"
            return 0
        fi
        echo -n "."
        sleep 2
        ((attempt++))
    done
    
    error "❌  failed to start after 0 seconds"
}

# Check core services
check_service "API" "http://localhost:8000/health"
check_service "MinIO" "http://localhost:9000/minio/health/ready"
check_service "Qdrant" "http://localhost:6333/health"

# Show running services
log "Deployment completed! Services running:"
 -f "" ps

log "🎉 AOMaaS is now running!"
echo -e ""
echo "📍 API Documentation: http://localhost:8000/docs"
echo "📍 MinIO Console: http://localhost:9001"
echo "📍 Qdrant Dashboard: http://localhost:6333/dashboard"
echo "📍 Flower (Celery): http://localhost:5555"
echo "📍 Health Check: http://localhost:8000/health"
echo -e ""

log "To stop services:  -f  down"
log "To view logs:  -f  logs -f"
