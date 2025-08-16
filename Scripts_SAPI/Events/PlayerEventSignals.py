# coding=utf-8

from EventBases import *
import mod.server.extraServerApi as serverApi


class ChatSendAfterEventSignal(Events):
    """
    Manages callbacks that are connected to chat messages being sent.
    """

    def __init__(self):
        self.__eventName = "ServerChatEvent"

    def subscribe(self, callback):
        # type: (types.FunctionType) -> None
        """
        Adds a callback that will be called when new chat messages are sent.
        """
        import PlayerEvents as pe
        EventListener(self.__eventName, callback, None, None, None, pe.ChatSendAfterEvent)


class ItemUseAfterEventSignal(Events):
    """
    Manages callbacks that are connected to an item use event.
    """

    def __init__(self):
        self.__eventName = "ItemUseAfterServerEvent"

    def subscribe(self, callback):
        # type: (types.FunctionType) -> None
        """
        Adds a callback that will be called when an item is used.
        """
        import PlayerEvents as pe
        EventListener(self.__eventName, callback, None, None, None, pe.ItemUseAfterEvent)


class ItemCompleteUseAfterEventSignal(Events):
    """
    Manages callbacks that are connected to the completion of charging for a chargeable item.
    """

    def __init__(self):
        self.__eventName = "ItemReleaseUsingServerEvent"

    def subscribe(self, callback):
        # type: (types.FunctionType) -> None
        """
        Adds a callback that will be called when a chargeable item completes charging.
        """
        import PlayerEvents as pe
        EventListener(self.__eventName, callback, None, None, None, pe.ItemCompleteUseAfterEvent)