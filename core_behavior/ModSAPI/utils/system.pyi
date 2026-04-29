import mod.server.extraServerApi as serverApi
from ..modules.server.World import World
from ..modules.server.System import System
from modules import Modules
from enums import Enums
from components import Components

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

    @property
    def enums() -> Enums:
        """Enums"""

    @property
    def components() -> Components: 
        """Components"""