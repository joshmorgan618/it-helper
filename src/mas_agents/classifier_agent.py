from src.mas_agents.base_agent import BaseAgent
import json

class ClassifierAgent(BaseAgent):
    def __init__(self, client):
        super().__init__(client, name="ClassifierAgent")
    
    def process(self, parsed_ticket):
        self.log_action("Classifying ticket")
        
        system_prompt = """
You are a Classifier Agent for IT support. Analyze the ticket and return ONLY valid JSON.

Classify the ticket into:
- Category: "hardware", "software", "network", or "access"
- Urgency: "low", "medium", "high", or "critical"
- Expertise Level: "tier1" (basic), "tier2" (intermediate), "tier3" (advanced)

Return this exact JSON structure:
{
    "category": "hardware|software|network|access",
    "urgency": "low|medium|high|critical",
    "expertise_level": "tier1|tier2|tier3",
    "reasoning": "brief explanation of classification"
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