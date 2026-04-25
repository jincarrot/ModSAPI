# -*- coding: utf-8 -*-
import mod.server.extraServerApi as serverApi
from typing import TypedDict
from ..enums.Structure import *

class StructureCreateOptions(TypedDict):
    includeBlocks: bool
    includeEntities: bool
    includeAir: bool
    saveMode: StructureSaveMode

class StructurePlaceOptions(TypedDict):
    animationMode: str
    animationSeconds: str
    includeBlocks: bool
    includeEntities: bool
    integrity: float
    integritySeed: int
    mirror: StructureMirrorAxis
    rotation: StructureRotation
    waterlogged: bool
