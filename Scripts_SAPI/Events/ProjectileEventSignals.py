# coding=utf-8

from EventBases import *
import mod.server.extraServerApi as serverApi
from ..decorators import *


class ProjectileHitBlockAfterEventSignal(Events):
    """
    Manages callbacks that are connected to when a projectile hits a block.
    """

    def __init__(self):
        Events.__init__(self)
        self.__eventName = "ProjectileDoHitEffectEvent"

    def _check(self, __obj, data, __valueName):
        # type: (EventListener, dict, str) -> bool
        if data['hitTargetType'] == "BLOCK":
            return True
        else:
            return False

    def subscribe(self, callback):
        # type: (types.FunctionType) -> None
        """
        Adds a callback that will be called when a projectile hits a block.
        """
        import ProjectileEvents as pe
        self._events[id(callback)] = EventListener(self.__eventName, callback, None, self._check, None, pe.ProjectileHitBlockAfterEvent)

class ProjectileHitEntityAfterEventSignal(Events):
    """
    Manages callbacks that are connected to when a projectile hits an entity.
    """

    def __init__(self):
        Events.__init__(self)
        self.__eventName = "ProjectileDoHitEffectEvent"

    def _check(self, __obj, data, __valueName):
        # type: (EventListener, dict, str) -> bool
        if data['hitTargetType'] == "ENTITY":
            return True
        else:
            return False

    def subscribe(self, callback):
        # type: (types.FunctionType) -> None
        """
        Adds a callback that will be called when a projectile hits an entity.
        """
        import ProjectileEvents as pe
        self._events[id(callback)] = EventListener(self.__eventName, callback, None, self._check, None, pe.ProjectileHitEntityAfterEvent)
