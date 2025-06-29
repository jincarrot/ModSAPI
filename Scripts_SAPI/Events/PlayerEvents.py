# coding=utf-8
from ..Classes.Entity import *


class ChatSendAfterEvent(object):
    """
    An event that fires as players enter chat messages.
    """

    def __init__(self, data):
        self.__message = data['message']
        self.__sender = Player(data['playerId']) if data['playerId'] else None
        targetIds = data['toPlayerIds']
        self.__targets = []
        for id in targetIds:
            self.__targets.append(Player(id))

    def __str__(self):
        data = {
            "message": self.__message,
            "sender": str(self.__sender)
        }
        return "<ChatSendAfterEvent> %s" % data

    @property
    def message(self):
        # type: () -> str
        """
        Message that is being broadcast.
        """
        return self.__damageSource
    
    @property
    def sender(self):
        # type: () -> Player
        """
        Player that sent the chat message.
        """
        return self.__sender
    
    @property
    def targets(self):
        # type: () -> List[Player]
        """
        Optional list of players that will receive this message. 
        If defined, this message is directly targeted to one or more players (i.e., is not broadcast.)
        """
        return self.__targets


class ItemUseAfterEvent(object):
    """
    Contains information related to an item being used on a block. 
    This event fires when an item used by a player successfully triggers an entity interaction.
    """

    def __init__(self, data):
        itemData = data['itemDict']
        self.__itemStack = ItemStack(itemData['newItemName'], itemData['count'])
        self.__source = Player(data['entityId'])

    @property
    def itemStack(self):
        # type: () -> ItemStack
        return self.__itemStack
    
    @property
    def source(self):
        # type: () -> Player
        return self.__source