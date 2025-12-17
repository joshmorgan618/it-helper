class FetchAgent:  # Maybe don't inherit from BaseAgent?
    def __init__(self, redis_client, chroma_client):
        self.redis_client = redis_client
        self.chroma_client = chroma_client  # When you set up ChromaDB
        self.name = "FetchAgent"
    
    def process(self, query_data):
        """
        Search for relevant documentation and past solutions
        
        query_data = {
            "category": "hardware",
            "issue_type": "printer",
            "keywords": ["connection", "network"]
        }
        """
        results = {}
        
        # Search Redis for past solutions
        if self.redis_client:
            past_tickets = self.redis_client.fetch_similar_resolutions(
                category=query_data.get('category'),
                limit=5
            )
            results['past_solutions'] = past_tickets
        
        # Search ChromaDB for docs (when implemented)
        # if self.chroma_client:
        #     docs = self.chroma_client.search(...)
        #     results['documentation'] = docs
        
        return results