from ..annotation import AnnotationHelper
from ..basic import isServer, clientApi, serverApi

COMPONENT_NAMESPACE = 'xxx_roninComponent_xxx'

clientCompCls = []
serverCompCls = []

components = {}

def Component(isSingleton=False, persist=False):
    def decorator(cls):
        _isServer = isServer()
        clsList = serverCompCls if _isServer else clientCompCls
        # 标记类为组件
        AnnotationHelper.addAnnotation(cls, '_component', {
            'isSingleton': isSingleton,
            'persist': persist
        })
        clsList.append(cls)
        return cls

    return decorator

def registerComponents(isServer):
    clsList = serverCompCls if isServer else clientCompCls
    api = serverApi if isServer else clientApi
    for cls in clsList:
        result = api.RegisterComponent(COMPONENT_NAMESPACE, cls.__name__, cls.__module__ + '.' + cls.__name__)
        print('[INFO] Register component', cls.__name__, 'result:', result)

def getComponentAnnotation(cls):
    return AnnotationHelper.getAnnotation(cls, '_component')

def isSingletonComponent(cls):
    ann = getComponentAnnotation(cls)
    return ann is not None and ann.get('isSingleton', False)

def isPersistComponent(cls):
    ann = getComponentAnnotation(cls)
    return ann is not None and ann.get('persist', False)

entitiesServer = {}
entitiesClient = {}

def createComponent(entityId, cls):
    # print('create component', entityId, cls)
    api = serverApi if isServer() else clientApi
    comp = api.CreateComponent(entityId, COMPONENT_NAMESPACE, cls.__name__)
    components[(entityId, cls)] = comp
    if hasattr(comp, 'onCreate'):
        comp.onCreate(entityId)

    entities = entitiesServer if isServer() else entitiesClient
    if entityId not in entities:
        entities[entityId] = 0
    entities[entityId] += 1
    return comp


def destroyComponent(entityId, cls):
    api = serverApi if isServer() else clientApi
    api.DestroyComponent(entityId, COMPONENT_NAMESPACE, cls.__name__)
    key = (entityId, cls)
    entities = entitiesServer if isServer() else entitiesClient
    if key in components:
        del components[key]
    if entityId in entities:
        entities[entityId] -= 1
        if entities[entityId] <= 0:
            del entities[entityId]


def getComponent(entityId, clsList, filter=None):
    # print(components)
    result = []
    for c in clsList:
        key = (entityId, c)
        if key in components:
            comp = components[key]
            if filter is None or filter(comp):
                result.append(components[key])
        else:
            return None
    return result


def getEntities():
    entities = entitiesServer if isServer() else entitiesClient
    return list(entities.keys())