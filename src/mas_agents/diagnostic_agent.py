from .base_agent import BaseAgent
import json

class DiagnosticAgent(BaseAgent):
    def __init__(self, client):
        super().__init__(client, name="DiagnosticAgent")
    
    def process(self, classified_ticket):
        self.log_action("Diagnosing ticket")
        
        system_prompt = """
You are a Diagnostic Agent for IT support. Analyze the classified ticket and return ONLY valid JSON.

Based on the category and issue type, provide a detailed diagnosis of the problem.

Return this exact JSON structure:
{
    "diagnosis": "detailed diagnosis of the issue",
    "potential_causes": ["list", "of", "potential", "causes"],
    "recommended_tests": ["list", "of", "tests", "to", "perform"],
    "category": "extract category from ticket",
    "issue_type": "extract issue type",
    "keywords": ["relevant", "keywords", "for", "searching"]
}
"""
        
        messages = [
            {"role": "user", "content": f"Classified Ticket Data: {json.dumps(classified_ticket)}"}
        ]
        
        response = self.call_claude(messages, system_prompt)
        
        if not response:
            self.log_action("Failed to get response from Claude")
            return None
        
        try:
            diagnosis = json.loads(response)
            self.log_action("Successfully diagnosed the issue")
            return diagnosis
        except json.JSONDecodeError as e:
            self.log_action(f"Failed to parse JSON: {e}")
            self.log_action(f"Raw response: {response}")
            return None