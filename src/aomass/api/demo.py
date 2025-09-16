"""Demo functionality for first-time users of AOMaaS."""
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Dict, List, Optional

from .auth import get_current_user
from ..utils.logging import get_logger

logger = get_logger(__name__)

router = APIRouter()


class DemoRepository(BaseModel):
    """Demo repository model."""
    id: str
    name: str
    description: str
    url: str
    stars: int
    forks: int
    issues: int
    language: str


class DemoOpportunity(BaseModel):
    """Demo opportunity model."""
    id: str
    title: str
    description: str
    file_path: str
    line_number: int
    priority: str
    category: str
    estimated_effort: str


class DemoImplementation(BaseModel):
    """Demo implementation model."""
    id: str
    opportunity_id: str
    title: str
    description: str
    code_diff: str
    status: str


# Sample demo data
DEMO_REPOSITORIES = [
    DemoRepository(
        id="demo-repo-1",
        name="sample-python-app",
        description="A sample Python application with various improvement opportunities",
        url="https://github.com/example/sample-python-app",
        stars=120,
        forks=35,
        issues=8,
        language="Python"
    ),
    DemoRepository(
        id="demo-repo-2",
        name="react-dashboard",
        description="A React dashboard with performance optimization opportunities",
        url="https://github.com/example/react-dashboard",
        stars=450,
        forks=120,
        issues=15,
        language="JavaScript"
    ),
    DemoRepository(
        id="demo-repo-3",
        name="go-microservice",
        description="A Go microservice with scalability improvements",
        url="https://github.com/example/go-microservice",
        stars=320,
        forks=85,
        issues=12,
        language="Go"
    )
]

DEMO_OPPORTUNITIES = [
    DemoOpportunity(
        id="demo-opp-1",
        title="Optimize database query performance",
        description="The current query is fetching all records without pagination, causing performance issues with large datasets.",
        file_path="app/models/user.py",
        line_number=45,
        priority="high",
        category="performance",
        estimated_effort="medium"
    ),
    DemoOpportunity(
        id="demo-opp-2",
        title="Add proper error handling",
        description="The function lacks proper error handling, which can lead to unexpected crashes.",
        file_path="app/services/api.py",
        line_number=78,
        priority="medium",
        category="reliability",
        estimated_effort="low"
    ),
    DemoOpportunity(
        id="demo-opp-3",
        title="Fix security vulnerability in authentication",
        description="The current implementation is vulnerable to timing attacks.",
        file_path="app/auth/login.py",
        line_number=112,
        priority="high",
        category="security",
        estimated_effort="high"
    ),
    DemoOpportunity(
        id="demo-opp-4",
        title="Improve code documentation",
        description="The module lacks proper documentation, making it difficult for new developers to understand.",
        file_path="app/utils/helpers.py",
        line_number=23,
        priority="low",
        category="maintainability",
        estimated_effort="low"
    ),
    DemoOpportunity(
        id="demo-opp-5",
        title="Refactor duplicate code",
        description="There's significant code duplication across multiple functions that should be refactored.",
        file_path="app/controllers/product.py",
        line_number=156,
        priority="medium",
        category="maintainability",
        estimated_effort="medium"
    )
]

