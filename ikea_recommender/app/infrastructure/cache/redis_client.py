import redis
import json
from typing import Optional, Any

class RedisCacheClient:
    def __init__(self, host: str = 'localhost', port: int = 6379, db: int = 0):
        self._redis = redis.StrictRedis(host=host, port=port, db=db, decode_responses=True)

    def get(self, key: str) -> Optional[Any]:
        value = self._redis.get(key)
        if value:
            return json.loads(value)
        return None

    def set(self, key: str, value: Any, expire: int = 3600):
        self._redis.setex(key, expire, json.dumps(value))

    def delete(self, key: str):
        self._redis.delete(key)
