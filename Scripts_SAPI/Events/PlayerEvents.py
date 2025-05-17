# coding=utf-8
from ..Classes.Entity import *


class ChatSendAfterEvent(object):
    """
    An event that fires as players enter chat messages.
    """

    def __init__(self, data):
        self.__message = data['message']
        self.__sender = data['sender']
        self.targets = data['targets']

    def __str__(self):
        data = {
            "message": self.__message,
        }
        return "<EntityDieAfterEvent> %s" % data

    @property
    def message(self):
        # type: () -> str
        """
        Message that is being broadcast.
        """
        return self.__damageSource

    @property
    def deadEntity(self):
        # type: () -> Entity
        """
        Now-dead entity object.
        """
        return self.__deadEntity
