
EntityQueryOptionsProperties = ["closest", "farthest", "location", "maxDistance", "minDistance", "volume"]
MinecraftDimensionTypes = ["minecraft:overworld", "minecraft:nether", "minecraft:the_end"]


class EntityDamageCause(object):
    """
    Describes the source of damage from an Entity.
    """
    anvil = 'anvil',
    blockExplosion = 'blockExplosion',
    charging = 'charging',
    contact = 'contact',
    drowning = 'drowning',
    entityAttack = 'entityAttack',
    entityExplosion = 'entityExplosion',
    fall = 'fall',
    fallingBlock = 'fallingBlock',
    fire = 'fire',
    fireTick = 'fireTick',
    fireworks = 'fireworks',
    flyIntoWall = 'flyIntoWall',
    freezing = 'freezing',
    lava = 'lava',
    lightning = 'lightning',
    maceSmash = 'maceSmash',
    magic = 'magic',
    magma = 'magma',
    none = 'none',
    override = 'override',
    piston = 'piston',
    projectile = 'projectile',
    ramAttack = 'ramAttack',
    selfDestruct = 'selfDestruct',
    sonicBoom = 'sonicBoom',
    soulCampfire = 'soulCampfire',
    stalactite = 'stalactite',
    stalagmite = 'stalagmite',
    starve = 'starve',
    suffocation = 'suffocation',
    suicide = 'suicide',
    temperature = 'temperature',
    thorns = 'thorns',
    void = 'void',
    wither = 'wither'


class LiquidType(object):
    "Represents the type of liquid that can be placed on a block or flow dynamoically in the world"
    Water = 'Water'


class ItemLockMode(object):
    """
    Describes how an an item can be moved within a container.
    """
    none = "none",
    inventory = "inventory",
    slot = "slot"
