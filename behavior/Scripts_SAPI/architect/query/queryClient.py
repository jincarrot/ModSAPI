from ..level.client import compClient, clientApi
from .cache import QueryCache
from ..annotation import AnnotationHelper

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


from ..component import getComponent

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
        return True

def query(entityId, comps):
    # type: (int, list) -> _Query
    return _Query(entityId, comps)

queries = []

def callQueries(entityId, frameUpdate=False):
    for q in queries:
        anyFrame = AnnotationHelper.getAnnotation(q, 'AnyFrame') or False
        if frameUpdate == anyFrame:
            q(entityId)


def Query(*compCls):
    def decorator(fn):
        def wrapper(entityId):
            comps = getComponent(entityId, compCls)
            if comps:
                return fn(entityId, *comps)
        queries.append(wrapper)
        return wrapper
    return decorator


def QueryAnyFrame(*compCls):
    def decorator(fn):
        def wrapper(entityId):
            comps = getComponent(entityId, compCls)
            if comps:
                return fn(entityId, *comps)
        queries.append(wrapper)
        AnnotationHelper.addAnnotation(wrapper, 'AnyFrame', True)
        return wrapper
    return decorator