# API Reference

## Overview

AOMaaS provides a comprehensive REST API for autonomous repository maintenance. All endpoints return JSON responses and follow standard HTTP status codes.

**Base URL:** 

## Authentication

Currently, AOMaaS operates without authentication for development. In production, API keys or OAuth2 tokens will be required.

## Endpoints

### Health Check



Check the health status of AOMaaS services.

**Response:**


### Index Repository



Index a GitHub repository for analysis and opportunity mining.

**Request Body:**


**Response:**


### Mine Opportunities



Mine maintenance opportunities from an indexed repository.

**Request Body:**


**Response:**


### Generate Plan



Generate an implementation plan for a maintenance opportunity.

**Request Body:**


**Response:**


### Implement Plan



Implement a generated plan.

**Request Body:**


**Response:**


### Create Pull Request



Create a GitHub pull request for implemented changes.

**Request Body:**


**Response:**


### Review Pull Request



Conduct AI-powered review of a pull request.

**Request Body:**


**Response:**


### Get Task Status



Get the status of a background task.

**Response:**


## Error Responses

All endpoints return standard HTTP status codes:

-  - Success
-  - Bad Request
-  - Not Found
-  - Validation Error
-  - Internal Server Error

Error responses include details:



## Rate Limiting

API endpoints are rate limited to prevent abuse:

- 100 requests per minute for index operations
- 1000 requests per minute for read operations
- 500 requests per minute for write operations

Rate limit headers are included in responses:


