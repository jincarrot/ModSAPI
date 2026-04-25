# -*- coding: utf-8 -*-
import mod.server.extraServerApi as serverApi

ServerSystem = serverApi.GetServerSystemCls()

class Enums(ServerSystem):
    """Contains all enums of ModSAPI."""

    @property
    def StructureSaveMode(self):
        from ..enums.Structure import StructureSaveMode as s
        return s()
    
    @property
    def StructureMirrorAxis(self):
        from ..enums.Structure import StructureMirrorAxis as s
        return s()
    
    @property
    def StructureRotation(self):
        from ..enums.Structure import StructureRotation as s
        return s()
    
    @property
    def StructureAnimationMode(self):
        from ..enums.Structure import StructureAnimationMode as s
        return s()
    
    @property
    def EquipmentSlot(self):
        from ..enums.Entity import EquipmentSlot as e
        return e()