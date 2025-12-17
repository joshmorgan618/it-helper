from anthropic import Anthropic
import os
from dotenv import load_dotenv
from os import getenv

load_dotenv()

class BaseAgent:
    def __init__(self, client: Anthropic, name: str = "BaseAgent"):
        self.client = client
        self.name = name
    
    def call_claude(self, messages: list, system_prompt: str) -> str:
        """Call Claude API and return response text"""
        try:
            response = self.client.messages.create(
                model=getenv('MODEL'),
                max_tokens=4096,
                system=system_prompt,
                messages=messages
            )
            return response.content[0].text
        except Exception as e:
            self.log_action(f"Error: {e}")
            return None
    
    def log_action(self, action: str):
        """Log agent actions"""
        print(f"[{self.name}] {action}")
    
    def process(self, input_data):
        """Must be implemented by subclasses"""
        raise NotImplementedError(f"{self.name} must implement process()")