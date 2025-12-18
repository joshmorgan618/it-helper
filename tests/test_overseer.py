# test_full_workflow.py
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from anthropic import Anthropic
from src.backend.overseer import Overseer
from src.backend.redis_client import RedisDB
from dotenv import load_dotenv
import json

load_dotenv()

# Initialize clients
anthropic_client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
redis_client = RedisDB(os.getenv('REDIS_URL'))

# Create orchestrator
overseer = Overseer(anthropic_client, redis_client)

# Test ticket
raw_ticket = {
    "user_email": "john@company.com",
    "subject": "printer broken!!!",
    "description": "cant print on 3rd floor, need help asap for meeting"
}

# Process through full workflow
result = overseer.process_ticket(raw_ticket)

# Print results
print(json.dumps(result, indent=2))