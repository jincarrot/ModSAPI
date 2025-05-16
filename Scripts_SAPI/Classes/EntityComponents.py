# -*- coding: utf-8 -*-
from typing import Union, Dict
from Components import *

class EntityAddRiderComponent(EntityComponent):
    """
    When added, this component makes the entity spawn with a rider of the specified entityType.
    """
    
    def __init__(self, typeId, data):
        super().__init__(typeId, data)
        self.__entityType = data['entityType']
        self.__spawnEvent = data['spawnEvent']
    
    def __str__(self):
        data = {
            "typeId": self.typeId,
            "entity": str(self.entity),
            "entityType": self.entityType,
            "spawnEvent": self.spawnEvent
        }
        return "<EntityComponent> %s" % data
    
    @property
    def entityType(self):
        # type: () -> str
        """
        The entity that owns this component. 
        The entity will be undefined if it has been removed.
        """
        return self.__entityType
    
    @property
    def spawnEvent(self):
        # type: () -> str
        """
        Optional spawn event to trigger on the rider when that rider is spawned for this entity.
        """
        return self.__spawnEvent
