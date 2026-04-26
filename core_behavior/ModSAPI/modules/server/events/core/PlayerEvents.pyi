# coding=utf-8
from ...Entity import *
from ...Player import *

class ChatSendAfterEvent(object):
    """
    An event that fires as players enter chat messages.
    """

    @property
    def message(self):
        # type: () -> str
        """
        Message that is being broadcast.
        """
    
    @property
    def sender(self):
        # type: () -> Player
        """
        Player that sent the chat message.
        """
    
    @property
    def targets(self):
        # type: () -> list[Player]
        """
        Optional list of players that will receive this message. 
        If defined, this message is directly targeted to one or more players (i.e., is not broadcast.)
        """

class ItemUseAfterEvent(object):
    """
    Contains information related to an item being used on a block. 
    This event fires when an item used by a player successfully triggers an entity interaction.
    """

    @property
    def itemStack(self):
        # type: () -> ItemStack
        """
        The impacted item stack that is being used.
        """
    
    @property
    def source(self):
        # type: () -> Player
        """
        Returns the source entity that triggered this item event.
        """
    
class ItemStartUseOnAfterEvent(object):
    """
    Contains information related to an item being used on a block. 
    This event fires when a player presses the the Use Item / Place Block button to successfully use an item or place a block. 
    Fires for the first block that is interacted with when performing a build action. 
    
    Note: This event cannot be used with Hoe or Axe items.
    """

    @property
    def itemStack(self):
        # type: () -> ItemStack
        """
        The impacted item stack that is being used.
        """
    
    @property
    def source(self):
        # type: () -> Player
        """
        Returns the source entity that triggered this item event.
        """
    
class ItemCompleteUseAfterEvent(object):
    """
    Contains information related to a chargeable item completing being charged.
    """

    @property
    def itemStack(self):
        # type: () -> ItemStack
        """
        Returns the item stack that has completed charging.
        """
    
    @property
    def source(self):
        # type: () -> Player
        """
        Returns the source entity that triggered this item event.
        """
    
    @property
    def useDuration(self):
        # type: () -> float
        """
        Returns the time, in ticks, for the remaining duration left before the charge completes its cycle.
        """
    
class PlayerDimensionChangeAfterEvent(object):
    """
    Contains information related to a chargeable item completing being charged.
    """

    @property
    def fromDimension(self):
        """The dimension the player is changing from."""
    
    @property
    def toDimension(self):
        """The dimension that the player is changing to."""
    
    @property
    def fromLocation(self):
        """The location the player was at before changing dimensions."""
    
    @property
    def toLocation(self):
        """The location the player will spawn to after changing dimensions."""
    
    @property
    def player(self):
        """Handle to the player that is changing dimensions."""
    
class PlayerInteractWithEntityAfterEvent(object):
    """
    Contains information regarding an event after a player successfully interacts with an entity.
    """
    
    @property
    def beforeItemStack(self):
        """The ItemStack before the interaction succeeded, or undefined if hand is empty."""
    
    @property
    def itemStack(self):
        """The ItemStack after the interaction succeeded, or undefined if hand is empty."""
    
    @property
    def player(self):
        """Source Player for this event."""
    
    @property
    def target(self):
        """The entity that will be interacted with."""

class PlayerInventoryItemChangeAfterEvent(object):
    """Contains information regarding an event after a player's inventory item changes."""
    
    @property
    def player(self):
        """Source Player for this event."""
    
    @property
    def itemStack(self):
        """The new item stack."""
    
    @property
    def beforeItemStack(self):
        """The previous item stack."""
    
    @property
    def slot(self):
        # type: () -> int
        """The slot index with the change."""
    
    @property
    def inventoryType(self):
        """Inventory type."""
    
class PlayerSpawnAfterEvent(object):
    """
    Contains information regarding a player that has joined. 
    
    See the playerSpawn event for more detailed information that could be returned after the first time a player has spawned within the game.
    """
    
    @property
    def player(self):
        """Object that represents the player that joined the game."""
    
    @property
    def initialSpawn(self):
        # type: () -> bool
        """If true, this is the initial spawn of a player after joining the game."""
    
class PlayerJoinAfterEvent(object):
    """
    Contains information regarding a player that has joined. 
    
    See the playerSpawn event for more detailed information that could be returned after the first time a player has spawned within the game.
    """
    @property
    def playerId(self):
        # type: () -> str
        """Opaque string identifier of the player that joined the game."""
    
    @property
    def playerName(self):
        # type: () -> str
        """Name of the player that has joined."""

class PlayerLeaveAfterEvent(object):
    """Contains information regarding a player that has left the world.    """
    
    @property
    def playerId(self):
        # type: () -> str
        """Opaque string identifier of the player that left the game."""
    
    @property
    def playerName(self):
        # type: () -> str
        """Name of the player that has left."""


class ChatSendBeforeEvent(object):
    """
    An event that fires as players enter chat messages.
    """

    @property
    def message(self):
        # type: () -> str
        """
        Message that is being broadcast.
        """
    
    @property
    def sender(self):
        # type: () -> Player
        """
        Player that sent the chat message.
        """
    
    @property
    def targets(self):
        # type: () -> list[Player]
        """
        Optional list of players that will receive this message. 
        If defined, this message is directly targeted to one or more players (i.e., is not broadcast.)
        """
    
    @property
    def cancel(self):
        # type: () -> bool
        """
        If set to true in a beforeChat event handler, this message is not broadcast out.
        """
    
    @cancel.setter
    def cancel(self, value):
        # type: (bool) -> None
        pass

class PlayerInteractWithEntityBeforeEvent(object):
    """
    Contains information regarding an event before a player successfully interacts with an entity.
    """
    
    @property
    def itemStack(self):
        """The ItemStack before the interaction succeeded, or undefined if hand is empty."""
    
    @property
    def player(self):
        """Source Player for this event."""
    
    @property
    def target(self):
        """The entity that will be interacted with."""
    
    @property
    def cancel(self):
        """cancel this event"""
    
    @cancel.setter
    def cancel(self, value):
        # type: (bool) -> None
        pass
