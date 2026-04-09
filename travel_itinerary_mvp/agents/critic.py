"""
Travel Itinerary Critic Agent.
"""
import json
import logging
from typing import Dict, Any, Optional

from ..config.settings import SYSTEM_SETTINGS

logger = logging.getLogger(__name__)

class CriticAgent:
    """Travel itinerary critic agent."""
    
    def __init__(self):
        self.prompt_template = self._load_prompt_template()
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
    
    def _load_prompt_template(self) -> str:
        """Load the critic prompt template from file."""
        try:
            with open(SYSTEM_SETTINGS.CRITIC_PROMPT_FILE, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            self.logger.error(f"Critic prompt file not found")
            return "Evaluate the travel itinerary for quality and feasibility."
    
    def evaluate_plan(self, plan: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate a travel itinerary plan."""
        self.logger.info("Starting plan evaluation")
        
        try:
            feedback = self._evaluate_mock_plan(plan)
            self.logger.info(f"Plan evaluation completed. Score: {feedback['score']:.1f}")
            return feedback
        except Exception as e:
            self.logger.error(f"Error evaluating plan: {str(e)}")
            raise
    
    def _evaluate_mock_plan(self, plan: Dict[str, Any]) -> Dict[str, Any]:
        """Generate mock evaluation for demonstration."""
        plan_data = plan.get('plan', {})
        
        # Mock scoring based on plan completeness and structure
        clarity_score = self._score_clarity(plan_data)
        consistency_score = self._score_consistency(plan_data)
        constraint_score = 8.0
        optimization_score = 7.5
        risk_score = self._score_risk_assessment(plan)
        detail_score = self._score_detail_level(plan_data)
        
        # Calculate weighted overall score
        overall_score = (
            clarity_score * 0.15 +
            consistency_score * 0.20 +
            constraint_score * 0.25 +
            optimization_score * 0.20 +
            risk_score * 0.10 +
            detail_score * 0.10
        )
        
        approved = overall_score >= 7.0
        
        issues = self._identify_issues(plan_data, overall_score)
        improvements = self._suggest_improvements(plan_data, overall_score)
        strengths = self._identify_strengths(plan_data)
        
        return {
            "score": round(overall_score, 1),
            "detailed_scores": {
                "clarity": round(clarity_score, 1),
                "consistency": round(consistency_score, 1),
                "constraint_compliance": constraint_score,
                "optimization": optimization_score,
                "risk_assessment": round(risk_score, 1),
                "detail_level": round(detail_score, 1)
            },
            "issues": issues,
            "improvements": improvements,
            "strengths": strengths,
            "approved": approved,
            "priority_fixes": issues[:2] if issues else []
        }
    
    def _score_clarity(self, plan_data: Dict[str, Any]) -> float:
        score = 6.0
        if plan_data.get('itinerary'): score += 1.5
        if plan_data.get('practical_info'): score += 0.5
        return min(score, 10.0)
    
    def _score_consistency(self, plan_data: Dict[str, Any]) -> float:
        score = 6.5
        if len(plan_data.get('itinerary', [])) > 1: score += 1.5
        if plan_data.get('budget_estimate'): score += 1.0
        return min(score, 10.0)
    
    def _score_risk_assessment(self, plan: Dict[str, Any]) -> float:
        score = 6.0
        if plan.get('risks'): score += 2.0
        if plan.get('alternatives'): score += 1.0
        return min(score, 10.0)
    
    def _score_detail_level(self, plan_data: Dict[str, Any]) -> float:
        score = 5.0
        itinerary = plan_data.get('itinerary', [])
        if itinerary:
            first_day = itinerary[0]
            if first_day.get('activities'): score += 2.0
            if first_day.get('accommodation'): score += 1.5
            if first_day.get('meals'): score += 1.5
        return min(score, 10.0)
    
    def _identify_issues(self, plan_data: Dict[str, Any], score: float) -> list:
        issues = []
        if score < 6.0: issues.append("Overall plan quality needs improvement")
        if not plan_data.get('practical_info'): issues.append("Missing practical information")
        return issues
    
    def _suggest_improvements(self, plan_data: Dict[str, Any], score: float) -> list:
        improvements = []
        if score < 8.0:
            improvements.append("Add more specific timing details")
            improvements.append("Include contact information")
        return improvements
    
    def _identify_strengths(self, plan_data: Dict[str, Any]) -> list:
        strengths = []
        if plan_data.get('itinerary'): strengths.append("Well-structured itinerary")
        if plan_data.get('budget_estimate'): strengths.append("Clear budget estimation")
        return strengths
