from .base_agent import BaseAgent
import json

# Agent used to intake and parse new tickets
class IntakeAgent(BaseAgent):
    def __init__(self, client):
        super().__init__(client, name="IntakeAgent")
    
    def process(self, ticket_data):
        self.log_action("Processing new ticket")
        
        system_prompt = """
You are an Intake Agent for IT support. Analyze the ticket and return ONLY valid JSON (no markdown, no backticks).

Extract and structure the following:
- Clean up the subject line
- Improve and clarify the description with any relevant details from the input

Return this exact JSON structure:
{
    "user_email": "email from input",
    "subject": "cleaned subject",
    "description": "improved description"
}
"""
        
        messages = [
            {"role": "user", "content": f"Ticket Data: {json.dumps(ticket_data)}"}
        ]
        
        response = self.call_claude(messages, system_prompt)
        
        if not response:
            self.log_action("Failed to get response from Claude")
            return None
        
        try:
            # Parse JSON response
            parsed = json.loads(response)
            self.log_action("Successfully processed ticket")
            return parsed
        except json.JSONDecodeError as e:
            self.log_action(f"Failed to parse JSON: {e}")
            self.log_action(f"Raw response: {response}")
            return None