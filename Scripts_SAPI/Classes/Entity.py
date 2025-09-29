# coding=utf-8
# from typing import Any, Union, Dict, List
from mod.common.minecraftEnum import EntityComponentType, RayFilterType

from Effect import *
from ..Interfaces.BlockOptions import *
from ..Interfaces.AnimeOptions import *
from ..Interfaces.EntityOptions import *
from ..Interfaces.TeleportOptions import *
from ..Interfaces.Raycasts import *
from EntityComponents import *
import math, time, random
from Camara import *
from Request import *
from ClientSystemInfo import *
import mod.server.extraServerApi as serverApi
from ..minecraft import *
from Command import *
import types

SComp = serverApi.GetEngineCompFactory()


class Entity(object):
    """
    Represents the state of an entity (a mob, the player, or other moving objects like mine carts) in the world.
    """
    import Dimension as __d
    import Block as __b

    def __init__(self, entityId):
        self.__id = entityId
        self.__healthComp = SComp.CreateAttr(self.__id)

    def __str__(self):
        data = {
            "id": self.id,
            "dimension": str(self.dimension),
            "typeId": self.typeId
        }
        return "<Entity> %s" % data

    @property
    def id(self):
        # type: () -> str
        """
        Unique identifier of the entity.
        This identifier is intended to be consistent across loads of a world instance.
        No meaning should be inferred from the value and structure of this unique identifier - do not parse or interpret it.
        This property is accessible even if Entity.isValid is false.
        """
        return self.__id
    
    @property
    def isValid(self):
        # type: () -> bool
        """"""
        return SComp.CreateGame(serverApi.GetLevelId()).IsEntityAlive(self.__id)

    @property
    def dimension(self):
        # type: () -> Entity.__d.Dimension
        """
        Dimension that the entity is currently within.
        """
        dim = self.__d.Dimension(SComp.CreateDimension(self.__id).GetEntityDimensionId())
        return dim

    @property
    def isClimbing(self):
        # type: () -> bool
        """
        Whether the entity is touching a climbable block. For example, a player next to a ladder or a spider next to a stone wall.
        """
        data = SComp.CreateQueryVariable(self.__id).EvalMolangExpression("query.is_wall_climbing")['value']
        if data:
            return True
        return False

    @property
    def isFalling(self):
        # type: () -> bool
        """
        Whether the entity has a fall distance greater than 0, or greater than 1 while gliding.
        """
        if SComp.CreateEntityDefinitions(self.__id).GetEntityFallDistance():
            return True
        return False

    @property
    def isInWater(self):
        # type: () -> bool
        """
        Whether any part of the entity is inside a water block.
        """
        if SComp.CreateQueryVariable(self.__id).EvalMolangExpression("query.is_in_water")['value']:
            return True
        return False

    @property
    def isOnGround(self):
        # type: () -> bool
        """
        Whether the entity is on top of a solid block.
        This property may behave in unexpected ways.
        This property will always be true when an Entity is first spawned, and if the Entity has no gravity this property may be incorrect.
        """
        if SComp.CreateQueryVariable(self.__id).EvalMolangExpression("query.is_on_ground")['value']:
            return True
        return False

    @property
    def isSleeping(self):
        # type: () -> bool
        """
        If true, the entity is currently sleeping.
        """
        if SComp.CreateQueryVariable(self.__id).EvalMolangExpression("query.is_sleeping")['value']:
            return True
        return False
    
    @property
    def isSitting(self):
        # type: () -> bool
        """
        If true, the entity is currently sitting.
        """
        return SComp.CreateEntityDefinitions(self.__id).IsSitting()

    @property
    def isSneaking(self):
        # type: () -> bool
        """
        Whether the entity is sneaking - that is, moving more slowly and more quietly.
        """
        if SComp.CreateQueryVariable(self.__id).EvalMolangExpression("query.is_sneaking")['value']:
            return True
        return False

    @property
    def isSprinting(self):
        # type: () -> bool
        """
        Whether the entity is sprinting. For example, a player using the sprint action, an ocelot running away or a pig boosting with Carrot on a Stick.
        """
        if SComp.CreateQueryVariable(self.__id).EvalMolangExpression("query.is_sprinting")['value']:
            return True
        return False

    @property
    def isSwimming(self):
        # type: () -> bool
        """
        Whether the entity is in the swimming state. For example, a player using the swim action or a fish in water.
        """
        if SComp.CreateQueryVariable(self.__id).EvalMolangExpression("query.is_swimming")['value']:
            return True
        return False

    @property
    def location(self):
        # type: () -> Vector3
        """
        Current location of the entity.
        """
        pos = SComp.CreatePos(self.__id).GetPos()
        loc = Vector3({"x": pos[0], "y": pos[1], "z": pos[2]})
        return loc

    @property
    def nameTag(self):
        # type: () -> str
        """
        Given name of the entity.
        """
        return SComp.CreateName(self.__id).GetName()

    @nameTag.setter
    def nameTag(self, name):
        # type: (str) -> None
        """
        Given name of the entity.
        """
        SComp.CreateName(self.__id).SetName(name)

    @property
    def health(self):
        return self.__healthComp.GetAttrValue(0)
    
    @health.setter
    def health(self, value):
        self.__healthComp.SetAttrValue(0, value)
    
    @property
    def scoreboardIdentity(self):
        return 0

    @property
    def typeId(self):
        # type: () -> str
        """
        Identifier of the type of the entity - for example, 'minecraft:skeleton'.
        This property is accessible even if @minecraft/server.Entity.isValid is false.
        """
        return SComp.CreateEngineType(self.__id).GetEngineTypeStr()

    def addEffect(self, effectType, duration, options=EntityEffectOptions):
        # type: (str | EffectType, int, EntityEffectOptions | dict) -> Effect
        """
        Adds or updates an effect, like poison, to the entity.
        """
        effectType = effectType if type(effectType) == str else effectType.getName()
        options = EntityEffectOptions(options if type(options) == dict else {})  if type(options) != EntityEffectOptions else options
        SComp.CreateEffect(self.__id).AddEffectToEntity(effectType, duration / 20 + 1, options.amplifier, options.showParticle)

        def stop():
            if SComp.CreateGame(self.__id).IsEntityAlive(self.__id):
                SComp.CreateEffect(self.__id).RemoveEffectFromEntity(effectType)

        if duration < 20:
            SComp.CreateGame(serverApi.GetLevelId()).AddTimer(duration / 20.0, stop)
        return Effect(effectType, duration, options.amplifier)

    def addTag(self, tag):
        # type: (str) -> bool
        """
        Adds a specified tag to an entity.
        """
        return SComp.CreateTag(self.__id).AddEntityTag(tag)

    def applyDamage(self, amount, options=None):
        # type: (int, dict | EntityApplyDamageByProjectileOptions | EntityApplyDamageOptions) -> bool
        """
        Applies a set of damage to an entity.
        """
        if options and type(options).__name__ == 'dict':
            cause = options['cause'] if type(options).__name__ == 'dict' else None
            if not cause and options['damagingProjectile']:
                cause = 'projectile'
                options = EntityApplyDamageByProjectileOptions(options)
                return SComp.CreateHurt(self.__id).Hurt(amount, cause, options.damagingEntity.id, options.damagingProjectile.id, False)
            else:
                options = EntityApplyDamageOptions(options)
                return SComp.CreateHurt(self.__id).Hurt(amount, options.cause, options.damagingEntity.id if options.damagingEntity else None, None, False)
        elif not options:
            cause = "none"
            return SComp.CreateHurt(self.__id).Hurt(amount, cause, None, None, False)
        else:
            if hasattr(options, 'damagingProjectile'):
                return SComp.CreateHurt(self.__id).Hurt(amount, 'projectile', options.damagingEntity.id, options.damagingProjectile.id, False)
            elif hasattr(options, 'cause'):
                return SComp.CreateHurt(self.__id).Hurt(amount, options.cause, options.damagingEntity.id, None, False)

    def applyImpulse(self, vector):
        # type: (Vector3 | dict) -> None
        """
        Applies impulse vector to the current velocity of the entity.
        """
        vector = Vector3(vector) if type(vector).__name__ == 'dict' else vector
        SComp.CreateActorMotion(self.__id).SetMotion((vector.x, vector.y, vector.z))

    def applyKnockback(self, horizontalForce, verticalStrength):
        # type: (dict | VectorXZ, float) -> None
        """
        Applies impulse vector to the current velocity of the entity.
        """
        vector = VectorXZ(horizontalForce) if type(horizontalForce).__name__ == 'dict' else horizontalForce
        SComp.CreateAction(self.__id).SetMobKnockback(vector.x, vector.z, 1.0, verticalStrength)

    def clearDynamicProperties(self):
        # type: () -> None
        """
        Clears all dynamic properties that have been set on this entity.
        """
        DataComp = SComp.CreateExtraData(self.__id)
        data = DataComp.GetWholeExtraData()
        for key in data.keys():
            DataComp.CleanExtraData(key)
        DataComp.SaveExtraData()

    def clearVelocity(self):
        # type: () -> None
        """
        Sets the current velocity of the Entity to zero. Note that this method may not have an impact on Players.
        """
        SComp.CreateActorMotion(self.__id).SetMotion((0, 0, 0))

    def extinguishFire(self, useEffects=True):
        # type: (bool) -> bool
        """
        Extinguishes the fire if the entity is on fire.
        Note that you can call getComponent('minecraft:onfire') and, if present, the entity is on fire.
        @params
        useEffects?: boolean = true
        Whether to show any visual effects connected to the extinguishing.
        """
        if SComp.CreateAttr(self.__id).IsEntityOnFire():
            if useEffects:
                pos = SComp.CreatePos(self.__id).GetPos()
                SComp.CreateCommand(self.__id).SetCommand("setblock %s %s %s powder_snow" % (pos[0], pos[1], pos[2]))
                return True
            else:
                SComp.CreateAttr(self.__id).SetEntityOnFire(0, 0)
                return True
        else:
            return False

    def getBlockFromViewDirection(self, options=BlockRaycastOptions):
        # type: (dict | BlockRaycastOptions) -> BlockRaycastHit
        """
        note: options is not complete
        Returns the first intersecting block from the direction that this entity is looking at.
        """
        options = BlockRaycastOptions(options if type(options) == dict else {}) if type(options) != BlockRaycastOptions else options
        direction = self.getViewDirection()
        location = self.location
        dimension = self.dimension.dimId
        blocks = serverApi.getEntitiesOrBlockFromRay(dimension, (location.x, location.y, location.z), (direction.x, direction.y, direction.z), 32, False, RayFilterType.OnlyBlocks)
        temps = serverApi.getEntitiesOrBlockFromRay(dimension, (location.x, location.y, location.z), (direction.x + 0.000001, direction.y + 0.000001, direction.z + 0.000001), 32, False, RayFilterType.OnlyBlocks)
        if blocks and len(blocks):
            face = None
            block = blocks[0]
            temp = temps[0]
            pos0 = block['hitPos']
            pos1 = temp['hitPos']
            if pos0[0] == pos1[0]:
                if pos0[0] > block['pos'][0] + 0.5:
                    face = Direction.East
                else:
                    face = Direction.West
            elif pos0[1] == pos1[1]:
                if pos0[1] > block['pos'][1] + 0.5:
                    face = Direction.Up
                else:
                    face = Direction.Down
            else:
                if pos0[2] > block['pos'][2] + 0.5:
                    face = Direction.North
                else:
                    face = Direction.South
            data = {
                "block": self.__b.Block({"location": Vector3({"x": block['pos'][0], "y": block['pos'][1], "z": block['pos'][2]}), "dimension": self.dimension}),
                "face": face,
                "faceLocation": Vector3({"x": block['hitPos'][0], "y": block['hitPos'][1], "z": block['hitPos'][2]})
            }
            return BlockRaycastHit(data)
        return None

    def getComponent(self, componentId):
        # type: (str) -> EntityComponent | None
        """
        Gets a component (that represents additional capabilities) for an entity.
        """
        if not self.hasComponent(componentId):
            print("Get entity component error! component '%s' isn't exist in this entity" % componentId)
            return None
        if componentId.find("minecraft:") >= 0:
            componentId = componentId[10::].lower()
        if componentId in vars(EntityComponentType).keys():
            import Components as comp
            return comp.EntityComponentGenerater(self, componentId).get()
        else:
            print("Get entity component error! No such component name '%s'" % componentId)
            return None

    def getComponents(self):
        # type: () -> list[EntityComponent]
        """
        Returns all components that are both present on this entity and supported by the API.
        """
        componentNames = SComp.CreateEntityComponent(self.__id).GetAllComponentsName()
        components = []
        for name in componentNames:
            components.append(self.getComponent(name))
        return components

    def getDynamicProperty(self, identifier):
        # type: (str) -> 0
        """
        Returns a property value.
        """
        DataComp = SComp.CreateExtraData(self.__id)
        return DataComp.GetExtraData(identifier) if identifier in self.getDynamicPropertyIds() else None

    def getDynamicPropertyIds(self):
        # type: () -> list[str]
        """
        Returns the available set of dynamic property identifiers that have been used on this entity.
        """
        DataComp = SComp.CreateExtraData(self.__id)
        data = DataComp.GetWholeExtraData()
        return data.keys()

    def getDynamicPropertyTotalByteCount(self):
        # type: () -> int
        """
        Returns the total size, in bytes, of all the dynamic properties that are currently stored for this entity.
        This includes the size of both the key and the value.
        This can be useful for diagnosing performance warning signs -
        if, for example, an entity has many megabytes of associated dynamic properties, it may be slow to load on various devices.
        """
        DataComp = SComp.CreateExtraData(self.__id)
        data = DataComp.GetWholeExtraData()
        count = 0
        for key in data.keys():
            count += len(key)
            value = data[key]
            if type(value).__name__ == 'str':
                count += len(value)
            else:
                count += 8
        return count

    def getEffect(self, effectType):
        # type: (str | EffectType) -> Effect
        """
        Returns the effect for the specified EffectType on the entity,
        undefined if the effect is not present, or throws an error if the effect does not exist.
        """
        effectType = effectType if type(effectType).__name__ == 'str' else effectType.getName()
        if SComp.CreateEffect(self.__id).HasEffect(effectType):
            datas = SComp.CreateEffect(self.__id).GetAllEffects()
            data = None
            for d in datas:
                if d['effectName'] == effectType:
                    data = d
                    break
            effect = Effect(effectType, int(data['duration_f'] * 20), data['amplifier'])
            return effect

    def getEffects(self):
        # type: () -> list[Effect]
        """
        Returns a set of effects applied to this entity.
        """
        datas = SComp.CreateEffect(self.__id).GetAllEffects()
        effects = []
        if not datas:
            datas = []
        for data in datas:
            effects.append(Effect(data['effectName'], int(data['duration_f'] * 20), data['amplifier']))
        return effects

    def getEntitiesFromViewDirection(self, options=EntityRaycastOptions):
        # type: (dict) -> list[EntityRaycastHit]
        """
        Gets the entities that this entity is looking at by performing a ray cast from the view of this entity.
        """
        direction = self.getViewDirection()
        location = self.location
        dimension = self.dimension.dimId
        entities = serverApi.getEntitiesOrBlockFromRay(dimension, (location.x, location.y, location.z), (direction.x, direction.y, direction.z), 16, True, RayFilterType.OnlyEntities)
        if len(entities):
            results = []
            for entity in entities:
                distance = math.sqrt((entity['hitPos'][0] - location.x) ** 2 + (entity['hitPos'][1] - location.y) ** 2 + (entity['hitPos'][2] - location.z) ** 2)
                results.append(EntityRaycastHit({"entity": createEntity(entity['entityId']), "distance": distance}))
            return results

    def getHeadLocation(self):
        # type: () -> Vector3
        """
        Returns the current location of the head component of this entity.
        """
        data = SComp.CreateCollisionBox(self.__id).GetSize()
        pos = SComp.CreatePos(self.__id).GetFootPos()
        location = Vector3({"x": pos[0], "y": pos[1] + data[1] * 0.85, "z": pos[2]})
        return location

    def getRotation(self):
        # type: () -> Vector2
        """
        Returns the current rotation component of this entity.
        """
        rot = SComp.CreateRot(self.__id).GetRot()
        return Vector2({"x": rot[0], "y": rot[1]})

    def getTags(self):
        # type: () -> list[str]
        """
        Returns all tags associated with the entity.
        """
        return SComp.CreateTag(self.__id).GetEntityTags()

    def getVelocity(self):
        # type: () -> Vector3
        """
        Returns the current velocity vector of the entity.
        """
        v = SComp.CreateActorMotion(self.__id).GetMotion()
        return Vector3({"x": v[0], 'y': v[1], 'z': v[2]})

    def getProperty(self, identifier):
        # type: (str) -> 0
        """
        Gets an entity Property value.
        If the property was set using the setProperty function within the same tick, the updated value will not be reflected until the subsequent tick.
        """
        return SComp.CreateQueryVariable(self.__id).EvalMolangExpression("q.property('%s')" % identifier)['value']

    def getViewDirection(self):
        # type: () -> Vector3
        """
        Returns the current view direction of the entity.
        """
        rot = SComp.CreateRot(self.__id).GetRot()
        direction = serverApi.GetDirFromRot(rot)
        return Vector3({"x": direction[0], "y": direction[1], "z": direction[2]})

    def getFamilies(self):
        """
        Returns family types
        """
        return SComp.CreateAttr(self.__id).GetTypeFamily()

    def hasComponent(self, componentId):
        # type: (str) -> bool
        """
        Returns true if the specified component is present on this entity.
        """
        componentId = componentId[10::].lower() if "minecraft:" in componentId else componentId
        return SComp.CreateEntityComponent(self.__id).HasComponent(getattr(EntityComponentType, componentId))

    def hasTag(self, tag):
        # type: (str) -> bool
        """
        Returns whether an entity has a particular tag.
        """
        return SComp.CreateTag(self.__id).EntityHasTag(tag)

    def hasTarget(self):
        # type: () -> bool
        """Returns True if entity has a target"""
        targetId = SComp.CreateAction(self.__id).GetAttackTarget()
        if targetId == -1 or not targetId:
            return False
        else:
            return True
        
    def getTarget(self):
        # type: () -> Entity | None
        """Returns the target if entity has a target"""
        targetId = SComp.CreateAction(self.__id).GetAttackTarget()
        if targetId == -1 or not targetId:
            return None
        else:
            return createEntity(targetId)

    def hasFamily(self, familyName):
        # type: (str) -> bool
        """
        Returns whether an entity belongs to a family.
        """
        families = SComp.CreateAttr(self.__id).GetTypeFamily()
        return familyName in families

    def kill(self):
        # type: () -> bool
        """
        Kills this entity. The entity will drop loot as normal.
        Returns boolean - Returns true if entity can be killed (even if it is already dead), otherwise it returns false.
        """
        return SComp.CreateGame(serverApi.GetLevelId()).KillEntity(self.__id)

    def matches(self, options=None):
        # type: (dict) -> bool
        """
        Matches the entity against the passed in options.
        Uses the location of the entity for matching if the location is not specified in the passed in EntityQueryOptions.
        """
        options = EntityQueryOptions(options if type(options) == dict else {}) if type(options) != EntityQueryOptions else options
        if options.selfCheck():
            if len(options.check([self.__id])):
                return True
        return False

    def playAnimation(self, animationName, options=None):
        # type: (str, dict | PlayAnimationOptions) -> None
        """
        Cause the entity to play the given animation.
        """
        options = PlayAnimationOptions(options if type(options) == dict else {}) if type(options) != PlayAnimationOptions else options
        SComp.CreateCommand(serverApi.GetLevelId()).SetCommand('playanimation @s "%s" %s %s %s %s' % (animationName, options.nextState, options.blendOutTime, options.stopExpression, options.controller), self.__id)

    def remove(self):
        # type: () -> None
        """
        Immediately removes the entity from the world.
        The removed entity will not perform a death animation or drop loot upon removal.
        """
        global world
        if not world:
            world = getWorld()
        world.DestroyEntity(self.__id)

    def removeEffect(self, effectType):
        # type: (str | EffectType) -> bool
        """
        Removes the specified EffectType on the entity, or returns false if the effect is not present.
        """
        effectType = effectType if type(effectType).__name__ == 'str' else effectType.getName()
        return SComp.CreateEffect(self.__id).RemoveEffectFromEntity(effectType)

    def removeTag(self, tag):
        # type: (str) -> bool
        """
        Removes a specified tag from an entity.
        """
        return SComp.CreateTag(self.__id).RemoveEntityTag(tag)

    def resetProperty(self, identifier):
        # type: (str) -> 0
        """
        Resets an Entity Property back to its default value, as specified in the Entity's definition.
        This property change is not applied until the next tick.
        """
        ori = SComp.CreateQueryVariable(self.__id).EvalMolangExpression("q.property('%s')" % identifier)['value']

        # 获取原nbt
        nbt = SComp.CreateEntityDefinitions(self.__id).GetEntityNBTTags()
        # 检测是否存在该值
        if 'properties' in nbt and identifier in nbt['properties']:
            # 生成临时实体便于获取默认值
            tempLoc = self.location
            tempLoc = (tempLoc.x, tempLoc.y + 100, tempLoc.z)
            tempDim = SComp.CreateDimension(self.__id).GetEntityDimensionId()
            tempEntity = world.CreateEngineEntityByTypeStr(self.typeId, tempLoc, (0, 0), tempDim)
            tempEntity = createEntity(tempEntity)
            # 获取默认值并存入原数据
            value = tempEntity.getProperty(identifier)
            nbt['properties'][identifier]['__value__'] = value if type(value).__name__ != 'bool' else int(value)
            world.DestroyEntity(self.__id)
            tempEntity.remove()
            self.__id = world.CreateEngineEntityByNBT(nbt)
            return value

    def runCommand(self, commandString):
        # type: (str) -> CommandResult
        """
        Runs a synchronous command on the entity.

        Note: it may return wrong message
        """
        SComp.CreateCommand(serverApi.GetLevelId()).SetCommand(commandString, self.__id)
        index = commandString.find("@")
        if index >= 0:
            selector = ""
            while index < len(commandString):
                hasParam = False
                if commandString[index] == "[":
                    hasParam = True
                if commandString[index] == "]":
                    selector += commandString[index]
                    break
                if commandString[index] == " " and not hasParam:
                    break
                selector += commandString[index]
                index += 1
            return CommandResult({"successCount": len(SComp.CreateEntityComponent(self.__id).GetEntitiesBySelector(selector))})
        return None

    def setDynamicProperty(self, identifier, value):
        # type: (str, 0) -> None
        """
        Sets a specified property to a value.
        """
        DataComp = SComp.CreateExtraData(self.__id)
        DataComp.SetExtraData(identifier, value)
        DataComp.SaveExtraData()

    def setOnFire(self, seconds, useEffects=True):
        # type: (int, bool) -> bool
        """
        Sets an entity on fire (if it is not in water or rain).
        Note that you can call getComponent('minecraft:onfire') and, if present, the entity is on fire.
        """
        return SComp.CreateAttr(self.__id).SetEntityOnFire(seconds)

    def setProperty(self, identifier, value):
        # type: (str, 0) -> None
        """
        Sets an Entity Property to the provided value.
        This property change is not applied until the next tick.
        """
        SComp.CreateQueryVariable(self.__id).SetPropertyValue(identifier, value)

    def setRotation(self, rotation):
        # type: (str | Vector2) -> None
        """
        Sets the main rotation of the entity.
        """
        rotation = Vector2({rotation}) if type(rotation).__name__ == 'dict' else rotation
        SComp.CreateRot(self.__id).SetRot((rotation.x, rotation.y))

    def teleport(self, location, teleportOptions=None):
        # type: (Vector3 | dict, dict | TeleportOptions) -> None
        """
        Teleports the selected entity to a new location
        """
        location = Vector3(location if type(location) == dict else {}) if type(location) != Vector3 else location
        teleportOptions = TeleportOptions(teleportOptions if type(teleportOptions) == dict else {}) if type(teleportOptions) != TeleportOptions else teleportOptions
        SComp.CreatePos(self.__id).SetFootPos((location.x, location.y, location.z))

    def triggerEvent(self, eventName):
        # type: (str) -> None
        """
        Triggers an entity type event.
        For every entity, a number of events are defined in an entities' definition for key entity behaviors;
        for example, creepers have a minecraft:start_exploding type event.
        """
        SComp.CreateEntityEvent(self.__id).TriggerCustomEvent(self.__id, eventName)

    def tryTeleport(self, location, teleportOptions=TeleportOptions):
        # type: (dict | Vector3, dict) -> bool
        """
        Attempts to try a teleport, but may not complete the teleport operation (for example, if there are blocks at the destination.)
        """
        SComp.CreateCommand(serverApi.GetLevelId()).SetCommand("tp @s %s %s %s true" % (location.x, location.y, location.z), self.__id)

    def asPlayer(self):
        # type: () -> Player
        """get the player object"""
        if self.typeId == 'minecraft:player':
            return Player(self.__id)
        else:
            print("error! This entity is not a player.")
            return None


