# Installation Guide

## Prerequisites

- **Python 3.11+** - Required for running AOMaaS
- **Docker & Docker Compose** - Required for running dependencies
- **Git** - For cloning repositories
- **GitHub Token** - For GitHub integration (optional for development)

## Quick Start

### 1. Clone the Repository



### 2. Development Setup

Run the development setup script:

🛠️ Setting up AOMaaS development environment...
[2025-08-31 00:18:14] 
[2025-08-31 00:18:14] 
[2025-08-31 00:18:14] 

This will:
- Create a Python virtual environment
- Install dependencies
- Set up pre-commit hooks
- Start required services (PostgreSQL, Redis, Qdrant, MinIO)
- Create configuration files

### 3. Configuration

Edit the  file with your settings:



### 4. Start the API Server



### 5. Start Background Workers

In a separate terminal:



## Production Deployment

### Using Docker Compose

1. **Configure Environment**



2. **Deploy Services**

🚀 Starting AOMaaS deployment...
[2025-08-31 00:17:44] 
[ERROR] 

3. **Verify Deployment**



### Manual Deployment

1. **Install Dependencies**



2. **Start Services**



## Using the CLI

Install the CLI tool:



Basic usage:



## Verification

Test the installation:



## Service URLs

After successful installation:

- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **MinIO Console**: http://localhost:9001 (admin/password)
- **Qdrant Dashboard**: http://localhost:6333/dashboard
- **Flower (Celery)**: http://localhost:5555

## Troubleshooting

### Common Issues

1. **Port Conflicts**
   

2. **Docker Issues**
   🚀 Starting AOMaaS deployment...
[2025-08-31 00:17:44] 
[ERROR] 

3. **Permission Issues**
   

4. **Python Version Issues**
   Obtaining file:///Users/shanky/aomass
  Installing build dependencies: started
  Installing build dependencies: finished with status 'done'
  Checking if build backend supports build_editable: started
  Checking if build backend supports build_editable: finished with status 'done'
  Getting requirements to build editable: started
  Getting requirements to build editable: finished with status 'done'
  Preparing editable metadata (pyproject.toml): started
  Preparing editable metadata (pyproject.toml): finished with status 'done'
Collecting fastapi>=0.104.0 (from aomass==0.1.0)
  Using cached fastapi-0.116.1-py3-none-any.whl.metadata (28 kB)
Collecting uvicorn>=0.24.0 (from uvicorn[standard]>=0.24.0->aomass==0.1.0)
  Using cached uvicorn-0.35.0-py3-none-any.whl.metadata (6.5 kB)
Collecting pydantic>=2.5.0 (from aomass==0.1.0)
  Using cached pydantic-2.11.7-py3-none-any.whl.metadata (67 kB)
Collecting redis>=5.0.0 (from aomass==0.1.0)
  Using cached redis-6.4.0-py3-none-any.whl.metadata (10 kB)
Collecting qdrant-client>=1.7.0 (from aomass==0.1.0)
  Downloading qdrant_client-1.15.1-py3-none-any.whl.metadata (11 kB)
Collecting minio>=7.2.0 (from aomass==0.1.0)
  Downloading minio-7.2.16-py3-none-any.whl.metadata (6.5 kB)
Collecting celery>=5.3.0 (from aomass==0.1.0)
  Using cached celery-5.5.3-py3-none-any.whl.metadata (22 kB)
Collecting asyncpg>=0.29.0 (from aomass==0.1.0)
  Downloading asyncpg-0.30.0-cp311-cp311-macosx_11_0_arm64.whl.metadata (5.0 kB)
Collecting sqlalchemy>=2.0.0 (from aomass==0.1.0)
  Downloading sqlalchemy-2.0.43-cp311-cp311-macosx_11_0_arm64.whl.metadata (9.6 kB)
Collecting alembic>=1.13.0 (from aomass==0.1.0)
  Downloading alembic-1.16.5-py3-none-any.whl.metadata (7.3 kB)
Collecting httpx>=0.25.0 (from aomass==0.1.0)
  Using cached httpx-0.28.1-py3-none-any.whl.metadata (7.1 kB)
Collecting aiofiles>=23.2.0 (from aomass==0.1.0)
  Downloading aiofiles-24.1.0-py3-none-any.whl.metadata (10 kB)
