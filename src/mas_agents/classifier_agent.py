from .base_agent import BaseAgent
import json

#Agent used to classify tickets into categories, urgency levels, and expertise levels
class ClassifierAgent(BaseAgent):
    def __init__(self, client):
        super().__init__(client, name="ClassifierAgent")
    
    def process(self, parsed_ticket):
        self.log_action("Classifying ticket")
        
        system_prompt = """
You are an IT Diagnostic Agent. Analyze the classified ticket and return ONLY valid JSON.

Provide technical diagnosis based on:
- hardware: Physical connections, drivers, device health
- software: Versions, configs, conflicts, dependencies
- network: Connectivity layers, DNS, routing, ports
- access: Credentials, permissions, group memberships

Return:
{
    "diagnosis": "concise technical explanation of the problem",
    "potential_causes": ["specific", "technical", "root", "causes"],
    "recommended_tests": ["diagnostic", "steps", "simple", "to", "complex"]
}

Example:
Input: {"category": "hardware", "subject": "Printer offline", "urgency": "medium"}
Output: {
    "diagnosis": "Printer connectivity failure, likely network or driver issue",
    "potential_causes": ["Network cable disconnected", "Print spooler stopped", "Driver crashed", "IP conflict"],
    "recommended_tests": ["Check physical connections", "Ping printer IP", "Restart print spooler", "Reinstall driver"]
}
"""

        messages = [
            {"role": "user", "content": f"Ticket Data: {json.dumps(parsed_ticket)}"}
        ]
        
        response = self.call_claude(messages, system_prompt)
        
        if not response:
            self.log_action("Failed to get response from Claude")
            return None
        
        try:
            classification = json.loads(response)
            self.log_action(f"Classified as: {classification.get('category')} - {classification.get('urgency')}")
            return classification
        except json.JSONDecodeError as e:
            self.log_action(f"Failed to parse JSON: {e}")
            self.log_action(f"Raw response: {response}")
            return None