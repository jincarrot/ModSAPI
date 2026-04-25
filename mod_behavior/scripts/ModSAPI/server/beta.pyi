# -*- coding: utf-8 -*-
from typing import Final
from indexd import *

# Constants
world: World
"""A class that wraps the state of a world - a set of dimensions and the environment of Minecraft."""
system: System
"""A class that provides system-level events and functions."""

# Modules
class ItemStack(systems.modules.ItemStack):
    """Defines a collection of items."""

# Types

# Enums
class StructureSaveMode(systems.enums.StructureSaveMode):
    """
    Specifies how a structure should be saved.
    """
class StructureMirrorAxis(systems.enums.StructureMirrorAxis):
    """
    Specifies how a structure should be mirrored when placed.
    """

class StructureRotation(systems.enums.StructureRotation):
    """
    Enum describing a structure's placement rotation.
    """

class StructureAnimationMode(systems.enums.StructureAnimationMode):
    """
    Specifies how structure blocks should be animated when a structure is placed.
    """

class EquipmentSlot(systems.enums.EquipmentSlot):
    """
    Specifies the slot in which an item can be equipped.
    """
