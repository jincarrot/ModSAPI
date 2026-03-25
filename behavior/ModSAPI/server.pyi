# -*- coding: utf-8 -*-
from typing import Final
from utils.system import systems

# Constants
world: Final = systems.world
system: Final = systems.system

# Classes
ItemStack: Final = systems.modules.ItemStack

# Types
# Events
from .events.core.BlockEvents import *
from .events.core.EntityEvents import *
from .events.core.WorldEvents import *
from .events.core.PlayerEvents import *
from .events.core.ProjectileEvents import *
