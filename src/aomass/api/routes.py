"""API routes for AOMaaS."""
from uuid import UUID

from fastapi import APIRouter, BackgroundTasks, HTTPException, status
from fastapi.responses import JSONResponse

from aomass.models.api import (
    CreatePRRequest,
    GeneratePlanRequest,
    ImplementPlanRequest,
    ImplementationResponse,
    IndexRepositoryRequest,
    IndexResponse,
    MineOpportunitiesRequest,
    OpportunitiesResponse,
    PlanResponse,
    PRResponse,
    ReviewPRRequest,
    ReviewResponse,
    TaskResponse,
)
from aomass.services.indexer import IndexerService
from aomass.services.miner import MinerService
from aomass.services.planner import PlannerService
from aomass.services.implementer import ImplementerService
from aomass.services.pr_manager import PRManagerService
from aomass.services.reviewer import ReviewerService

router = APIRouter()

# Service instances (will be injected via dependency injection)
indexer_service = IndexerService()
miner_service = MinerService()
planner_service = PlannerService()
implementer_service = ImplementerService()
pr_manager_service = PRManagerService()
reviewer_service = ReviewerService()


@router.post("/index", response_model=IndexResponse)
async def index_repository(
    request: IndexRepositoryRequest, 
    background_tasks: BackgroundTasks
) -> IndexResponse:
    """Index a GitHub repository."""
    try:
        task_id = await indexer_service.index_repository(
            url=str(request.url),
            branch=request.branch,
            force_reindex=request.force_reindex
        )
        
        return IndexResponse(
            task_id=task_id,
            status="pending",
            message="Repository indexing started"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to start indexing: {str(e)}"
        )


@router.post("/mine", response_model=OpportunitiesResponse)
async def mine_opportunities(
    request: MineOpportunitiesRequest
) -> OpportunitiesResponse:
    """Mine maintenance opportunities from a repository."""
    try:
        opportunities = await miner_service.mine_opportunities(
            repository_id=request.repository_id,
            opportunity_types=request.opportunity_types,
            languages=request.languages,
            max_opportunities=request.max_opportunities
        )
        
        return OpportunitiesResponse(
            repository_id=request.repository_id,
            opportunities=[opp.dict() for opp in opportunities],
            total_count=len(opportunities)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to mine opportunities: {str(e)}"
        )


@router.post("/plan", response_model=PlanResponse)
async def generate_plan(
    request: GeneratePlanRequest
) -> PlanResponse:
    """Generate implementation plan for an opportunity."""
    try:
        plan = await planner_service.generate_plan(
            opportunity_id=request.opportunity_id,
            preferences=request.preferences
        )
        
        return PlanResponse(
            plan_id=plan.id,
            title=plan.title,
            description=plan.description,
            steps=plan.steps,
            estimated_effort=plan.estimated_effort,
            risks=plan.risks
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate plan: {str(e)}"
        )


@router.post("/implement", response_model=ImplementationResponse)
async def implement_plan(
    request: ImplementPlanRequest,
    background_tasks: BackgroundTasks
) -> ImplementationResponse:
    """Implement a generated plan."""
    try:
        task_id = await implementer_service.implement_plan(
            plan_id=request.plan_id,
            dry_run=request.dry_run
        )
        
        return ImplementationResponse(
            task_id=task_id,
            status="pending",
            message="Implementation started"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to start implementation: {str(e)}"
        )


@router.post("/pr", response_model=PRResponse)
async def create_pull_request(
    request: CreatePRRequest
) -> PRResponse:
    """Create a GitHub pull request."""
    try:
        pr = await pr_manager_service.create_pull_request(
            implementation_id=request.implementation_id,
            title=request.title,
            description=request.description,
            draft=request.draft
        )
        
        return PRResponse(
            pr_id=pr.id,
            github_pr_number=pr.github_pr_number,
            url=f"https://github.com/owner/repo/pull/{pr.github_pr_number}" if pr.github_pr_number else None,
            status=pr.status
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create pull request: {str(e)}"
        )


@router.post("/review", response_model=ReviewResponse)
async def review_pull_request(
    request: ReviewPRRequest,
    background_tasks: BackgroundTasks
) -> ReviewResponse:
    """Review a pull request with AI agents."""
    try:
        review = await reviewer_service.review_pull_request(
            pull_request_id=request.pull_request_id,
            reviewers=request.reviewers
        )
        
        return ReviewResponse(
            review_id=review.id,
            status=review.status,
            score=review.score,
            comments_count=len(review.comments)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to review pull request: {str(e)}"
        )


@router.get("/tasks/{task_id}", response_model=TaskResponse)
async def get_task_status(task_id: str) -> TaskResponse:
    """Get the status of a background task."""
    # TODO: Implement task status tracking
    return TaskResponse(
        task_id=task_id,
        status="pending",
        message="Task status tracking not implemented yet"
    )


@router.get("/repositories/{repository_id}/opportunities")
async def get_repository_opportunities(repository_id: UUID):
    """Get all opportunities for a repository."""
    try:
        opportunities = await miner_service.get_opportunities(repository_id)
        return {"opportunities": [opp.dict() for opp in opportunities]}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get opportunities: {str(e)}"
        )
