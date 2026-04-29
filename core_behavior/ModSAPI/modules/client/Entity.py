
import mod.client.extraClientApi as clientApi
from ...interfaces.Vector import Vector3
CComp = clientApi.GetEngineCompFactory()
gameComp = CComp.CreateGame(clientApi.GetLevelId())

class ClientEntity:

    def __init__(self, entityId):
        self.__id = entityId
        self.__nameComp = None
        self.__typeComp = None
        self.__queryComp = None
        self.__posComp = None

    def __str__(self):
        data = {
            "id": self.__id,
            "typeId": self.typeId
        }
        return "<ClientEntity> %s" % data

    @property
    def id(self):
        """Runtime identifier of this entity."""
        return self.__id
    
    @property
    def isValid(self):
        """Whether this entity is valid."""
        return gameComp.HasEntity(self.__id) == 1
    
    @property
    def nameTag(self):
        """Name of this entity."""
        if not self.__nameComp:
            self.__nameComp = CComp.CreateName(self.__id)
        return self.__nameComp.GetName()
    
    @property
    def location(self):
        """Location of this entity."""
        if not self.__posComp:
            self.__posComp = CComp.CreatePos(self.__id)
        pos = self.__posComp.GetFootPos()
        return Vector3({"x": pos[0], "y": pos[1], "z": pos[2]})
    
    @property
    def typeId(self):
        """Type identifier of this entity."""
        if not self.__typeComp:
            self.__typeComp = CComp.CreateEngineType(self.__id)
        return self.__typeComp.GetEngineTypeStr()
    
    def getMolangValue(self, molangExpression):
        """Get value of molang."""
        if not self.__queryComp:
            self.__queryComp = CComp.CreateQueryVariable(self.__id)
        result = self.__queryComp.EvalMolangExpression(molangExpression)
        return result.get("value", None)
    
    def setMolangValue(self, molang, value):
        """Set value of molang."""
        if not self.__queryComp:
            self.__queryComp = CComp.CreateQueryVariable(self.__id)
        self.__queryComp.EvalMolangExpression("%s=%s" % (molang, value))