Collecting tree-sitter>=0.20.0 (from aomass==0.1.0)
  Downloading tree_sitter-0.25.1-cp311-cp311-macosx_11_0_arm64.whl.metadata (10.0 kB)
Collecting pygithub>=2.1.0 (from aomass==0.1.0)
  Downloading pygithub-2.7.0-py3-none-any.whl.metadata (3.9 kB)
Collecting openai>=1.3.0 (from aomass==0.1.0)
  Downloading openai-1.102.0-py3-none-any.whl.metadata (29 kB)
Collecting anthropic>=0.7.0 (from aomass==0.1.0)
  Downloading anthropic-0.64.0-py3-none-any.whl.metadata (27 kB)
Collecting python-dotenv>=1.0.0 (from aomass==0.1.0)
  Using cached python_dotenv-1.1.1-py3-none-any.whl.metadata (24 kB)
Collecting typer>=0.9.0 (from aomass==0.1.0)
  Downloading typer-0.17.3-py3-none-any.whl.metadata (15 kB)
Collecting rich>=13.7.0 (from aomass==0.1.0)
  Downloading rich-14.1.0-py3-none-any.whl.metadata (18 kB)
Collecting structlog>=23.2.0 (from aomass==0.1.0)
  Downloading structlog-25.4.0-py3-none-any.whl.metadata (7.6 kB)
Collecting pyyaml>=6.0.1 (from aomass==0.1.0)
  Downloading PyYAML-6.0.2-cp311-cp311-macosx_11_0_arm64.whl.metadata (2.1 kB)
Collecting Mako (from alembic>=1.13.0->aomass==0.1.0)
  Downloading mako-1.3.10-py3-none-any.whl.metadata (2.9 kB)
Collecting typing-extensions>=4.12 (from alembic>=1.13.0->aomass==0.1.0)
  Using cached typing_extensions-4.15.0-py3-none-any.whl.metadata (3.3 kB)
Collecting anyio<5,>=3.5.0 (from anthropic>=0.7.0->aomass==0.1.0)
  Using cached anyio-4.10.0-py3-none-any.whl.metadata (4.0 kB)
Collecting distro<2,>=1.7.0 (from anthropic>=0.7.0->aomass==0.1.0)
  Downloading distro-1.9.0-py3-none-any.whl.metadata (6.8 kB)
Collecting jiter<1,>=0.4.0 (from anthropic>=0.7.0->aomass==0.1.0)
  Downloading jiter-0.10.0-cp311-cp311-macosx_11_0_arm64.whl.metadata (5.2 kB)
Collecting sniffio (from anthropic>=0.7.0->aomass==0.1.0)
  Using cached sniffio-1.3.1-py3-none-any.whl.metadata (3.9 kB)
Collecting idna>=2.8 (from anyio<5,>=3.5.0->anthropic>=0.7.0->aomass==0.1.0)
  Using cached idna-3.10-py3-none-any.whl.metadata (10 kB)
Collecting certifi (from httpx>=0.25.0->aomass==0.1.0)
  Using cached certifi-2025.8.3-py3-none-any.whl.metadata (2.4 kB)
Collecting httpcore==1.* (from httpx>=0.25.0->aomass==0.1.0)
  Using cached httpcore-1.0.9-py3-none-any.whl.metadata (21 kB)
Collecting h11>=0.16 (from httpcore==1.*->httpx>=0.25.0->aomass==0.1.0)
  Using cached h11-0.16.0-py3-none-any.whl.metadata (8.3 kB)
Collecting annotated-types>=0.6.0 (from pydantic>=2.5.0->aomass==0.1.0)
  Using cached annotated_types-0.7.0-py3-none-any.whl.metadata (15 kB)
Collecting pydantic-core==2.33.2 (from pydantic>=2.5.0->aomass==0.1.0)
  Downloading pydantic_core-2.33.2-cp311-cp311-macosx_11_0_arm64.whl.metadata (6.8 kB)
Collecting typing-inspection>=0.4.0 (from pydantic>=2.5.0->aomass==0.1.0)
  Using cached typing_inspection-0.4.1-py3-none-any.whl.metadata (2.6 kB)