DEMO_IMPLEMENTATIONS = [
    DemoImplementation(
        id="demo-impl-1",
        opportunity_id="demo-opp-1",
        title="Implemented pagination for database queries",
        description="Added pagination to the database query to improve performance with large datasets.",
        code_diff="""@@ -45,7 +45,10 @@
 def get_all_users():
-    return db.session.query(User).all()
+    page = request.args.get('page', 1, type=int)
+    per_page = request.args.get('per_page', 20, type=int)
+    pagination = db.session.query(User).paginate(page=page, per_page=per_page)
+    return pagination.items, pagination.total
 """,
        status="completed"
    ),
    DemoImplementation(
        id="demo-impl-2",
        opportunity_id="demo-opp-2",
        title="Added proper error handling",
        description="Implemented try-except blocks with specific exception handling and logging.",
        code_diff="""@@ -78,5 +78,12 @@
 def call_external_api(endpoint, data):
-    response = requests.post(API_URL + endpoint, json=data)
-    return response.json()
+    try:
+        response = requests.post(API_URL + endpoint, json=data, timeout=10)
+        response.raise_for_status()
+        return response.json()
+    except requests.exceptions.Timeout:
+        logger.error(f"API request to {endpoint} timed out")
+        raise APITimeoutError(f"Request to {endpoint} timed out")
+    except requests.exceptions.RequestException as e:
+        logger.error(f"API request failed: {str(e)}")
+        raise APIRequestError(f"Request failed: {str(e)}")
 """,
        status="completed"
    )
]


@router.get("/demo/repositories", response_model=List[DemoRepository])
async def get_demo_repositories(current_user = Depends(get_current_user)):
    """Get list of demo repositories."""
    logger.info("User accessed demo repositories", user_id=current_user.username)
    return DEMO_REPOSITORIES


@router.get("/demo/repositories/{repo_id}", response_model=DemoRepository)
async def get_demo_repository(repo_id: str, current_user = Depends(get_current_user)):
    """Get a specific demo repository."""
    for repo in DEMO_REPOSITORIES:
        if repo.id == repo_id:
            return repo
    
    logger.warning("User attempted to access non-existent demo repository", 
                  user_id=current_user.username, repo_id=repo_id)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Demo repository not found"
    )


@router.get("/demo/opportunities", response_model=List[DemoOpportunity])
async def get_demo_opportunities(repo_id: Optional[str] = None, current_user = Depends(get_current_user)):
    """Get list of demo opportunities, optionally filtered by repository."""
    logger.info("User accessed demo opportunities", 
               user_id=current_user.username, repo_id=repo_id)
    
    # In a real implementation, we would filter by repo_id
    # For demo purposes, we're returning all opportunities
    return DEMO_OPPORTUNITIES


@router.get("/demo/opportunities/{opportunity_id}", response_model=DemoOpportunity)
async def get_demo_opportunity(opportunity_id: str, current_user = Depends(get_current_user)):
    """Get a specific demo opportunity."""
    for opp in DEMO_OPPORTUNITIES:
        if opp.id == opportunity_id:
            return opp
    
    logger.warning("User attempted to access non-existent demo opportunity", 
                  user_id=current_user.username, opportunity_id=opportunity_id)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Demo opportunity not found"
    )


@router.get("/demo/implementations", response_model=List[DemoImplementation])
async def get_demo_implementations(
    opportunity_id: Optional[str] = None, 
    current_user = Depends(get_current_user)
):
    """Get list of demo implementations, optionally filtered by opportunity."""
    logger.info("User accessed demo implementations", 
               user_id=current_user.username, opportunity_id=opportunity_id)
    
    if opportunity_id:
        return [impl for impl in DEMO_IMPLEMENTATIONS if impl.opportunity_id == opportunity_id]
    return DEMO_IMPLEMENTATIONS


@router.get("/demo/implementations/{implementation_id}", response_model=DemoImplementation)
async def get_demo_implementation(implementation_id: str, current_user = Depends(get_current_user)):
    """Get a specific demo implementation."""
    for impl in DEMO_IMPLEMENTATIONS:
        if impl.id == implementation_id:
            return impl
    
    logger.warning("User attempted to access non-existent demo implementation", 
                  user_id=current_user.username, implementation_id=implementation_id)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Demo implementation not found"
    )


@router.post("/demo/reset", status_code=status.HTTP_200_OK)
async def reset_demo_data(current_user = Depends(get_current_user)):
    """Reset demo data to initial state."""
    # In a real implementation, this would reset the demo data to its initial state
    # For this demo, the data is static, so we just log the action
    logger.info("User reset demo data", user_id=current_user.username)
    return {"message": "Demo data has been reset to initial state"}