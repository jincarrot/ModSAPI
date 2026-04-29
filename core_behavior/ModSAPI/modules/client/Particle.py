# -*- coding: utf-8 -*-
import mod.client.extraClientApi as clientApi
from ...interfaces.EntityOptions import *
from ...interfaces.Vector import *
from ...interfaces.ParticleOptions import *

CComp = clientApi.GetEngineCompFactory()
particleComp = CComp.CreateParticleSystem(clientApi.GetLevelId())

class Particle:
    "Contains a set of operations about particle effects"

    def __init__(self, parId):
        self.__id = parId

    @property
    def id(self):
        """Runtime identifier of this particle effect."""
        return self.__id
    
    @property
    def location(self):
        """Location of this particle effect."""
        pos = particleComp.GetPos(self.__id)
        return Vector3({"x": pos[0], "y": pos[1], "z": pos[2]})
    
    @property
    def isValid(self):
        """Whether this particle effect is valid."""
        return particleComp.Exist(self.__id)
    
    @property
    def isBinding(self):
        """Whether this particle effect is currently binding to an entity."""
        return particleComp.GetBindingID(self.__id) != "0"
    
    def bindToEntity(self, entity, options={}):
        """Bind this particle effect to an entity. The particle effect will move together with the entity."""
        return particleComp.BindEntity(
            self.__id, 
            entity.id, 
            options.get("bone", "body"), 
            options.get("offset", Vector3((0, 0, 0))).getTuple(), 
            options.get("rotate", Vector3()).getTuple()
        )
    
    def getMolang(self, molangExpression):
        """Get value of molang."""
        return particleComp.GetVariable(self.__id, molangExpression)
    
    def setMolang(self, molang, value):
        """Set value of molang."""
        particleComp.SetVariable(self.__id, molang, value)

    def remove(self):
        """Remove this particle effect."""
        particleComp.Remove(self.__id)
