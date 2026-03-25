import mod.server.extraServerApi as serverApi
from ..modules.server.World import World
from ..modules.server.System import System
from modules import Modules

class systems:

    @property
    def world() -> World:
        """World"""

    @property
    def system() -> System:
        """System"""

    @property
    def modules() -> Modules:
        """Modules"""