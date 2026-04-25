from Entity import *
from Screen import *
from ..client.Camara import *
from ..client.ClientSystemInfo import *
from ...utils.system import *
from ..client.Audio import *
from ItemStack import *
import mod.server.extraServerApi as serverApi

class Player(Entity):
    """
    Represents a player within the world.
    """
    import Container as con

    def __init__(self, playerId):
        # type: (str) -> None
        Entity.__init__(self, playerId)
        self.__id = playerId
        self.__container = self.con.Container(None, self.__id)
        self.__screen = Screen(self.__id)

    def __str__(self):
        data = {
            "id": self.id,
            "dimension": str(self.dimension),
            "name": self.name
        }
        return "<Player> %s" % data
    
    @property
    def name(self):
        """
        Name of the player.
        """
        return self.nameTag

    @property
    def camera(self):
        # type: () -> Camera
        """
        The player's Camera.

        No use now.
        """
        return Camera(self.__id)
    
    @property
    def isFlying(self):
        # type: () -> bool
        """Whether the player is flying. For example, in Creative or Spectator mode."""
        return SComp.CreateFly(self.__id).IsPlayerFlying()
    
    @property
    def level(self):
        # type: () -> int
        """The current overall level for the player, based on their experience."""
        return SComp.CreateLv(self.__id).GetPlayerLevel()

    @property
    def selectedSlotIndex(self):
        """the index of selected slot"""
        return SComp.CreateItem(self.__id).GetSelectSlotId()
    
    @selectedSlotIndex.setter
    def selectedSlotIndex(self, slotId):
        # type: (int) -> None
        SComp.CreatePlayer(self.__id).ChangeSelectSlot(slotId)

    @property
    def client(self):
        pass
    
    @property
    def clientSystemInfo(self):
        # type: () -> ClientSystemInfo
        """
        Contains the player's device information.
        """
        # requestId = request.create(self.__id, "clientSystemInfo")
        # value = request.getValue(requestId)
        # return ClientSystemInfo(value)

    @property
    def container(self):
        # type: () -> con.Container
        """returns the container of player's inventory"""
        return self.__container

    @property
    def mainHand(self):
        # type: () -> ItemStack
        """get the item of main hand"""
        return self.container.getItem(self.selectedSlotIndex)
    
    @mainHand.setter
    def mainHand(self, item):
        # type: (ItemStack) -> None
        self.container.setItem(self.selectedSlotIndex, item)
    
    def applyKnockback(self, horizontalForce, verticalStrength):
        # type: (dict | VectorXZ, float) -> None
        """
        Applies impulse vector to the current velocity of the entity.
        """
        vector = VectorXZ(horizontalForce) if type(horizontalForce).__name__ == 'dict' else horizontalForce
        SComp.CreateActorMotion(self.__id).SetPlayerMotion((vector.x, verticalStrength, vector.z))

    def playSound(self, soundID, soundOptions=PlayerSoundOptions):
        # type: (str, dict) -> None
        if soundOptions == PlayerSoundOptions:
            soundOptions = {}
        if 'location' not in soundOptions:
            pos = SComp.CreatePos(self.__id).GetPos()
            soundOptions['location'] = Vector3({"x": pos[0], "y": pos[1], "z": pos[2]})
        options = PlayerSoundOptions(soundOptions) if type(soundOptions) == dict else soundOptions
        SComp.CreateCommand(serverApi.GetLevelId()).SetCommand("playsound %s @s %s %s %s %s %s" % (soundID, options.location.x, options.location.y, options.location.z, options.volume, options.pitch), self.__id)

    def sendMessage(self, message):
        # type: (str) -> None
        """Sends a message to the player."""
        SComp.CreateMsg(self.__id).NotifyOneMessage(self.__id, message)

    def getSpawnPoint(self):
        # type: () -> Vector3
        """Gets the current spawn point of the player."""
        return Vector3(SComp.CreatePlayer(self.__id).GetPlayerRespawnPos())

    def sendToast(self, message, title=""):
        # type: (str, str) -> None
        """
        send a toast to player
        """
        world = systems.world
        data = {
            "title": title,
            "message": message
        }
        world.NotifyToClient(self.__id, "sendToast", data)

    def showUI(self, customUI):
        # world = systems.world
        # Screens[id(customUI)] = customUI
        # world.NotifyToClient(self.id, "showUI", {"screenId": id(customUI)})
        pass

    def popScreen(self):
        # world.NotifyToClient(self.id, "popScreen", {})
        pass

