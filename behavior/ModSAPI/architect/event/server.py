from .core import EventChain
from ..annotation import AnnotationHelper

import mod.server.extraServerApi as api
engine = api.GetEngineNamespace()
sysName = api.GetEngineSystemName()

class MinecraftServerEvents:
    globalEvents = {}

    @staticmethod
    def getOrCreateChain(eventType, isCustomEvent=False):
        # type: (str, bool) -> EventChain
        if eventType in MinecraftServerEvents.globalEvents:
            return MinecraftServerEvents.globalEvents[eventType]
        else:
            chain = EventChain()
            MinecraftServerEvents.globalEvents[eventType] = chain
            from ..subsystem import SubsystemManager
            SubsystemManager.getInst().addListener(eventType, lambda ev: chain.dispatch(eventType, ev), isCustomEvent)
            return chain

def event(eventType, isCustomEvent=False):
    return MinecraftServerEvents.getOrCreateChain(eventType, isCustomEvent)

def EventListener(eventType, isCustomEvent=False):
    def decorator(fn):
        # 标记方法为事件监听器
        AnnotationHelper.addAnnotation(fn, '_event_listener', eventType)
        if isCustomEvent:
            AnnotationHelper.addAnnotation(fn, '_custom_event', True)
        return fn
    return decorator
