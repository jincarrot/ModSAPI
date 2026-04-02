# -*- coding: utf-8 -*-
from typing import Any, Callable, Dict, Optional, Tuple, Union
from ..EventBases import Events
from ..core.BlockEvents import BlockEventOptions
import types

class BlockEvents(Events):
    def subscribe(self, callback: types.FunctionType, options: Optional[Union[Dict[str, Any], BlockEventOptions]] = None) -> None: ...

class BlockExplodeAfterEventSignal(BlockEvents):
    """
    Manages callbacks that are connected to when an explosion occurs, as it impacts individual blocks.
    """
    def subscribe(self, callback: types.FunctionType, options: Optional[Union[Dict[str, Any], BlockEventOptions]] = None) -> None:
        """
        Adds a callback that will be called when an explosion occurs, as it impacts individual blocks.
        """
        ...

class PlayerBreakBlockAfterEventSignal(BlockEvents):
    """
    Manages callbacks that are connected to when a player breaks a block.
    """
    def subscribe(self, callback: types.FunctionType, options: Optional[Union[Dict[str, Any], BlockEventOptions]] = None) -> None:
        """
        Adds a callback that will be called when a block is broken by a player.
        """
        ...
    def unsubscribe(self, callback: Callable) -> None: ...

class PlayerPlaceBlockAfterEventSignal(BlockEvents):
    """
    Manages callbacks that are connected to when a block is placed by a player.
    """
    def subscribe(self, callback: types.FunctionType, options: Optional[Union[Dict[str, Any], BlockEventOptions]] = None) -> None:
        """
        Adds a callback that will be called when a block is placed by a player.
        """
        ...

class PlayerBreakBlockBeforeEventSignal(Events):
    """
    Manages callbacks that are connected to when a player breaks a block.
    """
    def subscribe(self, callback: types.FunctionType, options: Optional[Union[Dict[str, Any], BlockEventOptions]] = None) -> None:
        """
        Adds a callback that will be called when a block is broken by a player.
        """
        ...
    def unsubscribe(self, callback: Callable) -> None: ...