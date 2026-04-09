"""
Orchestrator for the travel itinerary generation system.
"""
import logging
from typing import Dict, Any, Optional

from .state import PlanState
from ..agents.analyst import AnalystAgent
from ..agents.generator import PlannerAgent
from ..agents.critic import CriticAgent
from ..config.settings import SYSTEM_SETTINGS

logger = logging.getLogger(__name__)

class ItineraryOrchestrator:
    """Orchestrates the iterative plan generation and refinement process."""
    
    def __init__(self):
        self.analyst = AnalystAgent()
        self.planner = PlannerAgent()
        self.critic = CriticAgent()
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
    
    def process_request(
        self, 
        user_input: str, 
        constraints: Optional[Dict[str, Any]] = None,
        max_iterations: int = None
    ) -> PlanState:
        """
        Process a travel itinerary request through the complete workflow.
        
        Args:
            user_input: User's travel requirements
            constraints: Optional constraints (budget, dates, etc.)
            max_iterations: Maximum number of iterations (default from settings)
            
        Returns:
            Final state with approved plan or best attempt
        """
        if max_iterations is None:
            max_iterations = SYSTEM_SETTINGS.MAX_ITERATIONS
        
        # Initialize state
        state = PlanState(user_input=user_input)
        self.logger.info(f"Starting itinerary generation process. Session: {state.session_id}")
        
        try:
            while state.should_continue(max_iterations):
                state.set_status("analyzing")
                spec = self.analyst.analyze(user_input, constraints.get("budget") if constraints else None)

                state.set_status("planning")
                plan = self.planner.generate_plan(spec.dict())
                state.update_plan(plan)

                state.set_status("evaluating")
                feedback = self.critic.evaluate_plan(plan)
                state.update_feedback(feedback)

                if feedback.get("requires_human_review"):
                    state.set_status("requires_human_review")
                    break

                if feedback.get("approved"):
                    state.set_status("completed")
                    break

                if state.iteration >= max_iterations:
                    state.set_status("max_iterations_reached")
                    break

                state.set_status("refining")
            
        except Exception as e:
            error_msg = f"Error in orchestration process: {str(e)}"
            self.logger.error(error_msg)
            state.set_status("failed", error_msg)
        
        self.logger.info(f"Process completed. Final status: {state.status}")
        return state
    
    def get_process_summary(self, state: PlanState) -> Dict[str, Any]:
        """Get a summary of the process execution."""
        return {
            "session_id": state.session_id,
            "iterations": state.iteration,
            "final_status": state.status,
            "approved": state.approved,
            "final_score": state.get_current_score(),
            "created_at": state.created_at.isoformat(),
            "completed_at": state.updated_at.isoformat(),
            "error_message": state.error_message
        }
