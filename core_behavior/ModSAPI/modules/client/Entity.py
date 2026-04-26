
import mod.client.extraClientApi as clientApi
CComp = clientApi.GetEngineCompFactory()

class ClientEntity:

    def __init__(self, entityId):
        self.__id = entityId
        self.__nameComp = None
        self.__queryComp = None

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
    def nameTag(self):
        """Name of this entity."""
        if not self.__nameComp:
            self.__nameComp = CComp.CreateName(self.__id)
        return self.__nameComp.GetName()
    
    @property
    def typeId(self):
        """Type identifier of this entity."""
        if not self.__nameComp:
            self.__nameComp = CComp.CreateName(self.__id)
        return self.__nameComp.GetEngineTypeStr()
    
    def getMolangValue(self, molangExpression):
        """Get value of molang."""
        if not self.__queryComp:
            self.__queryComp = CComp.CreateQueryVariable(self.__id)
        result = self.__queryComp.EvalMolangExpression(molangExpression)
        return result.get("value", None)

