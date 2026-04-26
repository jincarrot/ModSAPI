
from Screen import Screen

class ClientPlayer:

    @property
    def id(self):
        """Runtime identifier of this player."""
    
    @property
    def nameTag(self):
        """Name of this player."""
    
    @property
    def name(self):
        """Name of this player."""
    
    @property
    def screen(self) -> Screen:
        """Contains informations of player's screen."""