Collecting billiard<5.0,>=4.2.1 (from celery>=5.3.0->aomass==0.1.0)
  Using cached billiard-4.2.1-py3-none-any.whl.metadata (4.4 kB)
Collecting kombu<5.6,>=5.5.2 (from celery>=5.3.0->aomass==0.1.0)
  Using cached kombu-5.5.4-py3-none-any.whl.metadata (3.5 kB)
Collecting vine<6.0,>=5.1.0 (from celery>=5.3.0->aomass==0.1.0)
  Using cached vine-5.1.0-py3-none-any.whl.metadata (2.7 kB)
Collecting click<9.0,>=8.1.2 (from celery>=5.3.0->aomass==0.1.0)
  Downloading click-8.2.1-py3-none-any.whl.metadata (2.5 kB)
Collecting click-didyoumean>=0.3.0 (from celery>=5.3.0->aomass==0.1.0)
  Using cached click_didyoumean-0.3.1-py3-none-any.whl.metadata (3.9 kB)
Collecting click-repl>=0.2.0 (from celery>=5.3.0->aomass==0.1.0)
  Using cached click_repl-0.3.0-py3-none-any.whl.metadata (3.6 kB)
Collecting click-plugins>=1.1.1 (from celery>=5.3.0->aomass==0.1.0)
  Using cached click_plugins-1.1.1.2-py2.py3-none-any.whl.metadata (6.5 kB)
Collecting python-dateutil>=2.8.2 (from celery>=5.3.0->aomass==0.1.0)
  Using cached python_dateutil-2.9.0.post0-py2.py3-none-any.whl.metadata (8.4 kB)
Collecting amqp<6.0.0,>=5.1.1 (from kombu<5.6,>=5.5.2->celery>=5.3.0->aomass==0.1.0)
  Using cached amqp-5.3.1-py3-none-any.whl.metadata (8.9 kB)
Collecting tzdata>=2025.2 (from kombu<5.6,>=5.5.2->celery>=5.3.0->aomass==0.1.0)
  Using cached tzdata-2025.2-py2.py3-none-any.whl.metadata (1.4 kB)
Collecting packaging (from kombu<5.6,>=5.5.2->celery>=5.3.0->aomass==0.1.0)
  Using cached packaging-25.0-py3-none-any.whl.metadata (3.3 kB)
Collecting prompt-toolkit>=3.0.36 (from click-repl>=0.2.0->celery>=5.3.0->aomass==0.1.0)
  Using cached prompt_toolkit-3.0.52-py3-none-any.whl.metadata (6.4 kB)
Collecting starlette<0.48.0,>=0.40.0 (from fastapi>=0.104.0->aomass==0.1.0)
  Using cached starlette-0.47.3-py3-none-any.whl.metadata (6.2 kB)
Collecting argon2-cffi (from minio>=7.2.0->aomass==0.1.0)
  Using cached argon2_cffi-25.1.0-py3-none-any.whl.metadata (4.1 kB)
Collecting pycryptodome (from minio>=7.2.0->aomass==0.1.0)
  Downloading pycryptodome-3.23.0-cp37-abi3-macosx_10_9_universal2.whl.metadata (3.4 kB)
Collecting urllib3 (from minio>=7.2.0->aomass==0.1.0)
  Using cached urllib3-2.5.0-py3-none-any.whl.metadata (6.5 kB)
Collecting tqdm>4 (from openai>=1.3.0->aomass==0.1.0)
  Using cached tqdm-4.67.1-py3-none-any.whl.metadata (57 kB)
Collecting wcwidth (from prompt-toolkit>=3.0.36->click-repl>=0.2.0->celery>=5.3.0->aomass==0.1.0)
  Using cached wcwidth-0.2.13-py2.py3-none-any.whl.metadata (14 kB)
Collecting pynacl>=1.4.0 (from pygithub>=2.1.0->aomass==0.1.0)
  Downloading PyNaCl-1.5.0-cp36-abi3-macosx_10_10_universal2.whl.metadata (8.7 kB)
Collecting requests>=2.14.0 (from pygithub>=2.1.0->aomass==0.1.0)
  Using cached requests-2.32.5-py3-none-any.whl.metadata (4.9 kB)
Collecting pyjwt>=2.4.0 (from pyjwt[crypto]>=2.4.0->pygithub>=2.1.0->aomass==0.1.0)
  Downloading PyJWT-2.10.1-py3-none-any.whl.metadata (4.0 kB)
