# coding=utf-8
from ..Classes.Entity import *
eventData = {
    "playerInteractWithEntity": {},
    "playerSpawn": {}
}

class InteractEvent(object):

    def __init__(self, data):
        global eventData
        eventData['playerInteractWithEntity'][(data['playerId'], data['victimId'])] = data['itemDict']

class PlayerSpawnEvent(object):

    def __init__(self, data):
        global eventData
        eventData['playerSpawn'][data['playerId']] = True

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
        # type: () -> list[Player]
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
        self.__itemStack = createItemStack(itemData)
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
    
class ItemStartUseOnAfterEvent(object):
    """
    Contains information related to an item being used on a block. 
    This event fires when a player presses the the Use Item / Place Block button to successfully use an item or place a block. 
    Fires for the first block that is interacted with when performing a build action. 
    
    Note: This event cannot be used with Hoe or Axe items.
    """

    def __init__(self, data):
        itemData = data['itemDict']
        self.__itemStack = createItemStack(itemData)
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
        self.__itemStack = createItemStack(itemData)
        self.__source = Player(data['playerId'])
        self.__useDuration = 0

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
    
class PlayerDimensionChangeAfterEvent(object):
    """
    Contains information related to a chargeable item completing being charged.
    """

    def __init__(self, data):
        self.__fromDimension = Dimension(data['fromDimensionId'])
        self.__fromLocation = Vector3((data['fromX'], data['fromY'], data['fromZ']))
        self.__toDimension = Dimension(data['toDimensionId'])
        y = SComp.CreateBlockInfo(serverApi.GetLevelId()).GetTopBlockHeight((data['toX'], data['toZ'])) or self.__fromLocation.y
        self.__toLocation = Vector3((data['toX'], y, data['toZ']))
        self.__player = Player(data['playerId'])

    def __str__(self):
        data = {
            "fromDimension": str(self.__fromDimension),
            "toDimension": str(self.__toDimension),
            "player": str(self.__player)
        }
        return "<PlayerDimensionChangeAfterEvent> %s" % data

    @property
    def fromDimension(self):
        """The dimension the player is changing from."""
        return self.__fromDimension
    
    @property
    def toDimension(self):
        """The dimension that the player is changing to."""
        return self.__toDimension
    
    @property
    def fromLocation(self):
        """The location the player was at before changing dimensions."""
        return self.__fromLocation
    
    @property
    def toLocation(self):
        """The location the player will spawn to after changing dimensions."""
        return self.__toLocation
    
    @property
    def player(self):
        """Handle to the player that is changing dimensions."""
        return self.__player
    
class PlayerInteractWithEntityAfterEvent(object):
    """
    Contains information regarding an event after a player successfully interacts with an entity.
    """

    def __init__(self, data):
        global eventData
        self.__beforeItemStack = None
        if (data['playerId'], data['interactEntityId']) in eventData['playerInteractWithEntity']:
            self.__beforeItemStack = createItemStack(eventData['playerInteractWithEntity'][(data['playerId'], data['interactEntityId'])])
            del eventData['playerInteractWithEntity'][(data['playerId'], data['interactEntityId'])]
        self.__itemStack = createItemStack(data['itemDict'])
        self.__player = Player(data['playerId'])
        self.__target = createEntity(data['interactEntityId'])

    def __str__(self):
        data = {
            "player": str(self.__player),
            "target": str(self.__target)
        }
        return "<PlayerInteractWithEntityAfterEvent> %s" % data
    
    @property
    def beforeItemStack(self):
        """The ItemStack before the interaction succeeded, or undefined if hand is empty."""
        return self.__beforeItemStack
    
    @property
    def itemStack(self):
        """The ItemStack after the interaction succeeded, or undefined if hand is empty."""
        return self.__itemStack
    
    @property
    def player(self):
        """Source Player for this event."""
        return self.__player
    
    @property
    def target(self):
        """The entity that will be interacted with."""
        return self.__target

class PlayerInventoryItemChangeAfterEvent(object):
    """Contains information regarding an event after a player's inventory item changes."""

    def __init__(self, data):
        self.__player = Player(data['playerId'])
        self.__slot = data['slot']
        self.__itemStack = createItemStack(data['newItemDict'])
        self.__beforeItemStack = createItemStack(data['beforeItemStack'])
        self.__inventoryType = "Hotbar" if self.__slot < 9 else "Inventory"

    def __str__(self):
        data = {
            "player": str(self.__player)
        }
        return "<PlayerInventoryItemChangeAfterEvent> %s" % data
    
    @property
    def player(self):
        """Source Player for this event."""
        return self.__player
    
    @property
    def itemStack(self):
        """The new item stack."""
        return self.__itemStack
    
    @property
    def beforeItemStack(self):
        """The previous item stack."""
        return self.__beforeItemStack
    
    @property
    def slot(self):
        # type: () -> int
        """The slot index with the change."""
        return self.__slot
    
    @property
    def inventoryType(self):
        """Inventory type."""
        return self.__inventoryType
    
