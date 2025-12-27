from anthropic import Anthropic
import os
from dotenv import load_dotenv
from os import getenv

load_dotenv()

class BaseAgent:
    def __init__(self, client: Anthropic, name: str = "BaseAgent"):
        self.client = client
        self.name = name
    
    def call_claude(self, messages: list, system_prompt: str, temperature: float = 1.0) -> str:
        """
        Call Claude API and return response text

        Args:
            messages: List of message dictionaries for the conversation
            system_prompt: System prompt defining agent behavior
            temperature: Controls randomness (0.0-1.0). Lower = more deterministic.
                        Default is 1.0 for creative responses.
                        Use 0.2-0.3 for consistent, factual outputs.

        Returns:
            Response text from Claude or None if error occurs
        """
        try:
            response = self.client.messages.create(
                model=getenv('MODEL'),
                max_tokens=4096,
                temperature=temperature,
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