# Upgrade - Yours is mine!

# 目标：兄弟兄弟，衣服借我穿穿
# 玩家在攻击实体时，有概率夺取对方的装备并穿戴在自己身上
# 玩家受击时，也同样有概率被夺去装备
from ..ModSAPI.server.beta import * # 导入ModSAPI-server模块
import random

def onEntityHurt(arg):
    # type: (EntityHurtAfterEvent) -> None
    attacker = arg.damageSource.damagingEntity
    entity = arg.hurtEntity
    if attacker.hasComponent(EntityEquippableComponent.componentId):
        # 攻击者有装备组件
        if entity.hasComponent(EntityEquippableComponent.componentId):
            # 受击者也有装备组件
            attackerEquip = attacker.getComponent(EntityEquippableComponent.componentId)
            entityEquip = entity.getComponent(EntityEquippableComponent.componentId)
            slots = (EquipmentSlot.Head, EquipmentSlot.Chest, EquipmentSlot.Legs, EquipmentSlot.Feet)
            for slot in slots:
                if random.random() < 0.1:
                    # 10%概率交换装备
                    equipment = attackerEquip.getEquipment(slot)
                    if equipment:
                        # 攻击者有装备，无法替换
                        continue
                    equipment = entityEquip.getEquipment(slot)
                    if equipment:
                        # 受击者有装备，可以替换
                        attackerEquip.setEquipment(slot, equipment)
                        entityEquip.setEquipment(slot)

world.afterEvents.entityHurt.subscribe(onEntityHurt) # 监听实体受伤事件
