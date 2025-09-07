# coding=utf-8

from EventBases import *
import mod.server.extraServerApi as serverApi
from ..decorators import *


class BlockExplodeAfterEventSignal(Events):
    """
    Manages callbacks that are connected to when an explosion occurs, as it impacts individual blocks.
    """

    def __init__(self):
        Events.__init__(self)
        self.__eventName = "ExplosionServerEvent"

    def subscribe(self, callback):
        # type: (types.FunctionType) -> None
        """
        Adds a callback that will be called when an explosion occurs, as it impacts individual blocks.
        """
        import BlockEvents as be
        EventListener(self.__eventName, callback, None, None, None, be.BlockExplodeAfterEvent)

    def unsubscribe(self, callback):
        pass

class PlayerBreakBlockAfterEventSignal(Events):
    """
    Manages callbacks that are connected to when a player breaks a block.
    """

    def __init__(self):
        Events.__init__(self)
        self.__eventName = "ServerPlayerTryDestroyBlockEvent"

    def subscribe(self, callback):
        # type: (types.FunctionType) -> None
        """
        Adds a callback that will be called when a block is broken by a player.
        """
        import BlockEvents as be
        EventListener(self.__eventName, callback, None, None, None, be.PlayerBreakBlockAfterEvent)

    def unsubscribe(self, callback):
        Events.unsubscribe(self, callback)


class BlockExplodeBeforeEventSignal(Events):
    """
    Manages callbacks that are connected to when an explosion occurs, as it impacts individual blocks.
    """

    def __init__(self):
        self.__eventName = "ExplosionServerEvent"

    def subscribe(self, callback):
        # type: (types.FunctionType) -> None
        """
        Adds a callback that will be called when an explosion occurs, as it impacts individual blocks.
        """
        import BlockEvents as be
        EventListener(self.__eventName, callback, None, None, None, be.BlockExplodeBeforeEvent)

    def unsubscribe(self, callback):
        pass
