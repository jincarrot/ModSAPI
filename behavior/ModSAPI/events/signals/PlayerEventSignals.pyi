# -*- coding: utf-8 -*-
# stub file for player events module
import types
from ..EventBases import Events

class ChatSendAfterEventSignal(Events):
    """
    Manages callbacks that are connected to chat messages being sent.
    """
    def subscribe(self, callback: types.FunctionType) -> None:
        """
        Adds a callback that will be called when new chat messages are sent.
        """
        ...

class ItemUseAfterEventSignal(Events):
    """
    Manages callbacks that are connected to an item use event.
    """
    def subscribe(self, callback: types.FunctionType) -> None:
        """
        Adds a callback that will be called when an item is used.
        """
        ...

class ItemStartUseOnAfterEventSignal(Events):
    """
    Manages callbacks that are connected to an item use event.
    """
    def subscribe(self, callback: types.FunctionType) -> None:
        """
        Adds a callback that will be called when an item is used.
        """
        ...

class ItemCompleteUseAfterEventSignal(Events):
    """
    Manages callbacks that are connected to the completion of charging for a chargeable item.
    """
    def subscribe(self, callback: types.FunctionType) -> None:
        """
        Adds a callback that will be called when a chargeable item completes charging.
        """
        ...

class PlayerDimensionChangeAfterEventSignal(Events):
    """
    Manages callbacks that are connected to successful player dimension changes.
    """
    def subscribe(self, callback: types.FunctionType) -> None:
        """
        Subscribes the specified callback to a player dimension change after event.
        """
        ...

class PlayerInteractWithEntityAfterEventSignal(Events):
    """
    Manages callbacks that are connected to after a player interacts with an entity.
    """
    def subscribe(self, callback: types.FunctionType) -> None:
        """
        Adds a callback that will be called after a player interacts with an entity.
        """
        ...

class PlayerInventoryItemChangeAfterEventSignal(Events):
    """
    Manages callbacks that are connected after a player's inventory item is changed.
    """
    def subscribe(self, callback: types.FunctionType) -> None:
        """
        Adds a callback that will be called after a player's inventory item is changed.
        """
        ...

class PlayerSpawnAfterEventSignal(Events):
    """
    Registers an event when a player is spawned (or re-spawned after death) and fully ready within the world.
    """
    def subscribe(self, callback: types.FunctionType) -> None:
        """
        Registers a new event receiver for this particular type of event.
        """
        ...

class PlayerJoinAfterEventSignal(Events):
    """
    Manages callbacks that are connected to a player joining the world.
    """
    def subscribe(self, callback: types.FunctionType) -> None:
        """
        Adds a callback that will be called when a player joins the world.
        """
        ...

class PlayerLeaveAfterEventSignal(Events):
    """
    Manages callbacks that are connected to a player leaving the world.
    """
    def subscribe(self, callback: types.FunctionType) -> None:
        """
        Adds a callback that will be called when a player leaves the world.
        """
        ...

class ChatSendBeforeEventSignal(Events):
    """
    Manages callbacks that are connected to an event that fires before chat messages are sent.
    """
    def subscribe(self, callback: types.FunctionType) -> None:
        """
        Adds a callback that will be called before new chat messages are sent.
        """
        ...

class PlayerInteractWithEntityBeforeEventSignal(Events):
    """
    Manages callbacks that are connected to after a player interacts with an entity.
    """
    def subscribe(self, callback: types.FunctionType) -> None:
        """
        Adds a callback that will be called after a player interacts with an entity.
        """
        ...