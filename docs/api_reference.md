# AOMaaS API Reference

This document provides a comprehensive reference for the AOMaaS (Autonomous Open-Source Maintainer as a Service) API.

## Base URL

All API endpoints are relative to the base URL:

```
http://localhost:8000/api/v1
```

For production deployments, replace `localhost:8000` with your actual domain.

## Authentication

AOMaaS API uses OAuth2 with Bearer token authentication. To authenticate:

1. Obtain an access token by sending a POST request to `/api/v1/auth/token`
2. Include the token in the Authorization header of subsequent requests:
   `Authorization: Bearer {your_access_token}`

### Authentication Endpoints

#### POST /auth/token

Obtain an access token.

**Request:**

```json
{
  "username": "your_username",
  "password": "your_password"
}
```

**Response:**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

#### GET /auth/me

Get information about the currently authenticated user.

**Response:**

```json
{
  "username": "demo",
  "email": "demo@aomass.ai",
  "full_name": "Demo User",
  "disabled": false
}
```

## Repository Management

### POST /repositories/index

Index a repository for analysis.

**Request:**

```json
{
  "repository_url": "https://github.com/username/repository",
  "provider_type": "github",
  "branch": "main"
}
```

**Response:**

```json
{
  "task_id": "123e4567-e89b-12d3-a456-426614174000",
  "status": "pending",
  "repository_id": "123e4567-e89b-12d3-a456-426614174001"
}
```

### POST /repositories/mine-opportunities

Mine maintenance opportunities from an indexed repository.

**Request:**

```json
{
  "repository_id": "123e4567-e89b-12d3-a456-426614174001",
  "opportunity_types": ["security", "performance", "documentation"],
  "max_opportunities": 10
}
```

**Response:**

```json
{
  "task_id": "123e4567-e89b-12d3-a456-426614174002",
  "status": "pending"
}
```

### GET /repositories/{repository_id}/opportunities

Get maintenance opportunities for a repository.

**Response:**

```json
{
  "opportunities": [
    {
      "id": "123e4567-e89b-12d3-a456-426614174003",
      "title": "Fix security vulnerability in authentication module",
      "description": "The authentication module uses an outdated encryption algorithm that is vulnerable to attacks.",
      "type": "security",
      "priority": "high",
      "effort_estimate": "medium",
      "location": "src/auth/login.js"
    },
    {
      "id": "123e4567-e89b-12d3-a456-426614174004",
      "title": "Optimize database query performance",
      "description": "The query in the user service is not using indexes properly, causing slow performance.",
      "type": "performance",
      "priority": "medium",
      "effort_estimate": "small",
      "location": "src/services/user.js"
    }
  ]
}
```

## Maintenance Planning

### POST /plans/generate

Generate an implementation plan for an opportunity.

**Request:**

```json
{
  "opportunity_id": "123e4567-e89b-12d3-a456-426614174003",
  "max_steps": 5
}
```

**Response:**

```json
{
  "task_id": "123e4567-e89b-12d3-a456-426614174005",
  "status": "pending",
  "plan_id": "123e4567-e89b-12d3-a456-426614174006"
}
```

### GET /plans/{plan_id}

Get a generated implementation plan.

**Response:**

```json
{
  "id": "123e4567-e89b-12d3-a456-426614174006",
  "opportunity_id": "123e4567-e89b-12d3-a456-426614174003",
  "title": "Fix security vulnerability in authentication module",
  "description": "Implementation plan to update the encryption algorithm in the authentication module.",
  "steps": [
    {
      "id": 1,
      "title": "Update encryption library",
      "description": "Update the encryption library to the latest version."
    },
    {
      "id": 2,
      "title": "Replace encryption algorithm",
      "description": "Replace the outdated algorithm with a modern, secure alternative."
    },
    {
      "id": 3,
      "title": "Update tests",
      "description": "Update the tests to verify the new encryption algorithm."
    }
  ]
}
```

## Implementation

### POST /implementations/create

Implement a plan.

**Request:**

```json
{
  "plan_id": "123e4567-e89b-12d3-a456-426614174006",
  "branch_name": "fix/security-vulnerability"
}
```

**Response:**

```json
{
  "task_id": "123e4567-e89b-12d3-a456-426614174007",
  "status": "pending",
  "implementation_id": "123e4567-e89b-12d3-a456-426614174008"
}
```

### GET /implementations/{implementation_id}

Get implementation details.

**Response:**

```json
{
  "id": "123e4567-e89b-12d3-a456-426614174008",
  "plan_id": "123e4567-e89b-12d3-a456-426614174006",
  "branch_name": "fix/security-vulnerability",
  "status": "completed",
  "files_changed": [
    "src/auth/login.js",
    "tests/auth/login.test.js"
  ],
  "commit_id": "abc123def456"
}
```

## Pull Requests

### POST /pull-requests/create

Create a pull request for an implementation.

**Request:**

```json
{
  "implementation_id": "123e4567-e89b-12d3-a456-426614174008",
  "title": "Fix security vulnerability in authentication module",
  "description": "This PR updates the encryption algorithm in the authentication module to address a security vulnerability.",
  "draft": false,
  "provider_type": "github"
}
```

**Response:**

```json
{
  "pr_id": "123e4567-e89b-12d3-a456-426614174009",
  "provider_type": "github",
  "provider_pr_number": "42",
  "url": "https://github.com/username/repository/pull/42",
  "status": "open"
}
```

### POST /pull-requests/{pr_id}/review

Review a pull request.

**Request:**

```json
{
  "review_type": "security"
}
```

**Response:**

```json
{
  "task_id": "123e4567-e89b-12d3-a456-426614174010",
  "status": "pending"
}
```

## Task Status

### GET /tasks/{task_id}

Get the status of a long-running task.

**Response:**

```json
{
  "id": "123e4567-e89b-12d3-a456-426614174010",
  "status": "completed",
  "result": {
    "success": true,
    "message": "Task completed successfully",
    "data": {}
  },
  "created_at": "2023-06-01T12:00:00Z",
  "updated_at": "2023-06-01T12:05:00Z"
}
```

## Error Handling

The API uses standard HTTP status codes to indicate the success or failure of requests:

- 200 OK: The request was successful
- 201 Created: The resource was created successfully
- 400 Bad Request: The request was invalid
- 401 Unauthorized: Authentication failed
- 403 Forbidden: The authenticated user does not have permission to access the resource
- 404 Not Found: The requested resource was not found
- 500 Internal Server Error: An error occurred on the server

Error responses include a JSON object with details about the error:

```json
{
  "detail": "Error message",
  "type": "ErrorType"
}
```

## Rate Limiting

The API implements rate limiting to prevent abuse. The current limits are:

- 100 requests per minute per IP address
- 1000 requests per hour per user

When a rate limit is exceeded, the API returns a 429 Too Many Requests status code.

## Versioning

The API is versioned using the URL path (e.g., `/api/v1`). When breaking changes are introduced, a new version will be released (e.g., `/api/v2`).