# -*- coding: utf-8 -*-
from typing import Final
from utils.system import systems
from indexd import *

# Constants
world = systems.world
"""A class that wraps the state of a world - a set of dimensions and the environment of Minecraft."""
system = systems.system
"""A class that provides system-level events and functions."""

# Modules
ItemStack = systems.modules.ItemStack
"""Defines a collection of items."""

# Types

# Enums
StructureSaveMode = systems.enums.StructureSaveMode
"""
Specifies how a structure should be saved.
"""
StructureMirrorAxis = systems.enums.StructureMirrorAxis
"""
Specifies how a structure should be mirrored when placed.
"""

StructureRotation = systems.enums.StructureRotation
"""
Enum describing a structure's placement rotation.
"""

StructureAnimationMode = systems.enums.StructureAnimationMode
"""
Specifies how structure blocks should be animated when a structure is placed.
"""
