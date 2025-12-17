# test_overseer.py
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from anthropic import Anthropic
from src.backend.overseer import Overseer
from dotenv import load_dotenv
import json

load_dotenv()

client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
overseer = Overseer(client)

raw_ticket = {
    "user_email": "john@company.com",
    "subject": "printer broken!!!",
    "description": "cant print on 3rd floor, need help asap"
}

result = overseer.process_ticket(raw_ticket)
print(json.dumps(result, indent=2))