"""Repository indexing service."""
import asyncio
import hashlib
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union
from uuid import UUID, uuid4

import aiofiles
import tree_sitter
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams

from ..config.settings import settings
from ..models.core import CodeFile, Language, Repository
from ..models.providers import ProviderType, RepositoryReference
from ..providers.factory import ProviderFactory


class IndexerService:
    """Service for indexing repositories."""
    
    def __init__(self):
        self.qdrant_client = QdrantClient(url=settings.qdrant_url)
        self.temp_dir = Path("/tmp/aomass_repos")
        self.temp_dir.mkdir(exist_ok=True)
        self.provider_factory = ProviderFactory
    
    async def index_repository(
        self, 
        url: str, 
        provider_type: str = None,
        branch: str = None, 
        force_reindex: bool = False
    ) -> str:
        """Index a repository from any supported cloud provider."""
        # Determine provider type from URL if not specified
        if not provider_type:
            provider_type, repo_info = self._detect_provider_from_url(url)
        else:
            provider_type = ProviderType(provider_type)
            repo_info = self._parse_repository_url(url, provider_type)
        
        # Get provider instance
        provider = self.provider_factory.get_provider(provider_type)
        if not provider:
            raise ValueError(f"Unsupported provider type: {provider_type}")
        
        # Get repository reference
        repo_ref = await provider.get_repository(repo_info["owner"], repo_info["repo"])
        if not repo_ref:
            raise ValueError(f"Repository not found: {url}")
        
        repository_id = uuid4()
        
        # Create task ID for tracking
        task_id = str(uuid4())
        
        # Start background indexing
        asyncio.create_task(self._index_repository_background(
            repository_id, repo_ref, branch, force_reindex, task_id
        ))
        
        return task_id
    
    async def _index_repository_background(
        self,
        repository_id: UUID,
        repo_ref: RepositoryReference,
        branch: str = None,
        force_reindex: bool = False,
        task_id: str = None
    ):
        """Background repository indexing."""
        try:
            # Get provider
            provider = self.provider_factory.get_provider(repo_ref.provider_type)
            if not provider:
                raise ValueError(f"Provider not available: {repo_ref.provider_type}")
            
            # Clone repository
            repo_path = await provider.clone_repository(
                repo_ref, 
                str(self.temp_dir / str(repository_id)),
                branch=branch or repo_ref.default_branch
            )
            
            # Analyze repository structure
            languages = await self._detect_languages(Path(repo_path))
            
            # Create repository record
            repository = Repository(
                id=repository_id,
                owner=repo_ref.full_name.split('/')[0],
                name=repo_ref.full_name.split('/')[1],
                full_name=repo_ref.full_name,
                url=repo_ref.url,
                default_branch=branch or repo_ref.default_branch,
                languages=languages,
                provider_type=repo_ref.provider_type.value,
                provider_id=repo_ref.provider_id
            )
            
            # Index code files
            await self._index_code_files(repository, Path(repo_path))
            
            # Create vector collection in Qdrant
            await self._create_vector_collection(repository_id)
            
            print(f"Repository {repository.full_name} indexed successfully")
            
        except Exception as e:
            print(f"Failed to index repository: {str(e)}")
        finally:
            # Cleanup
            if 'repo_path' in locals():
                await self._cleanup_repository(Path(repo_path))
    
    def _detect_provider_from_url(self, url: str) -> Tuple[ProviderType, Dict[str, str]]:
        """Detect provider type from URL and parse repository info."""
        if "github.com" in url:
            return ProviderType.GITHUB, self._parse_repository_url(url, ProviderType.GITHUB)
        elif "gitlab.com" in url or settings.gitlab_url in url:
            return ProviderType.GITLAB, self._parse_repository_url(url, ProviderType.GITLAB)
        elif "bitbucket.org" in url:
            return ProviderType.BITBUCKET, self._parse_repository_url(url, ProviderType.BITBUCKET)
        elif "dev.azure.com" in url:
            return ProviderType.AZURE_DEVOPS, self._parse_repository_url(url, ProviderType.AZURE_DEVOPS)
        elif "codecommit" in url:
            return ProviderType.AWS_CODECOMMIT, self._parse_repository_url(url, ProviderType.AWS_CODECOMMIT)
        else:
            return ProviderType.GENERIC_GIT, {"url": url, "owner": "unknown", "repo": "unknown"}
    
    def _parse_repository_url(self, url: str, provider_type: ProviderType) -> Dict[str, str]:
        """Parse repository URL based on provider type."""
        if provider_type == ProviderType.GITHUB:
            return self._parse_github_url(url)
        elif provider_type == ProviderType.GITLAB:
            # TODO: Implement GitLab URL parsing
            pass
        elif provider_type == ProviderType.BITBUCKET:
            # TODO: Implement Bitbucket URL parsing
            pass
        elif provider_type == ProviderType.AZURE_DEVOPS:
            # TODO: Implement Azure DevOps URL parsing
            pass
        elif provider_type == ProviderType.AWS_CODECOMMIT:
            # TODO: Implement AWS CodeCommit URL parsing
            pass
        
        # Default fallback
        return {"url": url, "owner": "unknown", "repo": "unknown"}
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
