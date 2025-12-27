"""
Redis Memory Service for IT Support Ticket Resolution Storage
"""

import redis
from typing import Optional, List, Dict, Any
from datetime import datetime


class RedisDB:
    """Redis service for storing and retrieving ticket resolutions"""
    
    # Key prefixes for organization
    TICKET_PREFIX = "ticket:"
    CATEGORY_INDEX_PREFIX = "category:"
    
    # Default TTL: 90 days (in seconds)
    DEFAULT_TTL = 90 * 24 * 60 * 60
    
    def __init__(self, connection_url: str):
        """Initialize Redis connection"""
        try:
            self.client = redis.from_url(
                connection_url,
                decode_responses=True,
                socket_connect_timeout=5
            )
            self.test_connection()
        except redis.ConnectionError as e:
            print(f"Failed to connect to Redis: {e}")
            raise
    
    def test_connection(self) -> None:
        """Verify Redis connection is working"""
        try:
            self.client.ping()
            print("Connected to Redis")
        except redis.ConnectionError as e:
            print(f"Redis connection failed: {e}")
            raise
    
    def store_resolution(
        self, 
        ticket_id: str, 
        category: str, 
        solution: str, 
        success: bool,
        ttl: int = DEFAULT_TTL
    ) -> bool:
        """
        Store ticket resolution with automatic indexing and expiration
        
        Args:
            ticket_id: Unique ticket identifier
            category: Ticket category (hardware/software/network/access)
            solution: The solution that was applied
            success: Whether the solution worked
            ttl: Time to live in seconds (default: 90 days)
        
        Returns:
            bool: True if stored successfully, False otherwise
        """
        try:
            ticket_key = f"{self.TICKET_PREFIX}{ticket_id}"
            category_index_key = f"{self.CATEGORY_INDEX_PREFIX}{category.lower()}"
            
            # Use pipeline for atomic operations
            pipe = self.client.pipeline()
            
            # Store ticket data
            pipe.hset(ticket_key, mapping={
                "id": ticket_id,
                "category": category.lower(),
                "solution": solution,
                "success": int(success),
                "timestamp": datetime.utcnow().isoformat()
            })
            pipe.expire(ticket_key, ttl)
            
            # Add to category index for fast retrieval
            pipe.sadd(category_index_key, ticket_id)
            pipe.expire(category_index_key, ttl)
            
            pipe.execute()
            return True
            
        except redis.RedisError as e:
            print(f"Error storing resolution {ticket_id}: {e}")
            return False
    
    def fetch_similar_resolutions(
        self, 
        category: str, 
        limit: int = 5,
        only_successful: bool = False
    ) -> List[Dict[str, Any]]:
        """
        Fetch similar ticket resolutions by category using indexed lookup
        
        Args:
            category: Category to search for
            limit: Maximum number of results to return
            only_successful: Only return successful resolutions
        
        Returns:
            List of resolution dictionaries
        """
        try:
            category_index_key = f"{self.CATEGORY_INDEX_PREFIX}{category.lower()}"
            
            # Get ticket IDs from category index (O(1) lookup)
            ticket_ids = self.client.smembers(category_index_key)
            
            if not ticket_ids:
                return []
            
            # Fetch ticket data using pipeline for efficiency
            pipe = self.client.pipeline()
            for ticket_id in ticket_ids:
                pipe.hgetall(f"{self.TICKET_PREFIX}{ticket_id}")
            
            results = pipe.execute()
            
            # Filter and collect results
            similar_resolutions = []
            for data in results:
                if not data:  # Skip expired/deleted tickets
                    continue
                
                # Filter by success if requested
                if only_successful and data.get("success") != "1":
                    continue
                
                similar_resolutions.append(data)
                
                if len(similar_resolutions) >= limit:
                    break
            
            return similar_resolutions
            
        except redis.RedisError as e:
            print(f"Error fetching resolutions for {category}: {e}")
            return []
    
    def get_resolution(self, ticket_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a specific ticket resolution by ID
        
        Args:
            ticket_id: Ticket ID to retrieve
        
        Returns:
            Resolution dictionary or None if not found
        """
        try:
            ticket_key = f"{self.TICKET_PREFIX}{ticket_id}"
            data = self.client.hgetall(ticket_key)
            return data if data else None
        except redis.RedisError as e:
            print(f"Error fetching ticket {ticket_id}: {e}")
            return None
    
    def delete_resolution(self, ticket_id: str) -> bool:
        """
        Delete a ticket resolution and remove from indexes
        
        Args:
            ticket_id: Ticket ID to delete
        
        Returns:
            bool: True if deleted successfully
        """
        try:
            ticket_key = f"{self.TICKET_PREFIX}{ticket_id}"
            
            # Get category before deletion for index cleanup
            data = self.client.hgetall(ticket_key)
            if not data:
                return False
            
            category = data.get("category")
            
            # Delete ticket and remove from category index
            pipe = self.client.pipeline()
            pipe.delete(ticket_key)
            if category:
                category_index_key = f"{self.CATEGORY_INDEX_PREFIX}{category}"
                pipe.srem(category_index_key, ticket_id)
            pipe.execute()
            
            return True
            
        except redis.RedisError as e:
            print(f"Error deleting ticket {ticket_id}: {e}")
            return False