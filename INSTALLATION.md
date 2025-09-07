# 📦 AOMaaS Dependencies Installation Guide

## 🎯 Quick Installation Commands

### Option 1: Install All Dependencies (Recommended for Development)
```bash
pip install -r requirements.txt
```

### Option 2: Install Core + Development Dependencies  
```bash
pip install -r requirements-dev.txt
```

### Option 3: Production Only (Minimal)
```bash
pip install -r requirements-prod.txt
```

### Option 4: Using pyproject.toml (Editable Install)
```bash
# Install core dependencies
pip install -e .

# Install with development tools
pip install -e ".[dev]"

# Install with full features
pip install -e ".[full,dev]"
```

## 🔧 Virtual Environment Setup (Recommended)

```bash
# Create virtual environment
python3.11 -m venv venv

# Activate (Mac/Linux)
source venv/bin/activate

# Activate (Windows)
# venv\Scriptsctivate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

## 📊 Requirements Breakdown

### 📱 Core API Dependencies (Always Required)
- **fastapi** - Web framework
- **uvicorn** - ASGI server
- **pydantic** - Data validation
- **httpx** - HTTP client
- **redis** - Caching & queues
- **typer** - CLI framework
- **rich** - Terminal formatting

### 🤖 AI & Analysis Dependencies
- **openai** - OpenAI API client
- **anthropic** - Anthropic API client
- **qdrant-client** - Vector database
- **tree-sitter** - Code parsing
- **pygithub** - GitHub integration

### 🗄️ Storage & Database
- **sqlalchemy** - SQL toolkit
- **asyncpg** - PostgreSQL driver
- **minio** - Object storage
- **alembic** - Database migrations

### ⚙️ Background Processing
- **celery** - Task queue
- **kombu** - Message transport
- **billiard** - Process pools

### 🧪 Development Tools
- **pytest** - Testing framework
- **black** - Code formatter
- **mypy** - Type checker
- **ruff** - Fast linter

## 🚀 Platform-Specific Instructions

### macOS
```bash
# Install system dependencies
brew install python@3.11 redis postgresql

# Create and activate virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install AOMaaS dependencies
pip install -r requirements.txt
```

### Ubuntu/Debian
```bash
# Install system dependencies
sudo apt update
sudo apt install python3.11 python3.11-venv python3.11-dev
sudo apt install redis-server postgresql postgresql-contrib

# Create and activate virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install AOMaaS dependencies
pip install -r requirements.txt
```

### Windows
```powershell
# Install Python 3.11 from python.org
# Create virtual environment
python -m venv venv
venv\Scriptsctivate

# Install dependencies
pip install -r requirements.txt
```

## 🐳 Docker Installation (Easiest)

```bash
# Build and run with Docker Compose (includes all dependencies)
docker-compose up -d

# Or build manually
docker build -t aomass .
docker run -p 8000:8000 aomass
```

## 🔍 Verify Installation

```bash
# Test core imports
python -c "import fastapi, uvicorn, pydantic, redis; print('✅ Core dependencies OK')"

# Test AI dependencies
python -c "import openai, anthropic; print('✅ AI dependencies OK')"

# Test database dependencies  
python -c "import sqlalchemy, qdrant_client; print('✅ Database dependencies OK')"

# Run AOMaaS health check
python -c "
from fastapi.testclient import TestClient
from simple_app import app
client = TestClient(app)
response = client.get('/health')
print(f'✅ AOMaaS Status: {response.json()["status"]}')
"
```

## ⚠️ Common Issues & Solutions

### 1. Python Version Issues
```bash
# Ensure Python 3.11+
python --version
# If not 3.11+, install from python.org or use pyenv
```

### 2. Tree-sitter Compilation Issues
```bash
# Install system build tools
# macOS:
xcode-select --install

# Ubuntu:
sudo apt install build-essential

# Windows:
# Install Visual Studio Build Tools
```

### 3. Redis Connection Issues
```bash
# Start Redis server
# macOS:
brew services start redis

# Ubuntu:
sudo systemctl start redis-server

# Or use Docker:
docker run -d -p 6379:6379 redis:alpine
```

### 4. PostgreSQL Issues
```bash
# Start PostgreSQL
# macOS:
brew services start postgresql

# Ubuntu:
sudo systemctl start postgresql

# Or use Docker:
docker run -d -p 5432:5432 -e POSTGRES_PASSWORD=password postgres:15
```

## 📈 Performance Optimization

### For Production:
```bash
# Install with production optimizations
pip install -r requirements-prod.txt

# Use faster JSON serialization
pip install orjson

# Use compiled packages where available
pip install --prefer-binary -r requirements-prod.txt
```

### For Development:
```bash
# Install with all development tools
pip install -r requirements-dev.txt

# Enable pre-commit hooks
pre-commit install
```

## 🎯 Next Steps After Installation

1. **Configure environment**: Copy  to 
2. **Start services**: Run  for full stack
3. **Test API**: Run 
4. **Access docs**: Open 
5. **Run tests**: Execute 

## 💡 Pro Tips

- Use **virtual environments** to avoid conflicts
- Install **requirements-dev.txt** for full development experience
- Use **Docker** for the easiest setup with all services
- Check **system dependencies** (Redis, PostgreSQL) before installing Python packages
- Update regularly: 

Happy coding with AOMaaS! 🤖⚡
