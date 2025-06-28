# coding=utf-8

from EventBases import *
import mod.server.extraServerApi as serverApi


class ChatSendAfterEventSignal(Events):
    """
    Manages callbacks that are connected to chat messages being sent.
    """

    def __detectFunction(self):
        return True

    def subscribe(self, callback, options=None):
        # type: (types.FunctionType, None) -> None
        """
        Adds a callback that will be called when new chat messages are sent.
        """
        if type(options).__name__ != "dict":
            options = None
        eventName = "ServerChatEvent"
        listener = EventListener(eventName, callback, options, self.__detectFunction)
        world.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), eventName, listener, listener.listen)