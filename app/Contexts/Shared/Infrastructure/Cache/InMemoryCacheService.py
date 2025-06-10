from app.Contexts.Shared.Application.Cache.CacheKeyGenerator import CacheKeyGenerator
from app.Contexts.Shared.Application.Cache.CacheService import CacheService


class InMemoryCacheService(CacheService):
    def __init__(self, key_generator: CacheKeyGenerator):
        self._cache: dict[str, str] = {}
        self._key_generator = key_generator

    def get(self, key: str) -> str:
        return self._cache.get(key, "")

    def set(self, key: str, value: str) -> None:
        self._cache[key] = value
