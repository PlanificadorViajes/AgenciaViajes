"""
Orchestrator for the travel itinerary generation system.
"""
import logging
from typing import Dict, Any, Optional

from .state import PlanState
from ..agents.generator import GeneratorAgent
from ..agents.critic import CriticAgent
from ..config.settings import SYSTEM_SETTINGS

logger = logging.getLogger(__name__)

class ItineraryOrchestrator:
    """Orchestrates the iterative plan generation and refinement process."""
    
    def __init__(self):
        self.generator = GeneratorAgent()
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
                # Generate plan
                state.set_status("generating")
                self.logger.info(f"Starting iteration {state.iteration + 1}")
                
                plan = self.generator.generate_plan(
                    user_input=user_input,
                    constraints=constraints,
                    feedback=state.critic_feedback
                )
                state.update_plan(plan)
                
                # Evaluate plan
                state.set_status("evaluating")
                feedback = self.critic.evaluate_plan(plan)
                state.update_feedback(feedback)
                
                self.logger.info(state.get_iteration_summary())
                
                if state.approved:
                    state.set_status("completed")
                    self.logger.info(f"Plan approved after {state.iteration} iterations")
                    break
                elif state.iteration >= max_iterations:
                    state.set_status("max_iterations_reached")
                    self.logger.warning(f"Reached maximum iterations ({max_iterations})")
                    break
                else:
                    state.set_status("refining")
                    self.logger.info("Plan not approved, continuing to next iteration")
            
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
