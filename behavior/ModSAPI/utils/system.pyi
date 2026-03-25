import mod.server.extraServerApi as serverApi
from ..modules.server.World import World
from modules import Modules

class systems:

    @property
    def world() -> World:
        """World"""

    @property
    def modules() -> Modules:
        """Modules"""