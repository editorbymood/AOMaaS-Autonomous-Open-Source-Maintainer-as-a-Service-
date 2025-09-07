"""Command-line interface for AOMaaS."""
from typing import List, Optional
from uuid import UUID

import typer
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
import httpx

from aomass.config.settings import settings

app = typer.Typer(
    name="aomass",
    help="Autonomous Open-Source Maintainer as a Service",
    add_completion=False
)
console = Console()

# API client
class AOMaaSClient:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.client = httpx.AsyncClient()
    
    async def index_repository(self, url: str, branch: str = "main", force: bool = False):
        response = await self.client.post(
            f"{self.base_url}/api/v1/index",
            json={"url": url, "branch": branch, "force_reindex": force}
        )
        return response.json()
    
    async def mine_opportunities(self, repo_id: str, types: List[str] = None, max_count: int = 10):
        response = await self.client.post(
            f"{self.base_url}/api/v1/mine",
            json={
                "repository_id": repo_id,
                "opportunity_types": types or [],
                "max_opportunities": max_count
            }
        )
        return response.json()

client = AOMaaSClient()

@app.command()
def index(
    url: str = typer.Argument(..., help="Repository URL to index"),
    branch: str = typer.Option("main", "--branch", "-b", help="Branch to index"),
    force: bool = typer.Option(False, "--force", "-f", help="Force reindexing")
):
    """Index a GitHub repository."""
    console.print(f"[blue]Indexing repository:[/blue] {url}")
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task("Indexing repository...", total=None)
        
        try:
            import asyncio
            result = asyncio.run(client.index_repository(url, branch, force))
            progress.update(task, description="Index complete!")
            
            console.print(f"[green]✓[/green] Repository indexed successfully")
            console.print(f"Task ID: {result['task_id']}")
            
        except Exception as e:
            console.print(f"[red]✗[/red] Failed to index repository: {e}")
            raise typer.Exit(1)

@app.command()
def mine(
    repo_id: str = typer.Argument(..., help="Repository ID"),
    types: Optional[List[str]] = typer.Option(None, "--type", "-t", help="Opportunity types to mine"),
    max_count: int = typer.Option(10, "--max", "-m", help="Maximum opportunities to return")
):
    """Mine maintenance opportunities."""
    console.print(f"[blue]Mining opportunities for repository:[/blue] {repo_id}")
    
    try:
        import asyncio
        result = asyncio.run(client.mine_opportunities(repo_id, types, max_count))
        
        opportunities = result['opportunities']
        console.print(f"[green]✓[/green] Found {len(opportunities)} opportunities")
        
        # Display opportunities in a table
        table = Table(title="Maintenance Opportunities")
        table.add_column("Priority", style="red", no_wrap=True)
        table.add_column("Type", style="blue")
        table.add_column("Title", style="white")
        table.add_column("Confidence", style="green")
        
        for opp in opportunities:
            table.add_row(
                str(opp['priority']),
                opp['type'].replace('_', ' ').title(),
                opp['title'][:50] + ("..." if len(opp['title']) > 50 else ""),
                f"{opp['confidence']:.1%}"
            )
        
        console.print(table)
        
    except Exception as e:
        console.print(f"[red]✗[/red] Failed to mine opportunities: {e}")
        raise typer.Exit(1)

@app.command()
def maintain(
    repo_url: str = typer.Argument(..., help="Repository URL"),
    auto_pr: bool = typer.Option(False, "--auto-pr", help="Automatically create PRs"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Simulate changes without applying"),
    max_opportunities: int = typer.Option(5, "--max", "-m", help="Maximum opportunities to process")
):
    """Full maintenance workflow: index, mine, plan, implement, and optionally create PRs."""
    console.print(f"[bold blue]Starting full maintenance workflow for:[/bold blue] {repo_url}")
    
    try:
        import asyncio
        
        # Step 1: Index repository
        console.print("
[yellow]Step 1:[/yellow] Indexing repository...")
        index_result = asyncio.run(client.index_repository(repo_url))
        console.print(f"[green]✓[/green] Repository indexed (Task ID: {index_result['task_id']})")
        
        # For demo purposes, we'll use a mock repo ID
        # In production, you'd extract this from the index result
        mock_repo_id = "12345678-1234-5678-9012-123456789012"
        
        # Step 2: Mine opportunities
        console.print("
[yellow]Step 2:[/yellow] Mining opportunities...")
        mine_result = asyncio.run(client.mine_opportunities(mock_repo_id, None, max_opportunities))
        opportunities = mine_result['opportunities']
        console.print(f"[green]✓[/green] Found {len(opportunities)} opportunities")
        
        # Step 3: Process each opportunity
        for i, opp in enumerate(opportunities[:max_opportunities], 1):
            console.print(f"
[yellow]Processing opportunity {i}/{len(opportunities)}:[/yellow] {opp['title']}")
            
            # TODO: Implement plan generation, implementation, and PR creation
            # For now, just show what would be done
            if dry_run:
                console.print(f"  [dim]Would generate plan and implement changes[/dim]")
                if auto_pr:
                    console.print(f"  [dim]Would create GitHub PR[/dim]")
            else:
                console.print(f"  [dim]Plan generation not implemented yet[/dim]")
        
        console.print(f"
[bold green]✓ Maintenance workflow completed![/bold green]")
        
    except Exception as e:
        console.print(f"[red]✗[/red] Maintenance workflow failed: {e}")
        raise typer.Exit(1)

@app.command()
def status():
    """Check AOMaaS service status."""
    console.print("[blue]Checking AOMaaS service status...[/blue]")
    
    try:
        import asyncio
        async def check_status():
            response = await client.client.get(f"{client.base_url}/health")
            return response.json()
        
        result = asyncio.run(check_status())
        
        console.print(f"[green]✓[/green] AOMaaS is healthy")
        console.print(f"Version: {result['version']}")
        
        # Display service status
        table = Table(title="Service Status")
        table.add_column("Service", style="blue")
        table.add_column("Status", style="green")
        
        for service, status in result['services'].items():
            table.add_row(service.title(), status.title())
        
        console.print(table)
        
    except Exception as e:
        console.print(f"[red]✗[/red] Failed to check status: {e}")
        raise typer.Exit(1)

@app.command()
def config():
    """Show current configuration."""
    console.print("[bold blue]AOMaaS Configuration[/bold blue]
")
    
    table = Table(title="Configuration Settings")
    table.add_column("Setting", style="blue")
    table.add_column("Value", style="white")
    
    config_items = [
        ("App Name", settings.app_name),
        ("Version", settings.app_version),
        ("Debug Mode", str(settings.debug)),
        ("Log Level", settings.log_level),
        ("Database URL", settings.database_url),
        ("Redis URL", settings.redis_url),
        ("Qdrant URL", settings.qdrant_url),
        ("MinIO Endpoint", settings.minio_endpoint),
    ]
    
    for setting, value in config_items:
        # Hide sensitive values
        if "password" in value.lower() or "secret" in value.lower() or "key" in value.lower():
            value = "***HIDDEN***"
        table.add_row(setting, str(value))
    
    console.print(table)

if __name__ == "__main__":
    app()
