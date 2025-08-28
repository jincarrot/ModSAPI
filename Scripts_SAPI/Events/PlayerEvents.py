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
        return self.__message
    
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

    def __str__(self):
        data = {
            "itemStack": str(self.__itemStack),
            "source": str(self.__source)
        }
        return "<ItemUseAfterEvent> %s" % data

    @property
    def itemStack(self):
        # type: () -> ItemStack
        """
        The impacted item stack that is being used.
        """
        return self.__itemStack
    
    @property
    def source(self):
        # type: () -> Player
        """
        Returns the source entity that triggered this item event.
        """
        return self.__source
    
class ItemCompleteUseAfterEvent(object):
    """
    Contains information related to a chargeable item completing being charged.
    """

    def __init__(self, data):
        itemData = data['itemDict']
        self.__itemStack = ItemStack(itemData['newItemName'], itemData['count'])
        self.__source = Player(data['playerId'])
        self.__useDuration = data['durationLeft']

    def __str__(self):
        data = {
            "itemStack": str(self.__itemStack),
            "source": str(self.__source)
        }
        return "<ItemCompleteUseAfterEvent> %s" % data

    @property
    def itemStack(self):
        # type: () -> ItemStack
        """
        Returns the item stack that has completed charging.
        """
        return self.__itemStack
    
    @property
    def source(self):
        # type: () -> Player
        """
        Returns the source entity that triggered this item event.
        """
        return self.__source
    
    @property
    def useDuration(self):
        # type: () -> float
        """
        Returns the time, in ticks, for the remaining duration left before the charge completes its cycle.
        """
        return self.__useDuration