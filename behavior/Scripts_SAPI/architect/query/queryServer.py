from ..levelServer import compServer
from .cache import QueryCache

class QueryServer:
    _caches = {}

    @staticmethod
    def cache(key, id, getter):
        # type: (str, int, object) -> QueryCache
        keyedCache = QueryServer._caches.get(key, {})
        if id not in keyedCache:
            qc = QueryCache(getter)
            keyedCache[id] = qc
            QueryServer._caches[key] = keyedCache
            return qc.get()
        else:
            qc = keyedCache[id] # type: QueryCache
            return qc.get()

    @staticmethod
    def queryOfKey(key, entityFilter=None):
        # type: (str, object) -> dict[str, QueryCache]
        cached = QueryServer._caches.get(key, {})
        if filter is None:
            return cached
        else:
            return { k: v for k, v in cached.items() if entityFilter(k) }

    @staticmethod
    def cache(key, id, getter):
        # type: (str, int, object) -> QueryCache
        keyedCache = QueryServer._caches.get(key, {})
        if id not in keyedCache:
            qc = QueryCache(getter)
            keyedCache[id] = qc
            QueryServer._caches[key] = keyedCache
            return qc.get()
        else:
            qc = keyedCache[id] # type: QueryCache
            return qc.get()
    
    @staticmethod
    def pos(id):
        return QueryServer.cache('pos', id, lambda: compServer.CreatePos(id)).get()
    
    @staticmethod
    def action(id):
        return compServer.CreateAction(id)
    
    @staticmethod
    def dimension(id):
        return compServer.CreateDimension(id)
