# -*- coding: utf-8 -*-

from system import systems

world = systems.world
system = systems.system


ItemStack = systems.modules.ItemStack
MolangVariableMap = systems.modules.MolangVariableMap
Vector3 = systems.modules.Vector3


StructureSaveMode = systems.enums.StructureSaveMode
StructureMirrorAxis = systems.enums.StructureMirrorAxis
StructureRotation = systems.enums.StructureRotation
StructureAnimationMode = systems.enums.StructureAnimationMode

EquipmentSlot = systems.enums.EquipmentSlot

EntityEquippableComponent = systems.components.EntityEquippableComponent
EntityInventoryComponent = systems.components.EntityInventoryComponent