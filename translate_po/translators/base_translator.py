from abc import ABC, abstractmethod

import redis

from .base_config import REDIS_URL


class AbstractTranslator(ABC):

    @abstractmethod
    def translate(self, text, target_code, source_code="en"):
        pass


class RedisClient(object):
    def __init__(self):
        self.conn = redis.StrictRedis.from_url(REDIS_URL)


class TranslatorCacheController(object):
    redis_client = RedisClient()

    @classmethod
    def get_cache_key(cls, text, source_code, target_code):
        return f"{text}-{source_code}-{target_code}"

    @classmethod
    def get_cache(cls, cache_name):
        result = cls.redis_client.conn.get(cache_name)
        if result:
            print(f"{cache_name} cached successful!")
            return result.decode()

    @classmethod
    def set_cache(cls, cache_name, value):
        cls.redis_client.conn.set(cache_name, value)
