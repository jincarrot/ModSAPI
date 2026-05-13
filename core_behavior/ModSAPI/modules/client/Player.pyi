from ...interfaces.Vector import Vector3

class ClientPlayer:

    @property
    def id(self):
        """Runtime identifier of this player."""
    
    @property
    def name(self) -> str:
        """Name of this player."""

    @property
    def location(self) -> Vector3:
        """Location of this player."""
    