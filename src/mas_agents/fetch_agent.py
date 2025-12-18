import json

class FetchAgent:
    """Knowledge retrieval agent - searches databases for relevant information"""
    
    def __init__(self, redis_client):
        self.redis_client = redis_client
        self.name = "FetchAgent"
    
    def log_action(self, action: str):
        """Log agent actions"""
        print(f"[{self.name}] {action}")
    
    def process(self, query_data):
        """
        Search for relevant documentation and past solutions
        
        Args:
            query_data: dict with 'category' and optional 'keywords'
            Example: {
                "category": "hardware",
                "issue_type": "printer",
                "keywords": ["connection", "network"]
            }
        
        Returns:
            dict with search results
        """
        self.log_action(f"Searching for category: {query_data.get('category')}")
        
        results = {
            "past_solutions": [],
            "search_query": query_data
        }
        
        # Search Redis for similar past tickets
        if self.redis_client:
            try:
                past_tickets = self.redis_client.fetch_similar_resolutions(
                    category=query_data.get('category'),
                    limit=5
                )
                results['past_solutions'] = past_tickets
                self.log_action(f"Found {len(past_tickets)} similar past tickets")
            except Exception as e:
                self.log_action(f"Error searching Redis: {e}")
                results['past_solutions'] = []
        
        # TODO: Add ChromaDB search when implemented
        # if self.chroma_client:
        #     docs = self.chroma_client.search(query_data.get('keywords'))
        #     results['documentation'] = docs
        
        return results