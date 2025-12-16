import sys
import os

# Add backend folder to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src', 'backend'))

from redis_client import RedisDB
from dotenv import load_dotenv

load_dotenv()

# Test connection
print("Testing Redis connection...")
redis_client = RedisDB(os.getenv('REDIS_URL'))

# Test storing resolutions
print("\nStoring test resolutions...")
redis_client.store_resolution("TKT-001", "hardware", "Reset printer", True)
redis_client.store_resolution("TKT-002", "hardware", "Replace cable", True)
redis_client.store_resolution("TKT-003", "software", "Reinstall driver", True)

# Test fetching
print("\nFetching hardware resolutions...")
results = redis_client.fetch_similar_resolutions("hardware", limit=5)
print(f"Found {len(results)} hardware resolutions:")
for r in results:
    print(f"  - {r['id']}: {r['solution']}")

print("\nFetching software resolutions...")
results = redis_client.fetch_similar_resolutions("software", limit=5)
print(f"Found {len(results)} software resolutions:")
for r in results:
    print(f"  - {r['id']}: {r['solution']}")