class Player(Entity):
    """
    Represents a player within the world.
    """
    import Container as con

    def __init__(self, playerId):
        # type: (str) -> None
        Entity.__init__(self, playerId)
        self.__id = playerId
        self.__container = self.con.Container(None, self.__id)

    def __str__(self):
        data = {
            "id": self.id,
            "dimension": str(self.dimension),
            "name": self.name
        }
        return "<Player> %s" % data
    
    @property
    def name(self):
        """
        Name of the player.
        """
        return self.nameTag

    @property
    def camera(self):
        # type: () -> Camera
        """
        The player's Camera.

        No use now.
        """
        return Camera(self.__id)
    
    @property
    def isFlying(self):
        # type: () -> bool
        """Whether the player is flying. For example, in Creative or Spectator mode."""
        return SComp.CreateFly(self.__id).IsPlayerFlying()
    
    @property
    def level(self):
        # type: () -> int
        """The current overall level for the player, based on their experience."""
        return SComp.CreateLv(self.__id).GetPlayerLevel()

    @property
    def selectedSlotIndex(self):
        """the index of selected slot"""
        return SComp.CreateItem(self.__id).GetSelectSlotId()
    
    @selectedSlotIndex.setter
    def selectedSlotIndex(self, slotId):
        # type: (int) -> None
        SComp.CreatePlayer(self.__id).ChangeSelectSlot(slotId)

    @property
    def client(self):
        pass
    
    @property
    def clientSystemInfo(self):
        # type: () -> ClientSystemInfo
        """
        Contains the player's device information.
        """
        requestId = request.create(self.__id, "clientSystemInfo")
        value = request.getValue(requestId)
        return ClientSystemInfo(value)

    @property
    def container(self):
        # type: () -> con.Container
        """returns the container of player's inventory"""
        return self.__container

    @property
    def mainHand(self):
        # type: () -> ItemStack
        """get the item of main hand"""
        return self.container.getItem(self.selectedSlotIndex)
    
    @mainHand.setter
    def mainHand(self, item):
        # type: (ItemStack) -> None
        self.container.setItem(self.selectedSlotIndex, item)
    
    def applyKnockback(self, horizontalForce, verticalStrength):
        # type: (dict | VectorXZ, float) -> None
        """
        Applies impulse vector to the current velocity of the entity.
        """
        vector = VectorXZ(horizontalForce) if type(horizontalForce).__name__ == 'dict' else horizontalForce
        SComp.CreateActorMotion(self.__id).SetPlayerMotion((vector.x, verticalStrength, vector.z))

    def playSound(self, soundID, soundOptions=PlayerSoundOptions):
        # type: (str, dict) -> None
        if soundOptions == PlayerSoundOptions:
            soundOptions = {}
        if 'location' not in soundOptions:
            pos = SComp.CreatePos(self.__id).GetPos()
            soundOptions['location'] = Vector3({"x": pos[0], "y": pos[1], "z": pos[2]})
        options = PlayerSoundOptions(soundOptions) if type(soundOptions) == dict else soundOptions
        SComp.CreateCommand(serverApi.GetLevelId()).SetCommand("playsound %s @s %s %s %s %s %s" % (soundID, options.location.x, options.location.y, options.location.z, options.volume, options.pitch), self.__id)

    def sendMessage(self, message):
        # type: (str) -> None
        """Sends a message to the player."""
        SComp.CreateMsg(self.__id).NotifyOneMessage(self.__id, message)

    def getSpawnPoint(self):
        # type: () -> Vector3
        """Gets the current spawn point of the player."""
        return Vector3(SComp.CreatePlayer(self.__id).GetPlayerRespawnPos())

    def sendToast(self, message, title=""):
        # type: (str, str) -> None
        """
        send a toast to player
        """
        global world
        data = {
            "title": title,
            "message": message
        }
        if not world:
            world = getWorld()
        world.NotifyToClient(self.__id, "sendToast", data)


def createEntity(entityId):
    # type: (str) -> Entity | Player | None
    en = Entity(entityId)
    if en.isValid:
        if en.typeId == 'minecraft:player':
            return en.asPlayer()
        else:
            return en
    return en