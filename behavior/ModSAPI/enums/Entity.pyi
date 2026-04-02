class EntityDamageCause(object):
    """
    Describes the source of damage from an Entity.
    """
    anvil = 'anvil'
    blockExplosion = 'block_explosion'
    charging = 'charging'
    contact = 'contact'
    drowning = 'drowning'
    entityAttack = 'entity_attack'
    entityExplosion = 'entity_explosion'
    fall = 'fall'
    fallingBlock = 'falling_block'
    fire = 'fire'
    fireTick = 'fire_tick'
    fireworks = 'fireworks'
    flyIntoWall = 'fly_into_wall'
    freezing = 'freezing'
    lava = 'lava'
    lightning = 'lightning'
    maceSmash = 'mace_smash'
    magic = 'magic'
    magma = 'magma'
    none = 'none'
    override = 'override'
    piston = 'piston'
    projectile = 'projectile'
    ramAttack = 'ram_attack'
    selfDestruct = 'self_destruct'
    sonicBoom = 'sonic_boom'
    soulCampfire = 'soul_campfire'
    stalactite = 'stalactite'
    stalagmite = 'stalagmite'
    starve = 'starve'
    suffocation = 'suffocation'
    suicide = 'suicide'
    temperature = 'temperature'
    thorns = 'thorns'
    void = 'void'
    wither = 'wither'

class EntityComponentTypes(object):
    """
    The types of entity components that are accessible via function Entity.getComponent.
    """

    __AddRider = "minecraft:addrider"
    """When added, this component makes the entity spawn with a rider of the specified entityType."""
    Health = "minecraft:health"
    """Defines the health properties of an entity."""
