"""Unit tests for services."""
import pytest
from uuid import uuid4

from aomass.services.miner import MinerService
from aomass.services.planner import PlannerService
from aomass.models.core import Language, OpportunityType


class TestMinerService:
    """Test cases for MinerService."""
    
    @pytest.fixture
    def miner_service(self):
        return MinerService()
    
    @pytest.mark.asyncio
    async def test_mine_opportunities(self, miner_service: MinerService):
        """Test opportunity mining."""
        repo_id = uuid4()
        opportunities = await miner_service.mine_opportunities(
            repository_id=repo_id,
            opportunity_types=[OpportunityType.DEPENDENCY_UPDATE],
            languages=[Language.PYTHON],
            max_opportunities=5
        )
        
        assert len(opportunities) <= 5
        for opp in opportunities:
            assert opp.repository_id == repo_id
            assert opp.type == OpportunityType.DEPENDENCY_UPDATE
    
    @pytest.mark.asyncio
    async def test_mine_all_types(self, miner_service: MinerService):
        """Test mining all opportunity types."""
        repo_id = uuid4()
        opportunities = await miner_service.mine_opportunities(
            repository_id=repo_id,
            opportunity_types=[],  # Empty means all types
            languages=[Language.PYTHON, Language.JAVASCRIPT],
            max_opportunities=10
        )
        
        assert len(opportunities) <= 10
        # Should have various opportunity types
        types_found = set(opp.type for opp in opportunities)
        assert len(types_found) > 1


class TestPlannerService:
    """Test cases for PlannerService."""
    
    @pytest.fixture
    def planner_service(self):
        return PlannerService()
    
    @pytest.mark.asyncio
    async def test_generate_plan(self, planner_service: PlannerService):
        """Test plan generation."""
        opportunity_id = uuid4()
        plan = await planner_service.generate_plan(opportunity_id)
        
        assert plan.opportunity_id == opportunity_id
        assert plan.title
        assert plan.description
        assert len(plan.steps) > 0
        assert plan.estimated_effort in ["low", "medium", "high"]
    
    @pytest.mark.asyncio
    async def test_generate_plan_with_preferences(self, planner_service: PlannerService):
        """Test plan generation with preferences."""
        opportunity_id = uuid4()
        preferences = {"risk_tolerance": "low", "testing_required": True}
        
        plan = await planner_service.generate_plan(opportunity_id, preferences)
        
        assert plan.opportunity_id == opportunity_id
        assert isinstance(plan.risks, list)
