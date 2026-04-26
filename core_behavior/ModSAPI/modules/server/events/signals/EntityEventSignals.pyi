# -*- coding: utf-8 -*-
# stub file for entity events module
import types
from typing import Any, Callable, Dict, Optional, Union, Tuple
from ..EventBases import Events
from .....interfaces.EntityOptions import EntityEventOptions
import mod.server.extraServerApi as serverApi


class EntityEvents(Events):
    def __init__(self) -> None: ...
    def subscribe(
        self, callback: types.FunctionType, options: Optional[Union[Dict[str, Any], EntityEventOptions]] = None
    ) -> None: ...
    def unsubscribe(self, callback: types.FunctionType) -> None: ...

class EntityDieAfterEventSignal(EntityEvents):
    """
    Supports registering for an event that fires after an entity has died.
    """
    def subscribe(
        self, callback: types.FunctionType, options: Optional[Union[Dict[str, Any], EntityEventOptions]] = None
    ) -> None:
        """Subscribes to an event that fires when an entity dies."""
        ...
    def unsubscribe(self, callback: types.FunctionType) -> None: ...

class EffectAddAfterEventSignal(EntityEvents):
    """
    Manages callbacks that are connected to when an effect is added to an entity.
    """
    def subscribe(
        self, callback: types.FunctionType, options: Optional[Union[Dict[str, Any], EntityEventOptions]] = None
    ) -> None:
        """Adds a callback that will be called when an effect is added to an entity."""
        ...

class EntityHealthChangedAfterEventSignal(EntityEvents):
    """
    Manages callbacks that are connected to when the health of an entity changes.
    """
    def subscribe(
        self, callback: types.FunctionType, options: Optional[Union[Dict[str, Any], EntityEventOptions]] = None
    ) -> None:
        """Adds a callback that will be called when the health of an entity changes."""
        ...

class __EntityHitBlockAfterEventSignal(EntityEvents):
    """
    Manages callbacks that are connected to when an effect is added to an entity.
    """
    def subscribe(
        self, callback: types.FunctionType, options: Optional[Union[Dict[str, Any], EntityEventOptions]] = None
    ) -> None:
        """
        Adds a callback that will be called when an effect is added to an entity.
        """
        ...

class EntityHitEntityAfterEventSignal(EntityEvents):
    """
    Manages callbacks that are connected to when an entity makes a melee attack on another entity.
    """
    def subscribe(
        self, callback: types.FunctionType, options: Optional[Union[Dict[str, Any], EntityEventOptions]] = None
    ) -> None:
        """
        Adds a callback that will be called when an entity hits another entity.
        """
        ...

class EntityHurtAfterEventSignal(EntityEvents):
    """
    Manages callbacks that are connected to when an effect is added to an entity.
    """
    def subscribe(
        self, callback: types.FunctionType, options: Optional[Union[Dict[str, Any], EntityEventOptions]] = None
    ) -> None:
        """
        Adds a callback that will be called when an effect is added to an entity.
        """
        ...

class EntityLoadAfterEventSignal(EntityEvents):
    """
    Registers a script-based event handler for handling what happens when an entity loads.
    """
    def subscribe(
        self, callback: types.FunctionType, options: Optional[Union[Dict[str, Any], EntityEventOptions]] = None
    ) -> None:
        """
        Adds a callback that will be called when an effect is added to an entity.
        """
        ...

class EntityRemoveAfterEventSignal(EntityEvents):
    """
    Allows registration for an event that fires when an entity is being removed from the game

    (for example, unloaded, or a few seconds after they are dead.)
    """
    def subscribe(
        self, callback: types.FunctionType, options: Optional[Union[Dict[str, Any], EntityEventOptions]] = None
    ) -> None:
        """
        Will call your function every time an entity is being removed from the game.
        """
        ...

class EntitySpawnAfterEventSignal(EntityEvents):
    """
    Registers a script-based event handler for handling what happens when an entity spawns.
    """
    def subscribe(
        self, callback: types.FunctionType, options: Optional[Union[Dict[str, Any], EntityEventOptions]] = None
    ) -> None:
        """
        Adds a callback that will be called when an effect is added to an entity.
        """
        ...

class DataDrivenEntityTriggerEventSignal(EntityEvents):
    """
    Contains event registration related to firing of a data driven entity event -
    for example, the minecraft:ageable_grow_up event on a chicken.
    """
    def subscribe(
        self, callback: types.FunctionType, options: Optional[Union[Dict[str, Any], EntityEventOptions]] = None
    ) -> None:
        """
        Adds a callback that will be called after a data driven entity event is triggered.
        """
        ...

class EntityHurtBeforeEventSignal(EntityEvents):
    """
    Manages callbacks that are connected to when an entity hurt.
    """
    def subscribe(
        self, callback: types.FunctionType, options: Optional[Union[Dict[str, Any], EntityEventOptions]] = None
    ) -> None:
        """
        Adds a callback that will be called when an effect is added to an entity.
        """
        ...