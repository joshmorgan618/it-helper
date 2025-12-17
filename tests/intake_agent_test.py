import sys
import os

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from anthropic import Anthropic
from src.mas_agents.intake_agent import IntakeAgent
from dotenv import load_dotenv

load_dotenv()

client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
agent = IntakeAgent(client)

raw_ticket = {
    "user_email": "john@company.com",
    "subject": "printer broken!!!",
    "description": "cant print on 3rd floor"
}

result = agent.process(raw_ticket)
print(result)