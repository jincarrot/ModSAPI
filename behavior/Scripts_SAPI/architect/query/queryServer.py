from ..level.server import compServer
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



from ..component.index import getComponent

class _Query:
    def __init__(self, entityId, comps):
        # type: (str, list) -> None
        self.entityId = entityId
        self.comps = comps

    def iter(self):
        return getComponent(self.entityId, self.comps) or []
    
    def __enter__(self):
        result = getComponent(self.entityId, self.comps)
        if result is None:
            raise Exception()
        return result
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

def query(entityId, comps):
    # type: (int, list) -> _Query
    return _Query(entityId, comps)

queries = []

def callQueries(entityId):
    for q in queries:
        q(entityId)

def Query(*compCls):
    def decorator(fn):
        def wrapper(entityId):
            with query(entityId, compCls) as comps:
                return fn(entityId, *comps)
        queries.append(wrapper)
        return wrapper
    return decorator