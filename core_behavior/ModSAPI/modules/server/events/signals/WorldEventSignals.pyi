# -*- coding: utf-8 -*-
# stub file for world events module

from typing import Any, Callable, Dict, Optional
import types
from ..EventBases import Events

class ExplosionAfterEventSignal(Events):
    """
    Manages callbacks that are connected to when an explosion occurs.
    """
    def subscribe(self, callback: types.FunctionType) -> None:
        """
        Adds a callback that will be called when an explosion occurs.
        """
        ...

class ScriptEventCommandMessageAfterEventSignal(Events):
    """
    Allows for registering an event handler that responds to inbound /scriptevent commands.
    """
    def subscribe(
        self, callback: types.FunctionType, options: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Registers a new ScriptEvent handler.
        """
        ...

class ClientEventReceiveAfterEventSignal(Events):
    """
    Allows for registering an event handler that responds to inbound /scriptevent commands.
    """

    def subscribe(self, eventName, callback, options={}):
        # type: (str, types.FunctionType, dict) -> None
        """
        Registers a new ScriptEvent handler.
        """

class ExplosionBeforeEventSignal(Events):
    """
    Manages callbacks that are connected to when an explosion occurs, as it impacts individual blocks.
    """
    def subscribe(self, callback: types.FunctionType) -> None:
        """
        Adds a callback that will be called when an explosion occurs, as it impacts individual blocks.
        """
        ...