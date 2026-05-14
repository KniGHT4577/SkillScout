import time
from typing import Any, Dict, Tuple
import asyncio

class TTLCache:
    def __init__(self, ttl_seconds: int = 60, max_size: int = 1000):
        self.ttl = ttl_seconds
        self.max_size = max_size
        self.cache: Dict[str, Tuple[float, Any]] = {}
        self.lock = asyncio.Lock()

    async def get(self, key: str) -> Any:
        async with self.lock:
            if key in self.cache:
                expiry, value = self.cache[key]
                if time.time() < expiry:
                    return value
                else:
                    del self.cache[key]
            return None

    async def set(self, key: str, value: Any):
        async with self.lock:
            if len(self.cache) >= self.max_size:
                # Simple eviction: clear expired, then if still full, clear all (for simplicity)
                now = time.time()
                expired = [k for k, (exp, _) in self.cache.items() if exp <= now]
                for k in expired:
                    del self.cache[k]
                if len(self.cache) >= self.max_size:
                    self.cache.clear()
            self.cache[key] = (time.time() + self.ttl, value)

    async def clear(self):
        async with self.lock:
            self.cache.clear()

cache = TTLCache(ttl_seconds=300)
