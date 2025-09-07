"""Repository indexing service."""
import asyncio
import hashlib
from pathlib import Path
from typing import List, Optional
from uuid import UUID, uuid4

import aiofiles
import tree_sitter
from git import Repo
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams

from aomass.config.settings import settings
from aomass.models.core import CodeFile, Language, Repository


class IndexerService:
    """Service for indexing repositories."""
    
    def __init__(self):
        self.qdrant_client = QdrantClient(url=settings.qdrant_url)
        self.temp_dir = Path("/tmp/aomass_repos")
        self.temp_dir.mkdir(exist_ok=True)
    
    async def index_repository(
        self, 
        url: str, 
        branch: str = "main", 
        force_reindex: bool = False
    ) -> str:
        """Index a GitHub repository."""
        repo_info = self._parse_github_url(url)
        repository_id = uuid4()
        
        # Create task ID for tracking
        task_id = str(uuid4())
        
        # Start background indexing
        asyncio.create_task(self._index_repository_background(
            repository_id, url, repo_info, branch, force_reindex, task_id
        ))
        
        return task_id
    
    async def _index_repository_background(
        self,
        repository_id: UUID,
        url: str,
        repo_info: dict,
        branch: str,
        force_reindex: bool,
        task_id: str
    ):
        """Background repository indexing."""
        try:
            # Clone repository
            repo_path = await self._clone_repository(url, branch)
            
            # Analyze repository structure
            languages = await self._detect_languages(repo_path)
            
            # Create repository record
            repository = Repository(
                id=repository_id,
                owner=repo_info["owner"],
                name=repo_info["repo"],
                full_name=f"{repo_info['owner']}/{repo_info['repo']}",
                url=url,
                default_branch=branch,
                languages=languages
            )
            
            # Index code files
            await self._index_code_files(repository, repo_path)
            
            # Create vector collection in Qdrant
            await self._create_vector_collection(repository_id)
            
            print(f"Repository {repository.full_name} indexed successfully")
            
        except Exception as e:
            print(f"Failed to index repository: {str(e)}")
        finally:
            # Cleanup
            if 'repo_path' in locals():
                await self._cleanup_repository(repo_path)
    
    async def _clone_repository(self, url: str, branch: str) -> Path:
        """Clone repository to temporary directory."""
        repo_id = hashlib.md5(url.encode()).hexdigest()
        repo_path = self.temp_dir / repo_id
        
        if repo_path.exists():
            # Remove existing clone
            import shutil
            shutil.rmtree(repo_path)
        
        # Clone repository
        Repo.clone_from(url, repo_path, branch=branch, depth=1)
        return repo_path
    
    async def _detect_languages(self, repo_path: Path) -> List[Language]:
        """Detect programming languages in repository."""
        languages = set()
        
        # Language file extensions mapping
        lang_extensions = {
            Language.PYTHON: [".py", ".pyw"],
            Language.JAVASCRIPT: [".js", ".mjs"],
            Language.TYPESCRIPT: [".ts", ".tsx"],
            Language.RUST: [".rs"],
            Language.GO: [".go"],
            Language.JAVA: [".java"],
        }
        
        for ext_list in lang_extensions.values():
            for ext in ext_list:
                if list(repo_path.rglob(f"*{ext}")):
                    for lang, exts in lang_extensions.items():
                        if ext in exts:
                            languages.add(lang)
                            break
        
        return list(languages)
    
    async def _index_code_files(self, repository: Repository, repo_path: Path):
        """Index individual code files."""
        lang_extensions = {
            Language.PYTHON: [".py", ".pyw"],
            Language.JAVASCRIPT: [".js", ".mjs"],
            Language.TYPESCRIPT: [".ts", ".tsx"],
            Language.RUST: [".rs"],
            Language.GO: [".go"],
            Language.JAVA: [".java"],
        }
        
        for language in repository.languages:
            extensions = lang_extensions[language]
            for ext in extensions:
                for file_path in repo_path.rglob(f"*{ext}"):
                    if file_path.is_file():
                        await self._index_single_file(
                            repository.id, file_path, repo_path, language
                        )
    
    async def _index_single_file(
        self, 
        repository_id: UUID, 
        file_path: Path, 
        repo_root: Path, 
        language: Language
    ):
        """Index a single code file."""
        try:
            # Read file content
            async with aiofiles.open(file_path, 'r', encoding='utf-8') as f:
                content = await f.read()
            
            # Calculate content hash
            content_hash = hashlib.sha256(content.encode()).hexdigest()
            
            # Get relative path
            relative_path = str(file_path.relative_to(repo_root))
            
            # Create code file record
            code_file = CodeFile(
                repository_id=repository_id,
                path=relative_path,
                language=language,
                content_hash=content_hash,
                size=len(content),
                last_modified=file_path.stat().st_mtime
            )
            
            # TODO: Parse AST and extract semantic information
            # TODO: Generate embeddings and store in Qdrant
            # TODO: Store file metadata in database
            
            print(f"Indexed file: {relative_path}")
            
        except Exception as e:
            print(f"Failed to index file {file_path}: {str(e)}")
    
    async def _create_vector_collection(self, repository_id: UUID):
        """Create Qdrant collection for repository vectors."""
        collection_name = f"repo_{repository_id}"
        
        try:
            self.qdrant_client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(
                    size=384,  # Embedding dimension
                    distance=Distance.COSINE
                )
            )
            print(f"Created vector collection: {collection_name}")
        except Exception as e:
            print(f"Failed to create vector collection: {str(e)}")
    
    async def _cleanup_repository(self, repo_path: Path):
        """Clean up cloned repository."""
        try:
            import shutil
            shutil.rmtree(repo_path)
        except Exception as e:
            print(f"Failed to cleanup repository: {str(e)}")
    
    def _parse_github_url(self, url: str) -> dict:
        """Parse GitHub URL to extract owner and repo."""
        # Simple URL parsing - in production, use more robust parsing
        parts = url.rstrip('/').split('/')
        return {
            "owner": parts[-2],
            "repo": parts[-1].replace(".git", "")
        }
