# Upgrade - Ocean Killer

# 目标：海洋杀手-玩家在水中击杀水中怪物时能够实现一击必杀的效果
# 尝试初步了解接口，明白如何获取游戏内数据，并编写简单逻辑
from ..ModSAPI.server.beta import * # 导入ModSAPI-server模块

def onEntityHurt(arg):
    # type: (EntityHurtAfterEvent) -> None
    attacker = arg.damageSource.damagingEntity # 攻击者
    if attacker and attacker.typeId == 'minecraft:player':
        # 攻击者是玩家
        entity = arg.hurtEntity # 受伤的实体
        if attacker.isInWater and entity.isInWater:
            # 同时在水中
            entity.kill()
            # 杀死实体

world.afterEvents.entityHurt.subscribe(onEntityHurt)
# 监听实体受伤事件
