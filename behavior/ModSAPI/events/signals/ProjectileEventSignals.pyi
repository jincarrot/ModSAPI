# -*- coding: utf-8 -*-
# stub file for projectile events module
import types
from ..EventBases import Events


class ProjectileHitBlockAfterEventSignal(Events):
    """
    Manages callbacks that are connected to when a projectile hits a block.
    """
    def subscribe(self, callback: types.FunctionType) -> None:
        """
        Adds a callback that will be called when a projectile hits a block.
        """
        ...

class ProjectileHitEntityAfterEventSignal(Events):
    """
    Manages callbacks that are connected to when a projectile hits an entity.
    """
    def subscribe(self, callback: types.FunctionType) -> None:
        """
        Adds a callback that will be called when a projectile hits an entity.
        """
        ...