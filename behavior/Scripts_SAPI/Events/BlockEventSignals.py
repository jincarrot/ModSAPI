# coding=utf-8

from EventBases import *
import mod.server.extraServerApi as serverApi
from ..decorators import *

class BlockEvents(Events):
    def __init__(self):
        Events.__init__(self)
        self.__eventName = ""
    
    def _check(self, obj, data, valueName):
        # type: (EventListener, dict, tuple) -> bool
        options = obj.options
        if type(options) == dict:
            options = BlockEventOptions(options)
        elif type(options) == BlockEventOptions:
            options = options
        else:
            options = None
        if options:
            location = valueName[1]
            if type(location) == tuple:
                location = (data[location[0]], data[location[1]], data[location[2]])
            else:
                location = data[location]
            if options.blockTypes:
                if Block({"dimansion": Dimension(data[valueName[0]]), "location": Vector3(location)}).typeId not in options.blockTypes:
                    return False
            if options.permutations:
                block = Block({"dimension": Dimension(data[valueName[0]]), "location": Vector3(location)})
                if block.permutation not in options.permutations:
                    return False
        return True

    def subscribe(self, callback, options=None):
        # type: (types.FunctionType, dict) -> None
        pass


class BlockExplodeAfterEventSignal(BlockEvents):
    """
    Manages callbacks that are connected to when an explosion occurs, as it impacts individual blocks.
    """

    def __init__(self):
        BlockEvents.__init__(self)
        self.__eventName = "ExplosionServerEvent"

    def subscribe(self, callback, options=None):
        # type: (types.FunctionType, dict) -> None
        """
        Adds a callback that will be called when an explosion occurs, as it impacts individual blocks.
        """
        import BlockEvents as be
        self._events[id(callback)] = EventListener(self.__eventName, callback, options, self._check, ('dimensionId', 'explodePos'), be.BlockExplodeAfterEvent)

class PlayerBreakBlockAfterEventSignal(BlockEvents):
    """
    Manages callbacks that are connected to when a player breaks a block.
    """

    def __init__(self):
        BlockEvents.__init__(self)
        self.__eventName = "ServerPlayerTryDestroyBlockEvent"

    def subscribe(self, callback, options=None):
        # type: (types.FunctionType, dict) -> None
        """
        Adds a callback that will be called when a block is broken by a player.
        """
        import BlockEvents as be
        self._events[id(callback)] = EventListener(self.__eventName, callback, options, self._check, ('dimensionId', ('x', 'y', 'z')), be.PlayerBreakBlockAfterEvent)

    def unsubscribe(self, callback):
        Events.unsubscribe(self, callback)

class PlayerPlaceBlockAfterEventSignal(BlockEvents):
    """
    Manages callbacks that are connected to when a block is placed by a player.
    """

    def __init__(self):
        BlockEvents.__init__(self)
        self.__eventName = "EntityPlaceBlockAfterServerEvent"
    
    def _check(self, obj, data, valueName):
        # type: (EventListener, dict, tuple) -> bool
        if createEntity(data['entityId']).typeId != "minecraft:player":
            return False
        options = obj.options
        if type(options) == dict:
            options = BlockEventOptions(options)
        elif type(options) == BlockEventOptions:
            options = options
        else:
            options = None
        if options:
            location = valueName[1]
            if type(location) == tuple:
                location = (data[location[0]], data[location[1]], data[location[2]])
            else:
                location = data[location]
            if options.blockTypes:
                if Block({"dimansion": Dimension(data[valueName[0]]), "location": Vector3(location)}).typeId not in options.blockTypes:
                    return False
            if options.permutations:
                block = Block({"dimension": Dimension(data[valueName[0]]), "location": Vector3(location)})
                if block.permutation not in options.permutations:
                    return False
        return True

    def subscribe(self, callback, options=None):
        # type: (types.FunctionType, dict) -> None
        """
        Adds a callback that will be called when a block is placed by a player.
        """
        import BlockEvents as be
        self._events[id(callback)] = EventListener(self.__eventName, callback, options, self._check, ('dimensionId', ('x', 'y', 'z')), be.PlayerBreakBlockAfterEvent)


class PlayerBreakBlockBeforeEventSignal(Events):
    """
    Manages callbacks that are connected to when a player breaks a block.
    """

    def __init__(self):
        Events.__init__(self)
        self.__eventName = "ServerPlayerTryDestroyBlockEvent"

    def subscribe(self, callback, options=None):
        # type: (types.FunctionType, dict) -> None
        """
        Adds a callback that will be called when a block is broken by a player.
        """
        import BlockEvents as be
        self._events[id(callback)] = EventListener(self.__eventName, callback, options, self._check, ('dimensionId', ('x', 'y', 'z')), be.PlayerPlaceBlockBeforeEvent)

    def unsubscribe(self, callback):
        Events.unsubscribe(self, callback)
