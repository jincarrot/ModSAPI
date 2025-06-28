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
        # type: (types.FunctionType, None) -> None
        """
        Adds a callback that will be called when new chat messages are sent.
        """
        import PlayerEvents as pe
        EventListener(self.__eventName, callback, None, None, None, pe.ChatSendAfterEvent)
