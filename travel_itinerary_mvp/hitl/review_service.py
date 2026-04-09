"""
Human-in-the-loop review service.
Handles plans that require manual approval.
"""

from typing import Dict, Any


class HumanReviewService:

    def review(self, plan: Dict[str, Any], decision: str) -> Dict[str, Any]:
        """
        decision: approve | reject | edit
        """

        if decision == "approve":
            plan["status"] = "approved_by_human"
        elif decision == "reject":
            plan["status"] = "rejected_by_human"
        elif decision == "edit":
            plan["status"] = "edited_by_human"
        else:
            raise ValueError("Invalid decision")

        return plan
