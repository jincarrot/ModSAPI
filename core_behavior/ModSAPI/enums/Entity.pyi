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

class EquipmentSlot:
    """The equipment slot of the mob. This includes armor, offhand and mainhand slots."""
    Body = "Body"
    """The body slot. This slot is used to hold armor for non-humanoid mobs."""
    Head = "Head"
    """The head slot. This slot is used to hold items such as Helmets or Carved Pumpkins."""
    Chest = "Chest"
    """The chest slot. This slot is used to hold items such as Chestplate or Elytra."""
    Legs = "Legs"
    """The legs slot. This slot is used to hold items such as Leggings."""
    Feet = "Feet"
    """The feet slot. This slot is used to hold items such as Boots."""
    Offhand = "Offhand"
    """The offhand slot. This slot is used to hold items such as shields and maps."""
    Mainhand = "Mainhand"
    """The mainhand slot. For players, the mainhand slot refers to the currently active hotbar slot."""
    
