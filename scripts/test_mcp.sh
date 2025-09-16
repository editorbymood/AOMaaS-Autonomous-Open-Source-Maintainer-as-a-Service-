#!/bin/bash

# Test script for Multi-Cloud Provider (MCP) architecture

echo "Running MCP integration tests..."

# Set environment variables (replace with your actual tokens)
export GITHUB_TOKEN="your_github_token"
export GITLAB_TOKEN="your_gitlab_token"

# Run the tests
python -m pytest tests/integration/test_github_provider.py -v
python -m pytest tests/integration/test_gitlab_provider.py -v
python -m pytest tests/integration/test_mcp_integration.py -v

echo "MCP tests completed!"