class PlayerBreakBlockAfterEvent(object):
    """Contains information regarding a player that has left the world.    """

    def __init__(self, data):
        self.__playerId = data['id']
        self.__playerName = data['name']

    def __str__(self):
        data = {
            "playerId": str(self.__playerId),
            "playerName": str(self.__playerName)
        }
        return "<PlayerBreakBlockAfterEvent> %s" % data
    
    @property
    def playerId(self):
        # type: () -> str
        """Opaque string identifier of the player that left the game."""
        return self.__playerId
    
    @property
    def playerName(self):
        # type: () -> str
        """Name of the player that has left."""
        return self.__playerName

class PlayerSpawnAfterEvent(object):
    """
    Contains information regarding a player that has joined. 
    
    See the playerSpawn event for more detailed information that could be returned after the first time a player has spawned within the game.
    """

    def __init__(self, data):
        global eventData
        self.__player = Player(data['playerId'])
        self.__initialSpawn = False
        if data['playerId'] in eventData['playerSpawn']:
            self.__initialSpawn = True
            del eventData['playerSpawn'][data['playerId']]

    def __str__(self):
        data = {
            "player": str(self.__player)
        }
        return "<PlayerSpawnAfterEvent> %s" % data
    
    @property
    def player(self):
        """Object that represents the player that joined the game."""
        return self.__player
    
    @property
    def initialSpawn(self):
        # type: () -> bool
        """If true, this is the initial spawn of a player after joining the game."""
        return self.__initialSpawn
    
class PlayerJoinAfterEvent(object):
    """
    Contains information regarding a player that has joined. 
    
    See the playerSpawn event for more detailed information that could be returned after the first time a player has spawned within the game.
    """

    def __init__(self, data):
        self.__playerId = data['id']
        self.__playerName = data['name']

    def __str__(self):
        data = {
            "playerId": str(self.__playerId),
            "playerName": str(self.__playerName)
        }
        return "<PlayerJoinAfterEvent> %s" % data
    
    @property
    def playerId(self):
        # type: () -> str
        """Opaque string identifier of the player that joined the game."""
        return self.__playerId
    
    @property
    def playerName(self):
        # type: () -> str
        """Name of the player that has joined."""
        return self.__playerName

class PlayerLeaveAfterEvent(object):
    """Contains information regarding a player that has left the world.    """

    def __init__(self, data):
        self.__playerId = data['id']
        self.__playerName = data['name']

    def __str__(self):
        data = {
            "playerId": str(self.__playerId),
            "playerName": str(self.__playerName)
        }
        return "<PlayerLeaveAfterEvent> %s" % data
    
    @property
    def playerId(self):
        # type: () -> str
        """Opaque string identifier of the player that left the game."""
        return self.__playerId
    
    @property
    def playerName(self):
        # type: () -> str
        """Name of the player that has left."""
        return self.__playerName


class ChatSendBeforeEvent(object):
    """
    An event that fires as players enter chat messages.
    """

    def __init__(self, data):
        self.__data = data
        self.__cancel = False
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
        return "<ChatSendBeforeEvent> %s" % data

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
        # type: () -> list[Player]
        """
        Optional list of players that will receive this message. 
        If defined, this message is directly targeted to one or more players (i.e., is not broadcast.)
        """
        return self.__targets
    
    @property
    def cancel(self):
        # type: () -> bool
        """
        If set to true in a beforeChat event handler, this message is not broadcast out.
        """
        return self.__cancel
    
    @cancel.setter
    def cancel(self, value):
        # type: (bool) -> None
        self.__cancel = value
        self.__data['cancel'] = value

class PlayerInteractWithEntityBeforeEvent(object):
    """
    Contains information regarding an event before a player successfully interacts with an entity.
    """

    def __init__(self, data):
        self.__data = data
        self.__itemStack = createItemStack(data['itemDict'])
        self.__player = Player(data['playerId'])
        self.__target = createEntity(data['interactEntityId'])
        self.__cancel = False

    def __str__(self):
        data = {
            "player": str(self.__player),
            "target": str(self.__target)
        }
        return "<PlayerInteractWithEntityAfterEvent> %s" % data
    
    @property
    def itemStack(self):
        """The ItemStack before the interaction succeeded, or undefined if hand is empty."""
        return self.__itemStack
    
    @property
    def player(self):
        """Source Player for this event."""
        return self.__player
    
    @property
    def target(self):
        """The entity that will be interacted with."""
        return self.__target
    
    @property
    def cancel(self):
        """cancel this event"""
        return self.__cancel
    
    @cancel.setter
    def cancel(self, value):
        # type: (bool) -> None
        self.__cancel = value
        self.__data['cancel'] = value
