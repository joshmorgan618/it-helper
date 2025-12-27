from .base_agent import BaseAgent
import json
import time
from typing import Optional, Dict, Any

class ClassifierAgentLite(BaseAgent):
    """
    Lightweight Classifier Agent with optimized prompt for cost/performance.

    Use this when:
    - Processing high volumes (>10k tickets/day)
    - Cost is a primary concern
    - Latency must be minimized
    - Classification is relatively straightforward

    Use ClassifierAgent (full version) when:
    - Accuracy is critical
    - Handling complex/ambiguous cases
    - Need detailed reasoning
    - Lower volumes where cost is acceptable
    """

    def __init__(self, client):
        super().__init__(client, name="ClassifierAgentLite")
        self.metrics = {
            "total_requests": 0,
            "successful_parses": 0,
            "failed_parses": 0,
            "average_response_time": 0.0
        }

    def _build_optimized_prompt(self) -> str:
        """
        Optimized prompt: ~400 tokens (vs 1400 in full version)

        Keeps:
        - Essential guidelines
        - 2 key examples (vs 5)
        - Basic validation

        Removes:
        - Verbose explanations
        - Reasoning process section
        - Extended edge case discussion
        """
        return """You are an IT support classifier. Return ONLY valid JSON.

Categories: "hardware" (devices), "software" (apps/OS), "network" (connectivity), "access" (login/permissions)
Urgency: "low" (requests), "medium" (workarounds exist), "high" (blocking work), "critical" (outages/security)
Expertise: "tier1" (common), "tier2" (technical), "tier3" (complex/custom)

Examples:
1. Input: {"subject": "Printer not working", "description": "Office printer won't print"}
   Output: {"category": "hardware", "urgency": "medium", "expertise_level": "tier1", "reasoning": "Hardware issue, has workarounds"}

2. Input: {"subject": "Email server down", "description": "Company-wide email outage"}
   Output: {"category": "network", "urgency": "critical", "expertise_level": "tier2", "reasoning": "Critical outage affecting all users"}

Return:
{
    "category": "hardware|software|network|access",
    "urgency": "low|medium|high|critical",
    "expertise_level": "tier1|tier2|tier3",
    "reasoning": "brief explanation"
}"""

    def _validate_classification(self, classification: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        """Quick validation - only checks essentials"""
        required = ["category", "urgency", "expertise_level"]
        for field in required:
            if field not in classification:
                return False, f"Missing: {field}"

        if classification["category"] not in ["hardware", "software", "network", "access"]:
            return False, "Invalid category"
        if classification["urgency"] not in ["low", "medium", "high", "critical"]:
            return False, "Invalid urgency"
        if classification["expertise_level"] not in ["tier1", "tier2", "tier3"]:
            return False, "Invalid expertise_level"

        return True, None

    def _update_metrics(self, response_time: float, parse_success: bool):
        """Simplified metrics tracking"""
        self.metrics["total_requests"] += 1
        if parse_success:
            self.metrics["successful_parses"] += 1
        else:
            self.metrics["failed_parses"] += 1

        total = self.metrics["total_requests"]
        current_avg = self.metrics["average_response_time"]
        self.metrics["average_response_time"] = ((current_avg * (total - 1)) + response_time) / total

    def get_metrics(self) -> Dict[str, Any]:
        """Get performance metrics"""
        total = self.metrics["total_requests"]
        return {
            **self.metrics,
            "parse_success_rate": self.metrics["successful_parses"] / total if total > 0 else 0
        }

    def process(self, parsed_ticket: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Lightweight processing with minimal overhead"""
        start_time = time.time()

        system_prompt = self._build_optimized_prompt()
        messages = [{"role": "user", "content": f"{json.dumps(parsed_ticket)}"}]

        # Still use lower temperature for consistency
        response = self.call_claude(messages, system_prompt, temperature=0.3)
        response_time = time.time() - start_time

        if not response:
            self._update_metrics(response_time, False)
            return None

        try:
            classification = json.loads(response)
        except json.JSONDecodeError:
            self._update_metrics(response_time, False)
            return None

        is_valid, _ = self._validate_classification(classification)
        if not is_valid:
            self._update_metrics(response_time, False)
            return None

        self._update_metrics(response_time, True)
        return classification
