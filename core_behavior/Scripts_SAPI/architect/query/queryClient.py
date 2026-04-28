from ..levelClient import compClient
from .cache import QueryCache


class QueryClient:
    _caches = {}

    @staticmethod
    def cache(key, id, getter):
        # type: (str, int, object) -> QueryCache
        keyedCache = QueryClient._caches.get(key, {})
        if id not in keyedCache:
            qc = QueryCache(getter)
            keyedCache[id] = qc
            QueryClient._caches[key] = keyedCache
            return qc.get()
        else:
            qc = keyedCache[id] # type: QueryCache
            return qc.get()

    @staticmethod
    def queryOfKey(key, entityFilter=None):
        # type: (str, object) -> dict[str, QueryCache]
        cached = QueryClient._caches.get(key, {})
        if filter is None:
            return cached
        else:
            return { k: v for k, v in cached.items() if entityFilter(k) }
        
    @staticmethod
    def queryOfEntity(entityId, keyFilter=None):
        # type: (int, object) -> dict[str, QueryCache]
        return { k: v[entityId] for k, v in QueryClient._caches.items() if entityId in v and (keyFilter is None or keyFilter(k)) }

    @staticmethod
    def pos(id):
        return compClient.CreatePos(id)
    
    @staticmethod
    def type(id):
        return compClient.CreateEngineType(id)

    @staticmethod
    def rot(id):
        return compClient.CreateRot(id)
    
    @staticmethod
    def action(id):
        return compClient.CreateAction(id)
    
    @staticmethod
    def motion(id):
        return compClient.CreateActorMotion(id)
