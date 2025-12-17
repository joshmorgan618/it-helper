# test_classifier.py
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from anthropic import Anthropic
from src.mas_agents.classifier_agent import ClassifierAgent
from dotenv import load_dotenv
import json

load_dotenv()

client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
agent = ClassifierAgent(client)

# Use output from IntakeAgent
parsed_ticket = {
    "user_email": "john@company.com",
    "subject": "Printer Not Working on 3rd Floor",
    "description": "I am experiencing issues printing documents on the printer located on the 3rd floor.",
    "extracted_info": {
        "device_type": "printer",
        "location": "3rd floor",
        "issue_type": "hardware",
        "urgency": "medium"
    }
}

result = agent.process(parsed_ticket)
print(json.dumps(result, indent=2))