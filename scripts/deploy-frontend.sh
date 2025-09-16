#!/bin/bash

# AOMaaS Frontend Deployment Script

set -e

echo "Starting AOMaaS deployment..."

# Navigate to project root
cd "$(dirname "$0")/.." || exit 1

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
  echo "Error: Docker is not running. Please start Docker and try again."
  exit 1
fi

# Build the Docker image
echo "Building Docker image..."
docker-compose build api

# Deploy the application
echo "Deploying application..."
docker-compose up -d api

# Wait for the application to start
echo "Waiting for application to start..."
sleep 5

# Check if the application is running
if curl -s http://localhost:8000/health | grep -q "healthy"; then
  echo "Deployment successful! Application is running at http://localhost:8000"
else
  echo "Warning: Application may not have started correctly. Check logs with 'docker-compose logs api'"
fi

echo "Deployment completed."