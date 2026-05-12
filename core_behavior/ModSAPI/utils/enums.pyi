# -*- coding: utf-8 -*-
import mod.server.extraServerApi as serverApi
from ..enums.Structure import *
from ..enums.Entity import *
from ..enums.Player import *
ServerSystem = serverApi.GetServerSystemCls()

class Enums:
    """Contains all enums of ModSAPI."""

    @property
    def StructureSaveMode(self) -> StructureSaveMode: ...
    
    @property
    def StructureMirrorAxis(self) -> StructureMirrorAxis: ...
    
    @property
    def StructureRotation(self) -> StructureRotation: ...
    
    @property
    def StructureAnimationMode(self) -> StructureAnimationMode: ...
    
    @property
    def EquipmentSlot(self) -> EquipmentSlot: ...

    @property
    def PlayerPermissionLevel(self) -> PlayerPermissionLevel: ...
    