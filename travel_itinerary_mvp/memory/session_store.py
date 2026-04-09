"""
Session storage for maintaining context during the iterative process.
"""
import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime

from ..graph.state import PlanState

logger = logging.getLogger(__name__)

class SessionStore:
    """Manages session storage for the travel itinerary system."""
    
    def __init__(self, storage_dir: str = "logs/sessions"):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
    
    def save_session(self, state: PlanState) -> bool:
        """Save the current session state."""
        try:
            session_file = self.storage_dir / f"session_{state.session_id}.json"
            
            session_data = {
                "session_id": state.session_id,
                "user_input": state.user_input,
                "current_plan": state.current_plan,
                "critic_feedback": state.critic_feedback,
                "iteration": state.iteration,
                "approved": state.approved,
                "plan_history": state.plan_history,
                "feedback_history": state.feedback_history,
                "status": state.status,
                "error_message": state.error_message,
                "created_at": state.created_at.isoformat(),
                "updated_at": state.updated_at.isoformat()
            }
            
            with open(session_file, 'w', encoding='utf-8') as f:
                json.dump(session_data, f, indent=2, ensure_ascii=False, default=str)
            
            self.logger.info(f"Session saved: {state.session_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error saving session {state.session_id}: {e}")
            return False
    
    def load_session(self, session_id: str) -> Optional[PlanState]:
        """Load a session state by ID."""
        try:
            session_file = self.storage_dir / f"session_{session_id}.json"
            
            if not session_file.exists():
                self.logger.warning(f"Session file not found: {session_id}")
                return None
            
            with open(session_file, 'r', encoding='utf-8') as f:
                session_data = json.load(f)
            
            # Reconstruct PlanState from saved data
            state = PlanState(user_input=session_data['user_input'])
            state.session_id = session_data['session_id']
            state.current_plan = session_data['current_plan']
            state.critic_feedback = session_data['critic_feedback']
            state.iteration = session_data['iteration']
            state.approved = session_data['approved']
            state.plan_history = session_data.get('plan_history', [])
            state.feedback_history = session_data.get('feedback_history', [])
            state.status = session_data.get('status', 'initialized')
            state.error_message = session_data.get('error_message')
            
            self.logger.info(f"Session loaded: {session_id}")
            return state
            
        except Exception as e:
            self.logger.error(f"Error loading session {session_id}: {e}")
            return None
    
    def list_sessions(self, limit: int = 10) -> List[str]:
        """List recent session IDs."""
        try:
            session_files = list(self.storage_dir.glob("session_*.json"))
            session_files.sort(key=lambda f: f.stat().st_mtime, reverse=True)
            return [f.stem.replace("session_", "") for f in session_files[:limit]]
        except Exception as e:
            self.logger.error(f"Error listing sessions: {e}")
            return []
