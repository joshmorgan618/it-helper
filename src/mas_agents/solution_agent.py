from .base_agent import BaseAgent
import json

class SolutionAgent(BaseAgent):
    def __init__(self, client):
        super().__init__(client, name="SolutionAgent")
    
    def process(self, diagnosis, fetched_data):
        """
        Generate solution based on diagnosis and past solutions
        
        Args:
            diagnosis: Output from DiagnosticAgent
            fetched_data: Output from FetchAgent with past solutions
        """
        self.log_action("Generating solution")
        
        system_prompt = """
You are a Solution Agent for IT support. Based on the diagnosis and fetched data, provide a comprehensive solution.

IMPORTANT: Return ONLY valid JSON. For multi-line text, use \\n for newlines.

Return this exact JSON structure:
{
    "solution": "Step 1: Do this\\nStep 2: Do that\\nStep 3: Complete",
    "tools_needed": ["tool1", "tool2"],
    "estimated_time": "time estimate",
    "confidence": "high|medium|low",
    "alternative_solutions": ["option1", "option2"]
}
"""
        
        messages = [
            {
                "role": "user", 
                "content": f"Diagnosis: {json.dumps(diagnosis)}\n\nFetched Data: {json.dumps(fetched_data)}"
            }
        ]
        
        response = self.call_claude(messages, system_prompt)
        
        if not response:
            self.log_action("Failed to get response from Claude")
            return None
        
        try:
            solution = json.loads(response)
            self.log_action("Successfully generated solution")
            return solution
        except json.JSONDecodeError as e:
            self.log_action(f"Failed to parse JSON: {e}")
            self.log_action(f"Raw response: {response}")
            return None