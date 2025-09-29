# coding=utf-8

from EventBases import *
import mod.server.extraServerApi as serverApi
from ..decorators import *


class ChatSendAfterEventSignal(Events):
    """
    Manages callbacks that are connected to chat messages being sent.
    """

    def __init__(self):
        Events.__init__(self)
        self.__eventName = "ServerChatEvent"

    def subscribe(self, callback):
        # type: (types.FunctionType) -> None
        """
        Adds a callback that will be called when new chat messages are sent.
        """
        import PlayerEvents as pe
        self._events[id(callback)] = EventListener(self.__eventName, callback, None, None, None, pe.ChatSendAfterEvent)

class ItemUseAfterEventSignal(Events):
    """
    Manages callbacks that are connected to an item use event.
    """

    def __init__(self):
        Events.__init__(self)
        self.__eventName = "ItemUseAfterServerEvent"

    def subscribe(self, callback):
        # type: (types.FunctionType) -> None
        """
        Adds a callback that will be called when an item is used.
        """
        import PlayerEvents as pe
        self._events[id(callback)] = EventListener(self.__eventName, callback, None, None, None, pe.ItemUseAfterEvent)

class ItemStartUseOnAfterEventSignal(Events):
    """
    Manages callbacks that are connected to an item use event.
    """

    def __init__(self):
        Events.__init__(self)
        self.__eventName = "ItemUseOnAfterServerEvent"

    def subscribe(self, callback):
        # type: (types.FunctionType) -> None
        """
        Adds a callback that will be called when an item is used.
        """
        import PlayerEvents as pe
        self._events[id(callback)] = EventListener(self.__eventName, callback, None, None, None, pe.ItemStartUseOnAfterEvent)

class ItemCompleteUseAfterEventSignal(Events):
    """
    Manages callbacks that are connected to the completion of charging for a chargeable item.
    """

    def __init__(self):
        Events.__init__(self)
        self.__eventName = "ItemReleaseUsingServerEvent"

    def _check(self, obj, data, valueName):
        return data['durationLeft'] <= 0

    def subscribe(self, callback):
        # type: (types.FunctionType) -> None
        """
        Adds a callback that will be called when a chargeable item completes charging.
        """
        import PlayerEvents as pe
        self._events[id(callback)] = EventListener(self.__eventName, callback, None, self._check, None, pe.ItemCompleteUseAfterEvent)

class PlayerDimensionChangeAfterEventSignal(Events):
    """
    Manages callbacks that are connected to successful player dimension changes.
    """

    def __init__(self):
        Events.__init__(self)
        self.__eventName = "DimensionChangeServerEvent"

    def subscribe(self, callback):
        # type: (types.FunctionType) -> None
        """
        Subscribes the specified callback to a player dimension change after event.
        """
        import PlayerEvents as pe
        self._events[id(callback)] = EventListener(self.__eventName, callback, None, None, None, pe.PlayerDimensionChangeAfterEvent)

class PlayerInteractWithEntityAfterEventSignal(Events):
    """
    Manages callbacks that are connected to after a player interacts with an entity.
    """

    def __init__(self):
        Events.__init__(self)
        self.__eventName = "PlayerDoInteractServerEvent"

    def subscribe(self, callback):
        # type: (types.FunctionType) -> None
        """
        Adds a callback that will be called after a player interacts with an entity.
        """
        import PlayerEvents as pe
        EventListener("PlayerInteractServerEvent", callback, None, None, None, pe.InteractEvent)
        self._events[id(callback)] = EventListener(self.__eventName, callback, None, None, None, pe.PlayerInteractWithEntityAfterEvent)

class PlayerInventoryItemChangeAfterEventSignal(Events):
    """
    Manages callbacks that are connected after a player's inventory item is changed.
    """

    def __init__(self):
        Events.__init__(self)
        self.__eventName = "InventoryItemChangedServerEvent"

    def subscribe(self, callback):
        # type: (types.FunctionType) -> None
        """
        Adds a callback that will be called after a player's inventory item is changed.
        """
        import PlayerEvents as pe
        self._events[id(callback)] = EventListener(self.__eventName, callback, None, None, None, pe.PlayerInventoryItemChangeAfterEvent)

class PlayerSpawnAfterEventSignal(Events):
    """
    Registers an event when a player is spawned (or re-spawned after death) and fully ready within the world.
    """

    def __init__(self):
        Events.__init__(self)
        self.__eventName = "PlayerRespawnFinishServerEvent"

    def subscribe(self, callback):
        # type: (types.FunctionType) -> None
        """
        Registers a new event receiver for this particular type of event.
        """
        import PlayerEvents as pe
        EventListener("playerSpawn", callback, None, None, None, pe.PlayerSpawnEvent, "SAPI", "SAPI_C")
        self._events[id(callback)] = EventListener(self.__eventName, callback, None, None, None, pe.PlayerSpawnAfterEvent)

class PlayerJoinAfterEventSignal(Events):
    """
    Manages callbacks that are connected to a player joining the world.
    """

    def __init__(self):
        Events.__init__(self)
        self.__eventName = "PlayerJoinMessageEvent"

    def subscribe(self, callback):
        # type: (types.FunctionType) -> None
        """
        Adds a callback that will be called when a player joins the world.
        """
        import PlayerEvents as pe
        self._events[id(callback)] = EventListener(self.__eventName, callback, None, None, None, pe.PlayerJoinAfterEvent)

class PlayerLeaveAfterEventSignal(Events):
    """
    Manages callbacks that are connected to a player leaving the world.
    """

    def __init__(self):
        Events.__init__(self)
        self.__eventName = "PlayerLeftMessageServerEvent"

    def subscribe(self, callback):
        # type: (types.FunctionType) -> None
        """
        Adds a callback that will be called when a player leaves the world.
        """
        import PlayerEvents as pe
        self._events[id(callback)] = EventListener(self.__eventName, callback, None, None, None, pe.PlayerLeaveAfterEvent)


class ChatSendBeforeEventSignal(Events):
    """
    Manages callbacks that are connected to an event that fires before chat messages are sent.
    """

    def __init__(self):
        Events.__init__(self)
        self.__eventName = "ServerChatEvent"

    def subscribe(self, callback):
        # type: (types.FunctionType) -> None
        """
        Adds a callback that will be called before new chat messages are sent.
        """
        import PlayerEvents as pe
        self._events[id(callback)] = EventListener(self.__eventName, callback, None, None, None, pe.ChatSendBeforeEvent)

class PlayerInteractWithEntityBeforeEventSignal(Events):
    """
    Manages callbacks that are connected to after a player interacts with an entity.
    """

    def __init__(self):
        Events.__init__(self)
        self.__eventName = "PlayerInteractServerEvent"

    def subscribe(self, callback):
        # type: (types.FunctionType) -> None
        """
        Adds a callback that will be called after a player interacts with an entity.
        """
        import PlayerEvents as pe
        self._events[id(callback)] = EventListener(self.__eventName, callback, None, None, None, pe.PlayerInteractWithEntityBeforeEvent)
