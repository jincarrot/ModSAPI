from Entity import Entity
from core_behavior.ModSAPI.modules.client.Screen import *
from ..client.Camara import *
from ..client.ClientSystemInfo import *
from ...utils.system import *
from ..client.Audio import *
from ItemStack import *
import mod.server.extraServerApi as serverApi
from Container import Container
from MolangVariableMap import MolangVariableMap

class Player(Entity):
    """
    Represents a player within the world.
    """
    
    @property
    def name(self):
        """
        Name of the player.
        """
    
    @property
    def isFlying(self):
        # type: () -> bool
        """Whether the player is flying. For example, in Creative or Spectator mode."""
    
    @property
    def level(self):
        # type: () -> int
        """The current overall level for the player, based on their experience."""

    @property
    def selectedSlotIndex(self):
        """the index of selected slot"""
    
    @selectedSlotIndex.setter
    def selectedSlotIndex(self, slotId):
        # type: (int) -> None
        pass

    @property
    def container(self):
        # type: () -> Container
        """returns the container of player's inventory"""

    @property
    def mainHand(self):
        # type: () -> ItemStack
        """get the item of main hand"""
    
    @mainHand.setter
    def mainHand(self, item):
        # type: (ItemStack) -> None
        pass
    
    def applyKnockback(self, horizontalForce, verticalStrength):
        # type: (dict | VectorXZ, float) -> None
        """
        Applies impulse vector to the current velocity of the entity.
        """

    def sendMessage(self, message):
        # type: (str) -> None
        """Sends a message to the player."""

    def getSpawnPoint(self):
        # type: () -> Vector3
        """Gets the current spawn point of the player."""

    def sendToast(self, message, title=""):
        # type: (str, str) -> None
        """
        send a toast to player
        """

    def spawnParticle(self, effectName: str, location: Vector3, molangVariables: MolangVariableMap = None):
        """Creates a new particle emitter at a specified location in the world."""

