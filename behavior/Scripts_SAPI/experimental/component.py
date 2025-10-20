from functools import wraps
import mod.client.extraClientApi as clientApi
import mod.client.extraClientApi as serverApi
from .env_config import componentNamespace

componentMetas = {}

def component(name, singleton=False, autoInstance=False):
    def decorator(cls):
        metadata = componentMetas[cls] or {}
        if singleton:
            metadata['singleton'] = True
        if autoInstance:
            metadata['autoInstance'] = True
        componentMetas[cls] = metadata
        clientApi.RegisterComponent(
            componentNamespace,
            name,
            None
        )
        return cls
    return decorator

def getComponentMeta(cls):
    return componentMetas[cls]

def isSingleton(cls):
    meta = getComponentMeta(cls)
    return None if not meta else meta['singleton']

def isAutoInstance(cls):
    meta = getComponentMeta(cls)
    return None if not meta else meta['autoInstance']