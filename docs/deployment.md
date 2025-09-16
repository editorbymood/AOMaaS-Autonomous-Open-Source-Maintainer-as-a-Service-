# AOMaaS Deployment Guide

## Overview

This guide provides instructions for deploying AOMaaS (Autonomous Open-Source Maintainer as a Service) in various environments, from development to production.

## Prerequisites

- Docker and Docker Compose (for development and testing)
- Kubernetes cluster (for production deployment)
- Domain name and SSL certificate (for production deployment)
- Access to cloud services (optional, for scaling)

## Development Deployment

### Using Docker Compose

The easiest way to deploy AOMaaS for development and testing is using Docker Compose.

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/aomass.git
   cd aomass
   ```

2. Run the deployment script:

   ```bash
   ./scripts/deploy-frontend.sh
   ```

   This script will:
   - Build the Docker images
   - Start all the required services
   - Initialize the databases
   - Set up the required volumes

3. Access the AOMaaS web interface at http://localhost:8000

### Manual Development Setup

If you prefer to run the services manually:

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/aomass.git
   cd aomass
   ```

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Set up the environment variables:

   ```bash
   cp .env.example .env
   ```

   Edit the `.env` file to configure your environment.

4. Start the required services (PostgreSQL, Redis, Qdrant, MinIO):

   ```bash
   docker-compose up -d postgres redis qdrant minio
   ```

5. Initialize the databases:

   ```bash
   python -m src.aomass.scripts.init_db
   ```

6. Start the API server:

   ```bash
   uvicorn src.aomass.main:app --reload
   ```

7. Start the worker:

   ```bash
   celery -A src.aomass.core.worker worker --loglevel=info
   ```

8. Access the AOMaaS web interface at http://localhost:8000

## Production Deployment

### Using Kubernetes

For production deployments, we recommend using Kubernetes for better scalability, reliability, and manageability.

#### Prerequisites

- Kubernetes cluster (GKE, EKS, AKS, or self-hosted)
- kubectl configured to access your cluster
- Helm (optional, for easier deployment)

#### Deployment Steps

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/aomass.git
   cd aomass
   ```

2. Configure the deployment:

   ```bash
   cp k8s/values.example.yaml k8s/values.yaml
   ```

   Edit `k8s/values.yaml` to configure your deployment.

3. Deploy using Helm (if available):

   ```bash
   helm install aomass ./k8s/helm
   ```

   Or deploy using kubectl:

   ```bash
   kubectl apply -f k8s/manifests/
   ```

4. Set up the ingress controller and SSL certificate:

   ```bash
   kubectl apply -f k8s/ingress.yaml
   ```

5. Access the AOMaaS web interface at your configured domain.

### Using Docker Swarm

Docker Swarm is a simpler alternative to Kubernetes for production deployments.

1. Initialize a Docker Swarm cluster:

   ```bash
   docker swarm init
   ```

2. Deploy the AOMaaS stack:

   ```bash
   docker stack deploy -c docker-compose.prod.yml aomass
   ```

3. Set up a reverse proxy (e.g., Traefik, Nginx) for SSL termination and routing.

4. Access the AOMaaS web interface at your configured domain.

## Configuration

### Environment Variables

AOMaaS can be configured using environment variables. The following variables are available:

#### Application Settings

- `APP_NAME`: The name of the application (default: "AOMaaS")
- `APP_VERSION`: The version of the application (default: "0.1.0")
- `APP_ENV`: The environment (development, testing, production) (default: "development")
- `APP_DEBUG`: Enable debug mode (default: "True" in development, "False" in production)
- `APP_SECRET_KEY`: Secret key for JWT tokens and other security features

#### Database Settings

- `DB_HOST`: PostgreSQL host (default: "postgres")
- `DB_PORT`: PostgreSQL port (default: "5432")
- `DB_NAME`: PostgreSQL database name (default: "aomass")
- `DB_USER`: PostgreSQL username (default: "postgres")
- `DB_PASSWORD`: PostgreSQL password

#### Redis Settings

- `REDIS_HOST`: Redis host (default: "redis")
- `REDIS_PORT`: Redis port (default: "6379")
- `REDIS_DB`: Redis database number (default: "0")
- `REDIS_PASSWORD`: Redis password (optional)

#### Qdrant Settings

- `QDRANT_HOST`: Qdrant host (default: "qdrant")
- `QDRANT_PORT`: Qdrant port (default: "6333")
- `QDRANT_COLLECTION`: Qdrant collection name (default: "aomass")

#### MinIO Settings

- `MINIO_HOST`: MinIO host (default: "minio")
- `MINIO_PORT`: MinIO port (default: "9000")
- `MINIO_ACCESS_KEY`: MinIO access key
- `MINIO_SECRET_KEY`: MinIO secret key
- `MINIO_BUCKET`: MinIO bucket name (default: "aomass")

#### AI Service Settings

- `AI_SERVICE_TYPE`: AI service type (openai, azure, huggingface) (default: "openai")
- `AI_SERVICE_API_KEY`: AI service API key
- `AI_SERVICE_MODEL`: AI service model name (default: "gpt-4")

#### GitHub Settings

- `GITHUB_APP_ID`: GitHub App ID (for GitHub integration)
- `GITHUB_APP_PRIVATE_KEY`: GitHub App private key
- `GITHUB_APP_WEBHOOK_SECRET`: GitHub App webhook secret

### Configuration Files

In addition to environment variables, AOMaaS can be configured using configuration files:

- `config/settings.py`: Main configuration file
- `config/logging.py`: Logging configuration
- `config/security.py`: Security configuration

## Scaling

### Horizontal Scaling

AOMaaS is designed to scale horizontally. You can scale the following components:

#### API Server

```bash
# Kubernetes
kubectl scale deployment aomass-api --replicas=3