Collecting cryptography>=3.4.0 (from pyjwt[crypto]>=2.4.0->pygithub>=2.1.0->aomass==0.1.0)
  Downloading cryptography-45.0.6-cp311-abi3-macosx_10_9_universal2.whl.metadata (5.7 kB)
Collecting cffi>=1.14 (from cryptography>=3.4.0->pyjwt[crypto]>=2.4.0->pygithub>=2.1.0->aomass==0.1.0)
  Downloading cffi-1.17.1-cp311-cp311-macosx_11_0_arm64.whl.metadata (1.5 kB)
Collecting pycparser (from cffi>=1.14->cryptography>=3.4.0->pyjwt[crypto]>=2.4.0->pygithub>=2.1.0->aomass==0.1.0)
  Using cached pycparser-2.22-py3-none-any.whl.metadata (943 bytes)
Collecting six>=1.5 (from python-dateutil>=2.8.2->celery>=5.3.0->aomass==0.1.0)
  Using cached six-1.17.0-py2.py3-none-any.whl.metadata (1.7 kB)
Collecting grpcio>=1.41.0 (from qdrant-client>=1.7.0->aomass==0.1.0)
  Downloading grpcio-1.74.0-cp311-cp311-macosx_11_0_universal2.whl.metadata (3.8 kB)
Collecting numpy>=1.21 (from qdrant-client>=1.7.0->aomass==0.1.0)
  Downloading numpy-2.3.2-cp311-cp311-macosx_14_0_arm64.whl.metadata (62 kB)
Collecting portalocker<4.0,>=2.7.0 (from qdrant-client>=1.7.0->aomass==0.1.0)
  Downloading portalocker-3.2.0-py3-none-any.whl.metadata (8.7 kB)
Collecting protobuf>=3.20.0 (from qdrant-client>=1.7.0->aomass==0.1.0)
  Using cached protobuf-6.32.0-cp39-abi3-macosx_10_9_universal2.whl.metadata (593 bytes)
Collecting h2<5,>=3 (from httpx[http2]>=0.20.0->qdrant-client>=1.7.0->aomass==0.1.0)
  Downloading h2-4.3.0-py3-none-any.whl.metadata (5.1 kB)
Collecting hyperframe<7,>=6.1 (from h2<5,>=3->httpx[http2]>=0.20.0->qdrant-client>=1.7.0->aomass==0.1.0)
  Downloading hyperframe-6.1.0-py3-none-any.whl.metadata (4.3 kB)
Collecting hpack<5,>=4.1 (from h2<5,>=3->httpx[http2]>=0.20.0->qdrant-client>=1.7.0->aomass==0.1.0)
  Downloading hpack-4.1.0-py3-none-any.whl.metadata (4.6 kB)
Collecting charset_normalizer<4,>=2 (from requests>=2.14.0->pygithub>=2.1.0->aomass==0.1.0)
  Downloading charset_normalizer-3.4.3-cp311-cp311-macosx_10_9_universal2.whl.metadata (36 kB)
Collecting markdown-it-py>=2.2.0 (from rich>=13.7.0->aomass==0.1.0)
  Downloading markdown_it_py-4.0.0-py3-none-any.whl.metadata (7.3 kB)
Collecting pygments<3.0.0,>=2.13.0 (from rich>=13.7.0->aomass==0.1.0)
  Using cached pygments-2.19.2-py3-none-any.whl.metadata (2.5 kB)
Collecting mdurl~=0.1 (from markdown-it-py>=2.2.0->rich>=13.7.0->aomass==0.1.0)
  Downloading mdurl-0.1.2-py3-none-any.whl.metadata (1.6 kB)
Collecting shellingham>=1.3.0 (from typer>=0.9.0->aomass==0.1.0)
  Downloading shellingham-1.5.4-py2.py3-none-any.whl.metadata (3.5 kB)
Collecting httptools>=0.6.3 (from uvicorn[standard]>=0.24.0->aomass==0.1.0)
  Downloading httptools-0.6.4-cp311-cp311-macosx_11_0_arm64.whl.metadata (3.6 kB)
