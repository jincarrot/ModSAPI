from ConstMeta import ConstMeta
EntityQueryOptionsProperties = ["closest", "farthest", "location", "maxDistance", "minDistance", "volume"]
MinecraftDimensionTypes = ["minecraft:overworld", "minecraft:nether", "minecraft:the_end"]
Direction_ModSDK = ['Down', 'Up', 'North', 'South', 'West', 'East']


class EntityDamageCause(object):
    """
    Describes the source of damage from an Entity.
    """
    __metaclass__ = ConstMeta
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


class LiquidType(object):
    "Represents the type of liquid that can be placed on a block or flow dynamoically in the world"
    __metaclass__ = ConstMeta
    Water = 'Water'


class ItemLockMode(object):
    """
    Describes how an an item can be moved within a container.
    """
    __metaclass__ = ConstMeta
    none = "none"
    inventory = "inventory"
    slot = "slot"


class Direction(object):
    """
    A general purpose relative direction enumeration.
    """
    __metaclass__ = ConstMeta
    Down = "Down"
    """Returns the @minecraft/server.Block beneath (y - 1) of this item."""

    East = "East"
    """Returns the @minecraft/server.Block to the east (x + 1) of this item."""

    North = "North"
    """Returns the @minecraft/server.Block to the east (z + 1) of this item."""

    South = "South"
    """Returns the @minecraft/server.Block to the south (z - 1) of this item."""

    Up = "Up"
    """Returns the @minecraft/server.Block above (y + 1) of this item."""

    West = "West"
    """Returns the @minecraft/server.Block to the west (x - 1) of this item."""


class EntityComponentTypes(object):
    """
    The types of entity components that are accessible via function Entity.getComponent.
    """
    __metaclass__ = ConstMeta

    __AddRider = "minecraft:addrider"
    """When added, this component makes the entity spawn with a rider of the specified entityType."""
    Health = "minecraft:health"
    """Defines the health properties of an entity."""


EnchantTypes = {
    0: "protection",
    1: "fire_protection",
    2: "feather_falling",
    3: "blast_protection",
    4: "projectile_protection",
    5: "thorns",
    6: "respiration",
    7: "depth_strider",
    8: "aqua_affinity",
    9: "sharpness",
    10: "smite",
    11: "bane_of_arthropods",
    12: "knockback",
    13: "fire_aspect",
    14: "looting",
    15: "efficiency",
    16: "silk_touch",
    17: "unbreaking",
    18: "fortune",
    19: "power",
    20: "punch",
    21: "flame",
    22: "infinity",
    23: "luck_of_the_sea",
    24: "lure",
    25: "frost_walker",
    26: "mending",
    27: "binding_curse",
    28: "vanishing_curse",
    29: "impaling",
    30: "riptide",
    31: "loyalty",
    32: "channeling",
    33: "multishot",
    34: "piercing",
    35: "quick_charge",
    36: "soul_speed",
    37: "swift_sneak",
    38: "wind_burst",
    39: "density",
    40: "breach",
    41: "num_enchantments",
    42: "invalid_enchantment",
    255: "mod_enchant"
}

