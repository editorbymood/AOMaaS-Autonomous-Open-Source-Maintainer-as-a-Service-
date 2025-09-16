"""Code implementation service."""
import asyncio
from typing import Any, Dict, List
from uuid import UUID, uuid4

from ..models.core import Implementation, Plan, TaskStatus


class ImplementerService:
    """Service for implementing planned changes."""
    
    def __init__(self):
        pass
    
    async def implement_plan(self, plan_id: UUID, dry_run: bool = False) -> str:
        """Implement a generated plan."""
        task_id = str(uuid4())
        
        # Start background implementation
        asyncio.create_task(self._implement_plan_background(plan_id, dry_run, task_id))
        
        return task_id
    
    async def _implement_plan_background(
        self, plan_id: UUID, dry_run: bool, task_id: str
    ):
        """Background plan implementation."""
        try:
            # TODO: Fetch plan from database
            plan = await self._get_plan(plan_id)
            
            # Create implementation record
            implementation = Implementation(
                plan_id=plan_id,
                status=TaskStatus.IN_PROGRESS
            )
            
            changes = []
            
            # Execute plan steps
            for step in plan.steps:
                change = await self._execute_step(step, dry_run)
                changes.append(change)
            
            # Run tests if not dry run
            if not dry_run:
                tests_passed = await self._run_tests()
                implementation.tests_passed = tests_passed
            
            implementation.changes = changes
            implementation.status = TaskStatus.COMPLETED
            
            print(f"Plan {plan_id} implemented successfully")
            
        except Exception as e:
            print(f"Failed to implement plan: {str(e)}")
            # Update implementation status to failed
    
    async def _get_plan(self, plan_id: UUID) -> Plan:
        """Get plan by ID."""
        # TODO: Implement database query
        return Plan(
            id=plan_id,
            opportunity_id=UUID("12345678-1234-5678-9012-123456789012"),
            title="Mock plan",
            description="Mock implementation plan",
            steps=[{"step": 1, "description": "Mock step"}],
            estimated_effort="low",
            risks=[]
        )
    
    async def _execute_step(self, step: Dict[str, Any], dry_run: bool) -> Dict[str, Any]:
        """Execute a single implementation step."""
        step_num = step.get("step", 0)
        description = step.get("description", "Unknown step")
        files = step.get("files", [])
        
        print(f"Executing step {step_num}: {description}")
        
        if dry_run:
            return {
                "step": step_num,
                "description": description,
                "status": "simulated",
                "files_modified": files,
                "changes": "Dry run - no actual changes made"
            }
        
        # Simulate actual implementation
        await asyncio.sleep(1)  # Simulate work
        
        return {
            "step": step_num,
            "description": description,
            "status": "completed",
            "files_modified": files,
            "changes": f"Implemented: {description}"
        }
    
    async def _run_tests(self) -> bool:
        """Run tests after implementation."""
        print("Running tests...")
        
        # Simulate test execution
        await asyncio.sleep(3)
        
        # Mock test results
        return True  # Tests passed
