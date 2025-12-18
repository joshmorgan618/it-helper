import redis
import os
from typing import Optional, List, Dict, Any

class RedisDB:
    """Initalize Redis Connection"""
    def __init__(self, connection_url: str):
        self.client = redis.from_url(
            connection_url,
            decode_responses=True
        )
        self.test_connection()

    def test_connection(self):
        try:
            self.client.ping()
            print("Connected to Redis")
        except redis.ConnectionError as e:
            print(f"Failed to connect to Redis: {e}")
            raise
    
    def store_resolution(self, ticket_id, category, solution, success):
        try:
            key = f"ticket:{ticket_id}"
            self.client.hset(key, mapping={
                "id": ticket_id,
                "category": category,
                "solution": solution,
                "success": int(success)
            })
        except redis.RedisError as e:
            print(f"Error storing resolution: {e}")


    def fetch_similar_resolutions(self, category, limit=5):
        try:
            keys = self.client.keys("ticket:*")
            similar_resolutions = []
            for key in keys:
                data = self.client.hgetall(key)
                if data.get("category") == category:
                    similar_resolutions.append(data)
                    if len(similar_resolutions) >= limit:
                        break
            return similar_resolutions
        except redis.RedisError as e:
            print(f"Error fetching resolutions: {e}")
            return []
    