Collecting uvloop>=0.15.1 (from uvicorn[standard]>=0.24.0->aomass==0.1.0)
  Downloading uvloop-0.21.0-cp311-cp311-macosx_10_9_universal2.whl.metadata (4.9 kB)
Collecting watchfiles>=0.13 (from uvicorn[standard]>=0.24.0->aomass==0.1.0)
  Downloading watchfiles-1.1.0-cp311-cp311-macosx_11_0_arm64.whl.metadata (4.9 kB)
Collecting websockets>=10.4 (from uvicorn[standard]>=0.24.0->aomass==0.1.0)
  Downloading websockets-15.0.1-cp311-cp311-macosx_11_0_arm64.whl.metadata (6.8 kB)
Collecting argon2-cffi-bindings (from argon2-cffi->minio>=7.2.0->aomass==0.1.0)
  Using cached argon2_cffi_bindings-25.1.0-cp39-abi3-macosx_11_0_arm64.whl.metadata (7.4 kB)
Collecting MarkupSafe>=0.9.2 (from Mako->alembic>=1.13.0->aomass==0.1.0)
  Downloading MarkupSafe-3.0.2-cp311-cp311-macosx_11_0_arm64.whl.metadata (4.0 kB)
Downloading aiofiles-24.1.0-py3-none-any.whl (15 kB)
Downloading alembic-1.16.5-py3-none-any.whl (247 kB)
Downloading anthropic-0.64.0-py3-none-any.whl (297 kB)
Using cached anyio-4.10.0-py3-none-any.whl (107 kB)
Downloading distro-1.9.0-py3-none-any.whl (20 kB)
Using cached httpx-0.28.1-py3-none-any.whl (73 kB)
Using cached httpcore-1.0.9-py3-none-any.whl (78 kB)
Downloading jiter-0.10.0-cp311-cp311-macosx_11_0_arm64.whl (321 kB)
Using cached pydantic-2.11.7-py3-none-any.whl (444 kB)
Downloading pydantic_core-2.33.2-cp311-cp311-macosx_11_0_arm64.whl (1.9 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.9/1.9 MB 4.9 MB/s eta 0:00:00
Using cached typing_extensions-4.15.0-py3-none-any.whl (44 kB)
Using cached annotated_types-0.7.0-py3-none-any.whl (13 kB)
Downloading asyncpg-0.30.0-cp311-cp311-macosx_11_0_arm64.whl (645 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 645.9/645.9 kB 5.3 MB/s eta 0:00:00
Using cached celery-5.5.3-py3-none-any.whl (438 kB)
Using cached billiard-4.2.1-py3-none-any.whl (86 kB)
Downloading click-8.2.1-py3-none-any.whl (102 kB)
Using cached kombu-5.5.4-py3-none-any.whl (210 kB)
Using cached vine-5.1.0-py3-none-any.whl (9.6 kB)
Using cached amqp-5.3.1-py3-none-any.whl (50 kB)
Using cached click_didyoumean-0.3.1-py3-none-any.whl (3.6 kB)
Using cached click_plugins-1.1.1.2-py2.py3-none-any.whl (11 kB)
Using cached click_repl-0.3.0-py3-none-any.whl (10 kB)
Using cached fastapi-0.116.1-py3-none-any.whl (95 kB)
Using cached starlette-0.47.3-py3-none-any.whl (72 kB)
Using cached h11-0.16.0-py3-none-any.whl (37 kB)
Using cached idna-3.10-py3-none-any.whl (70 kB)
Downloading minio-7.2.16-py3-none-any.whl (95 kB)
Downloading openai-1.102.0-py3-none-any.whl (812 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 812.0/812.0 kB 3.8 MB/s eta 0:00:00
Using cached prompt_toolkit-3.0.52-py3-none-any.whl (391 kB)
Downloading pygithub-2.7.0-py3-none-any.whl (416 kB)
Downloading PyJWT-2.10.1-py3-none-any.whl (22 kB)
Downloading cryptography-45.0.6-cp311-abi3-macosx_10_9_universal2.whl (7.0 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 7.0/7.0 MB 6.8 MB/s eta 0:00:00
Downloading cffi-1.17.1-cp311-cp311-macosx_11_0_arm64.whl (178 kB)
Downloading PyNaCl-1.5.0-cp36-abi3-macosx_10_10_universal2.whl (349 kB)
Using cached python_dateutil-2.9.0.post0-py2.py3-none-any.whl (229 kB)
Using cached python_dotenv-1.1.1-py3-none-any.whl (20 kB)
Downloading PyYAML-6.0.2-cp311-cp311-macosx_11_0_arm64.whl (172 kB)
Downloading qdrant_client-1.15.1-py3-none-any.whl (337 kB)
Downloading portalocker-3.2.0-py3-none-any.whl (22 kB)
Using cached urllib3-2.5.0-py3-none-any.whl (129 kB)
Downloading grpcio-1.74.0-cp311-cp311-macosx_11_0_universal2.whl (11.0 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 11.0/11.0 MB 7.0 MB/s eta 0:00:00
Downloading h2-4.3.0-py3-none-any.whl (61 kB)
Downloading hpack-4.1.0-py3-none-any.whl (34 kB)
Downloading hyperframe-6.1.0-py3-none-any.whl (13 kB)
Downloading numpy-2.3.2-cp311-cp311-macosx_14_0_arm64.whl (5.4 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 5.4/5.4 MB 5.3 MB/s eta 0:00:00
Using cached protobuf-6.32.0-cp39-abi3-macosx_10_9_universal2.whl (426 kB)
Using cached redis-6.4.0-py3-none-any.whl (279 kB)
Using cached requests-2.32.5-py3-none-any.whl (64 kB)
Downloading charset_normalizer-3.4.3-cp311-cp311-macosx_10_9_universal2.whl (204 kB)
Using cached certifi-2025.8.3-py3-none-any.whl (161 kB)
Downloading rich-14.1.0-py3-none-any.whl (243 kB)
Using cached pygments-2.19.2-py3-none-any.whl (1.2 MB)
Downloading markdown_it_py-4.0.0-py3-none-any.whl (87 kB)
Downloading mdurl-0.1.2-py3-none-any.whl (10.0 kB)
Using cached six-1.17.0-py2.py3-none-any.whl (11 kB)
Using cached sniffio-1.3.1-py3-none-any.whl (10 kB)
Downloading sqlalchemy-2.0.43-cp311-cp311-macosx_11_0_arm64.whl (2.1 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 2.1/2.1 MB 7.1 MB/s eta 0:00:00
Downloading structlog-25.4.0-py3-none-any.whl (68 kB)
Using cached tqdm-4.67.1-py3-none-any.whl (78 kB)
Downloading tree_sitter-0.25.1-cp311-cp311-macosx_11_0_arm64.whl (141 kB)
Downloading typer-0.17.3-py3-none-any.whl (46 kB)
Downloading shellingham-1.5.4-py2.py3-none-any.whl (9.8 kB)
Using cached typing_inspection-0.4.1-py3-none-any.whl (14 kB)
Using cached tzdata-2025.2-py2.py3-none-any.whl (347 kB)
Using cached uvicorn-0.35.0-py3-none-any.whl (66 kB)
Downloading httptools-0.6.4-cp311-cp311-macosx_11_0_arm64.whl (103 kB)
Downloading uvloop-0.21.0-cp311-cp311-macosx_10_9_universal2.whl (1.4 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.4/1.4 MB 4.9 MB/s eta 0:00:00
Downloading watchfiles-1.1.0-cp311-cp311-macosx_11_0_arm64.whl (397 kB)
Downloading websockets-15.0.1-cp311-cp311-macosx_11_0_arm64.whl (173 kB)
Using cached argon2_cffi-25.1.0-py3-none-any.whl (14 kB)
Using cached argon2_cffi_bindings-25.1.0-cp39-abi3-macosx_11_0_arm64.whl (31 kB)
Downloading mako-1.3.10-py3-none-any.whl (78 kB)
Downloading MarkupSafe-3.0.2-cp311-cp311-macosx_11_0_arm64.whl (12 kB)
Using cached packaging-25.0-py3-none-any.whl (66 kB)
Using cached pycparser-2.22-py3-none-any.whl (117 kB)
Downloading pycryptodome-3.23.0-cp37-abi3-macosx_10_9_universal2.whl (2.5 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 2.5/2.5 MB 5.9 MB/s eta 0:00:00
Using cached wcwidth-0.2.13-py2.py3-none-any.whl (34 kB)
Building wheels for collected packages: aomass
  Building editable for aomass (pyproject.toml): started
  Building editable for aomass (pyproject.toml): finished with status 'done'
  Created wheel for aomass: filename=aomass-0.1.0-0.editable-py3-none-any.whl size=2834 sha256=8c47de200cd8180965fdc4c391ccc6652c9f16ca16ca5c09781ed1f90bc4e0ca
  Stored in directory: /private/var/folders/0q/fddn1mld3_l4jb843dgmvndw0000gn/T/pip-ephem-wheel-cache-225e6h90/wheels/4f/70/dd/4c057e26815696bfc8c63f61de82d7f3639b2a62576c937d10
Successfully built aomass
Installing collected packages: wcwidth, websockets, vine, uvloop, urllib3, tzdata, typing-extensions, tree-sitter, tqdm, structlog, sniffio, six, shellingham, redis, pyyaml, python-dotenv, pyjwt, pygments, pycryptodome, pycparser, protobuf, prompt-toolkit, portalocker, packaging, numpy, mdurl, MarkupSafe, jiter, idna, hyperframe, httptools, hpack, h11, grpcio, distro, click, charset_normalizer, certifi, billiard, asyncpg, annotated-types, aiofiles, uvicorn, typing-inspection, sqlalchemy, requests, python-dateutil, pydantic-core, markdown-it-py, Mako, httpcore, h2, click-repl, click-plugins, click-didyoumean, cffi, anyio, amqp, watchfiles, starlette, rich, pynacl, pydantic, kombu, httpx, cryptography, argon2-cffi-bindings, alembic, typer, openai, fastapi, celery, argon2-cffi, anthropic, qdrant-client, pygithub, minio, aomass

Successfully installed Mako-1.3.10 MarkupSafe-3.0.2 aiofiles-24.1.0 alembic-1.16.5 amqp-5.3.1 annotated-types-0.7.0 anthropic-0.64.0 anyio-4.10.0 aomass-0.1.0 argon2-cffi-25.1.0 argon2-cffi-bindings-25.1.0 asyncpg-0.30.0 billiard-4.2.1 celery-5.5.3 certifi-2025.8.3 cffi-1.17.1 charset_normalizer-3.4.3 click-8.2.1 click-didyoumean-0.3.1 click-plugins-1.1.1.2 click-repl-0.3.0 cryptography-45.0.6 distro-1.9.0 fastapi-0.116.1 grpcio-1.74.0 h11-0.16.0 h2-4.3.0 hpack-4.1.0 httpcore-1.0.9 httptools-0.6.4 httpx-0.28.1 hyperframe-6.1.0 idna-3.10 jiter-0.10.0 kombu-5.5.4 markdown-it-py-4.0.0 mdurl-0.1.2 minio-7.2.16 numpy-2.3.2 openai-1.102.0 packaging-25.0 portalocker-3.2.0 prompt-toolkit-3.0.52 protobuf-6.32.0 pycparser-2.22 pycryptodome-3.23.0 pydantic-2.11.7 pydantic-core-2.33.2 pygithub-2.7.0 pygments-2.19.2 pyjwt-2.10.1 pynacl-1.5.0 python-dateutil-2.9.0.post0 python-dotenv-1.1.1 pyyaml-6.0.2 qdrant-client-1.15.1 redis-6.4.0 requests-2.32.5 rich-14.1.0 shellingham-1.5.4 six-1.17.0 sniffio-1.3.1 sqlalchemy-2.0.43 starlette-0.47.3 structlog-25.4.0 tqdm-4.67.1 tree-sitter-0.25.1 typer-0.17.3 typing-extensions-4.15.0 typing-inspection-0.4.1 tzdata-2025.2 urllib3-2.5.0 uvicorn-0.35.0 uvloop-0.21.0 vine-5.1.0 watchfiles-1.1.0 wcwidth-0.2.13 websockets-15.0.1

### Getting Help

- Check the [API documentation](docs/api.md)
- Review service logs: 
- Create an issue on GitHub
- Join our Discord community

## Next Steps

1. Configure GitHub integration
2. Set up AI service credentials
3. Explore the API documentation
4. Run your first maintenance workflow
5. Set up monitoring and alerts

## Development

For development setup:


