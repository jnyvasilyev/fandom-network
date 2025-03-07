"""
Cache class for storing and retrieving data
"""

import json
import os
from typing import Dict, Any

class Cache:
    def __init__(self, cache_dir: str = ".cache"):
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)
    
    def get(self, key: str) -> Any:
        """Get a value from the cache"""
        try:
            with open(os.path.join(self.cache_dir, f"{key}.json"), 'r') as f:
                return json.load(f)
        except:
            return None
    
    def set(self, key: str, value: Any):
        """Set a value in the cache"""
        with open(os.path.join(self.cache_dir, f"{key}.json"), 'w') as f:
            json.dump(value, f)
    
    def clear(self):
        """Clear all cached data"""
        for file in os.listdir(self.cache_dir):
            if file.endswith('.json'):
                os.remove(os.path.join(self.cache_dir, file)) 