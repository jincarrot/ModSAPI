
EntityQueryOptionsProperties = ["closest", "farthest", "location", "maxDistance", "minDistance", "volume"]
MinecraftDimensionTypes = ["minecraft:overworld", "minecraft:nether", "minecraft:the_end"]
Direction_ModSDK = ['Down', 'Up', 'North', 'South', 'West', 'East']


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


class Direction(object):
    """
    A general purpose relative direction enumeration.
    """
    @property
    def Down(self):
        """Returns the @minecraft/server.Block beneath (y - 1) of this item."""
        return "Down"
    @property
    def East(self):
        """Returns the @minecraft/server.Block to the east (x + 1) of this item."""
        return "East"
    @property
    def North(self):
        """Returns the @minecraft/server.Block to the east (z + 1) of this item."""
        return "North"
    @property
    def South(self):
        """Returns the @minecraft/server.Block to the south (z - 1) of this item."""
        return "South"
    @property
    def Up(self):
        """Returns the @minecraft/server.Block above (y + 1) of this item."""
        return "Up"
    @property
    def West(self): 
        """Returns the @minecraft/server.Block to the west (x - 1) of this item."""
        return "West"


class EntityComponentTypes(object):
    """
    The types of entity components that are accessible via function Entity.getComponent.
    """

    __AddRider = "minecraft:addrider"
    """When added, this component makes the entity spawn with a rider of the specified entityType."""
    Health = "minecraft:health"
    """Defines the health properties of an entity."""


class GameMode(object):
    """
    Represents a game mode for the current world experience.
    """
    
    adventure = 'adventure'
    """World is in a more locked-down experience, where blocks may not be manipulated."""

    creative = 'creative'
    """World is in a full creative mode. In creative mode, the player has all the resources
    available in the item selection tabs and the survival selection tab. They can also destroy
    blocks instantly including those which would normally be indestructible. Command and
    structure blocks can also be used in creative mode. Items also do not lose durability or disappear."""
    
    spectator = 'spectator'
    
    survival = 'survival'
    """World is in a survival mode, where players can take damage and entities may not be peaceful.
    Survival mode is where the player must collect resources, build structures while surviving
    in their generated world. Activities can, over time, chip away at player health and hunger bar."""


class ItemLockMode(object):
    """
    Specifies the lock mode for items in containers.
    """
    
    inventory = 'inventory'
    
    none = 'none'
    
    slot = 'slot'