# Getting Started with AOMaaS

## Introduction

AOMaaS (Autonomous Open-Source Maintainer as a Service) helps you maintain open-source projects by automatically identifying maintenance opportunities, generating implementation plans, and creating pull requests. This guide will help you get started with AOMaaS.

## Prerequisites

- Docker and Docker Compose installed on your system
- Git installed on your system
- A GitHub account (for GitHub integration)

## Installation

### Using Docker Compose (Recommended)

1. Clone the AOMaaS repository:

   ```bash
   git clone https://github.com/yourusername/aomass.git
   cd aomass
   ```

2. Run the deployment script:

   ```bash
   ./scripts/deploy-frontend.sh
   ```

   This script will build the Docker images and start all the required services.

3. Access the AOMaaS web interface at http://localhost:8000

### Manual Installation

1. Clone the AOMaaS repository:

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

4. Start the application:

   ```bash
   uvicorn src.aomass.main:app --reload
   ```

5. Access the AOMaaS web interface at http://localhost:8000

## Quick Start

### 1. Create an Account

1. Navigate to http://localhost:8000
2. Click on the "Sign Up" button
3. Fill in your details and create an account

### 2. Connect a Repository

1. Log in to your AOMaaS account
2. Navigate to the Dashboard
3. Click on "Add Repository"
4. Enter the repository URL and select the provider (GitHub, GitLab, etc.)
5. Click "Connect"

### 3. Mine Maintenance Opportunities

1. Select the connected repository from your Dashboard
2. Click on "Mine Opportunities"
3. Select the types of opportunities you want to mine (security, performance, documentation, etc.)
4. Click "Start Mining"
5. Wait for the mining process to complete

### 4. Review and Implement Opportunities

1. Once the mining process is complete, you'll see a list of maintenance opportunities
2. Click on an opportunity to view its details
3. Click "Generate Plan" to create an implementation plan
4. Review the plan and click "Implement" to automatically implement the plan
5. Once the implementation is complete, click "Create PR" to create a pull request

## API Usage

AOMaaS provides a comprehensive API for integrating with your own tools and workflows. See the [API Reference](api_reference.md) for detailed information.

Here's a simple example of using the API to index a repository:

```python
import requests

# Get an access token
response = requests.post(
    "http://localhost:8000/api/v1/auth/token",
    data={"username": "your_username", "password": "your_password"}
)
token = response.json()["access_token"]

# Index a repository
headers = {"Authorization": f"Bearer {token}"}
response = requests.post(
    "http://localhost:8000/api/v1/repositories/index",
    headers=headers,
    json={
        "repository_url": "https://github.com/username/repository",
        "provider_type": "github",
        "branch": "main"
    }
)
print(response.json())
```

## Next Steps

- Explore the [API Reference](api_reference.md) for more advanced usage
- Learn about the [Architecture](architecture.md) of AOMaaS
- Check out the [Deployment](deployment.md) guide for production deployment

## Troubleshooting

### Common Issues

#### Connection Issues

**Problem**: Unable to connect to the AOMaaS web interface.

**Solution**: Ensure that all the required services are running. You can check the status of the services using:

```bash
docker-compose ps
```

#### Authentication Issues

**Problem**: Unable to authenticate with the API.

**Solution**: Ensure that you're using the correct username and password. If you've forgotten your password, use the "Forgot Password" feature on the login page.

#### Repository Indexing Issues

**Problem**: Repository indexing fails.

**Solution**: Ensure that the repository URL is correct and that you have the necessary permissions to access the repository. Check the logs for more information:

```bash
docker-compose logs api
```

## Getting Help

If you encounter any issues or have questions, please:

1. Check the [Documentation](README.md) for information
2. Open an issue on the [GitHub repository](https://github.com/yourusername/aomass/issues)
3. Contact support at support@aomass.ai