# Docker Swarm
docker service scale aomass_api=3
```

#### Task Workers

```bash
# Kubernetes
kubectl scale deployment aomass-worker --replicas=5

# Docker Swarm
docker service scale aomass_worker=5
```

### Vertical Scaling

You can also scale the resources allocated to each component:

```bash
# Kubernetes
kubectl edit deployment aomass-api
# Update the resources section

# Docker Swarm
docker service update --limit-cpu 2 --limit-memory 4G aomass_api
```

## Monitoring

### Health Checks

AOMaaS provides health check endpoints for monitoring the health of the services:

- `/health`: Overall health check
- `/health/db`: Database health check
- `/health/redis`: Redis health check
- `/health/qdrant`: Qdrant health check
- `/health/minio`: MinIO health check
- `/health/ai`: AI service health check

### Metrics

AOMaaS exposes Prometheus metrics at the `/metrics` endpoint. You can use Prometheus and Grafana to monitor the system.

### Logging

AOMaaS uses structured logging with JSON format. Logs are written to stdout/stderr and can be collected using your preferred logging solution (e.g., ELK, Loki, Datadog).

## Backup and Restore

### Database Backup

```bash
# PostgreSQL backup
pg_dump -h postgres -U postgres -d aomass -F c -f backup.dump

# Kubernetes
kubectl exec -it $(kubectl get pods -l app=postgres -o jsonpath='{.items[0].metadata.name}') -- pg_dump -U postgres -d aomass -F c -f /tmp/backup.dump
kubectl cp $(kubectl get pods -l app=postgres -o jsonpath='{.items[0].metadata.name}'):/tmp/backup.dump backup.dump
```

### Database Restore

```bash
# PostgreSQL restore
pg_restore -h postgres -U postgres -d aomass -c backup.dump

# Kubernetes
kubectl cp backup.dump $(kubectl get pods -l app=postgres -o jsonpath='{.items[0].metadata.name}'):/tmp/backup.dump
kubectl exec -it $(kubectl get pods -l app=postgres -o jsonpath='{.items[0].metadata.name}') -- pg_restore -U postgres -d aomass -c /tmp/backup.dump
```

### Object Store Backup

```bash
# MinIO backup
mc mirror minio/aomass backup/

# Kubernetes
kubectl exec -it $(kubectl get pods -l app=minio -o jsonpath='{.items[0].metadata.name}') -- mc mirror /data/aomass /tmp/backup
kubectl cp $(kubectl get pods -l app=minio -o jsonpath='{.items[0].metadata.name}'):/tmp/backup backup/
```

## Troubleshooting

### Common Issues

#### API Server Not Starting

**Problem**: The API server fails to start.

**Solution**: Check the logs for errors:

```bash
# Docker Compose
docker-compose logs api

# Kubernetes
kubectl logs -l app=aomass-api
```

Common issues include:
- Database connection errors
- Missing environment variables
- Port conflicts

#### Worker Not Processing Tasks

**Problem**: Tasks are not being processed by the worker.

**Solution**: Check the worker logs:

```bash
# Docker Compose
docker-compose logs worker

# Kubernetes
kubectl logs -l app=aomass-worker
```

Common issues include:
- Redis connection errors
- Task queue configuration issues
- Worker process crashes

#### Database Migration Errors

**Problem**: Database migration fails.

**Solution**: Check the migration logs and manually fix the issues:

```bash
# Docker Compose
docker-compose logs api | grep migration

# Kubernetes
kubectl logs -l app=aomass-api | grep migration
```

## Security Considerations

### Secrets Management

Store sensitive information (API keys, passwords) securely:

- In development: Use `.env` files (not committed to version control)
- In production: Use Kubernetes Secrets or Docker Swarm Secrets

### Network Security

- Use TLS for all external communication
- Implement network policies to restrict communication between services
- Use a Web Application Firewall (WAF) for additional protection

### Access Control

- Implement role-based access control (RBAC)
- Use the principle of least privilege
- Regularly audit access logs

## Upgrading

### Minor Upgrades

For minor upgrades (patch versions):

```bash
# Docker Compose
git pull
docker-compose build
docker-compose up -d

# Kubernetes
git pull
kubectl apply -f k8s/manifests/
```

### Major Upgrades

For major upgrades:

1. Backup the database and object store
2. Follow the upgrade instructions in the release notes
3. Test the upgrade in a staging environment before applying to production

## Support

If you encounter any issues with deployment, please:

1. Check the [Documentation](README.md) for information
2. Open an issue on the [GitHub repository](https://github.com/yourusername/aomass/issues)
3. Contact support at support@aomass.ai