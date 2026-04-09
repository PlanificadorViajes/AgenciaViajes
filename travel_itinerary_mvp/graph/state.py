"""
State management for the travel itinerary system.
"""
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
from datetime import datetime

@dataclass
class PlanState:
    """State container for the iterative planning process."""
    
    user_input: str
    current_plan: Optional[Dict[str, Any]] = None
    critic_feedback: Optional[Dict[str, Any]] = None
    iteration: int = 0
    approved: bool = False
    
    plan_history: List[Dict[str, Any]] = field(default_factory=list)
    feedback_history: List[Dict[str, Any]] = field(default_factory=list)
    
    session_id: str = field(default_factory=lambda: datetime.now().strftime("%Y%m%d_%H%M%S"))
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    status: str = "initialized"
    error_message: Optional[str] = None
    
    def update_plan(self, new_plan: Dict[str, Any]) -> None:
        """Update the current plan and maintain history."""
        if self.current_plan:
            self.plan_history.append({
                "iteration": self.iteration,
                "plan": self.current_plan.copy(),
                "timestamp": self.updated_at
            })
        
        self.current_plan = new_plan
        self.iteration += 1
        self.updated_at = datetime.now()
        self.status = "plan_updated"
    
    def update_feedback(self, feedback: Dict[str, Any]) -> None:
        """Update critic feedback and maintain history."""
        if self.critic_feedback:
            self.feedback_history.append({
                "iteration": self.iteration - 1,
                "feedback": self.critic_feedback.copy(),
                "timestamp": self.updated_at
            })
        
        self.critic_feedback = feedback
        self.approved = feedback.get("approved", False)
        self.updated_at = datetime.now()
        self.status = "feedback_received"
    
    def set_status(self, status: str, error_message: Optional[str] = None) -> None:
        """Update the processing status."""
        self.status = status
        self.error_message = error_message
        self.updated_at = datetime.now()
    
    def get_current_score(self) -> float:
        """Get the current quality score from critic feedback."""
        if self.critic_feedback:
            return self.critic_feedback.get("score", 0.0)
        return 0.0
    
    def should_continue(self, max_iterations: int) -> bool:
        """Determine if the process should continue iterating."""
        if self.approved:
            return False
        if self.iteration >= max_iterations:
            return False
        return True
    
    def get_iteration_summary(self) -> str:
        """Get a summary of the current iteration."""
        score = self.get_current_score()
        return f"Iteration {self.iteration}: Score {score:.1f}/10.0, Status: {self.status}, Approved: {self.approved}"
