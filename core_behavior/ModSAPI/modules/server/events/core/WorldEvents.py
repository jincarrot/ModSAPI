# coding=utf-8
from ...Entity import *
from ...Player import *
from .....interfaces.Sources import *
from .....enums.Events import ScriptEventSource
from ...Block import Block
from ...Dimension import Dimension

class ExplosionAfterEvent(object):
    """
    Contains information regarding an explosion that has happened.
    """

    def __init__(self, data):
        self.__source = createEntity(data['sourceId']) if data['sourceId'] else None
        self.__dimension = Dimension(data['dimensionId'])
        self.__data = data

    def __str__(self):
        data = {
            "source": self.__source
        }
        return "<ExplosionAfterEvent> %s" % data
    
    @property
    def source(self):
        # type: () -> Entity
        """
        Optional source of the explosion.
        """
        return self.__source
    
    @property
    def dimension(self):
        # type: () -> Dimension
        """Dimension where the explosion has occurred."""
        return self.__dimension
    
    def getImpactedBlocks(self):
        # type: () -> list[Block]
        """A collection of blocks impacted by this explosion event."""
        lst = []
        for block in self.__data:
            lst.append(Block({"dimension": self.__dimension, "location": Vector3(block)}))
        return lst

class ScriptEventCommandMessageAfterEvent(object):
    """
    Returns additional data about a /scriptevent command invocation.
    """

    def __init__(self, data):
        self.__id = data['args'][0]['value'] # type: str
        self.__message = data['args'][1]['value'] # type: str
        self.__sourceData = data['origin'] # type: dict
        self.__source = None
        self.__sourceType = ScriptEventSource.Server
        if self.__sourceData.get('entityId', None):
            self.__source = createEntity(self.__sourceData['entityId'])
            self.__sourceType = ScriptEventSource.Entity
            if self.__source.typeId == 'minecraft:npc':
                self.__sourceType = ScriptEventSource.NPCDialogue
        else:
            self.__source = Block({"dimension": Dimension(self.__sourceData['dimension']), "location": Vector3(self.__sourceData['blockPos'])})
            self.__sourceType = ScriptEventSource.Block

    def __str__(self):
        data = {
            "id": self.__id,
            "message": self.__message
        }
        return "<ScriptEventCommandMessageAfterEvent> %s" % data
    
    @property
    def id(self):
        # type: () -> str
        """Identifier of this ScriptEvent command message."""
        return self.__id
    
    @property
    def message(self):
        # type: () -> str
        """Optional additional data passed in with the script event command."""
        return self.__message
    
    @property
    def initiator(self):
        """If this command was initiated via an NPC, returns the entity that initiated the NPC dialogue."""
        return self.__source if self.__sourceType == ScriptEventSource.NPCDialogue else None
    
    @property
    def sourceEntity(self):
        """Source entity if this command was triggered by an entity (e.g., a NPC)."""
        return self.__source if self.__sourceType == ScriptEventSource.Entity else None
    
    @property
    def sourceBlock(self):
        """Source block if this command was triggered via a block (e.g., a commandblock.)"""
        return self.__source if self.__sourceType == ScriptEventSource.Block else None
    
    @property
    def sourceType(self):
        """Returns the type of source that fired this command."""
        return self.__sourceType
    

class ExplosionBeforeEvent(object):
    """
    Contains information regarding an explosion that has happened.
    """

    def __init__(self, data):
        self.__source = createEntity(data['sourceId']) if data['sourceId'] else None
        self.__dimension = Dimension(data['dimensionId'])
        self.__data = data

    def __str__(self):
        data = {
            "source": self.__source
        }
        return "<ExplosionBeforeEvent> %s" % data
    
    @property
    def source(self):
        # type: () -> Entity
        """
        Optional source of the explosion.
        """
        return self.__source
    
    @property
    def dimension(self):
        # type: () -> Dimension
        """Dimension where the explosion has occurred."""
        return self.__dimension
    
    def getImpactedBlocks(self):
        # type: () -> list[Block]
        """A collection of blocks impacted by this explosion event."""
        lst = []
        for block in self.__data:
            lst.append(Block({"dimension": self.__dimension, "location": Vector3(block)}))
        return lst

    