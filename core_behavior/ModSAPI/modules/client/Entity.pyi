from ...interfaces.Vector import Vector3

class ClientEntity:
    """Client entity."""

    @property
    def id(self):
        """Runtime identifier of this entity."""
    
    @property
    def nameTag(self):
        """Name of this entity."""
    
    @property
    def typeId(self):
        """Type identifier of this entity."""

    @property
    def location(self) -> Vector3:
        """Location of this entity."""

    @property
    def isValid(self):
        """Whether this entity is valid."""
    
    def getMolangValue(self, molangExpression):
        """Get value of molang."""
    
    def setMolangValue(self, molang, value):
        """Set value of molang."""

