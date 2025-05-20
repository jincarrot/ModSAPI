# coding=utf-8
import types

from mod.common.minecraftEnum import EntityComponentType
from ..Interfaces.Sources import *
from EntityEvents import *

ServerSystem = serverApi.GetServerSystemCls()
SComp = serverApi.GetEngineCompFactory()


class EventListener(object):
    """
    事件监听处理器
    """

    def __init__(self, eventName, callback, options=None, detectFunc=None):
        # type: (str, types.FunctionType, EntityEventsOptions, types.FunctionType) -> None
        self.__eventName = eventName
        self.__callback = callback
        self.__options = options
        self.__detectFunction = detectFunc

    @property
    def options(self):
        return self.__options

    def listen(self, data):
        value = self.__detectFunction(self, data)
        if value:
            self.__callback(value)
        """
        arg = {}
        if self.__eventName == "DamageEvent":
            if self.__options:
                if self.__options.entities:
                    entityIds = []
                    for entity in self.__options.entities:
                        entityIds.append(entity.id)
                    if data['entityId'] not in entityIds:
                        return
                if self.__options.entityTypes:
                    if SComp.CreateEngineType(data['entityId']).GetEngineTypeStr() not in self.__options.entityTypes:
                        return
            damagingEntity = data['srcId'] if data['srcId'] else None
            damagingProjectile = data['projectileId']
            temp = {
                "cause": data['cause']
            }
            if damagingEntity:
                temp['damagingEntity'] = Entity(damagingEntity)
            if damagingProjectile:
                temp['damagingProjectile'] = Entity(damagingProjectile)
            arg['damageSource'] = EntityDamageSource(temp)
            arg['hurtEntity'] = Entity(data['entityId'])
            arg['damage'] = data['damage']
            self.__callback(EntityHurtAfterEvent(arg))
        """


class EntityEvents(object):

    def __init__(self):
        pass

    def subscribe(self, callback, options=EntityEventsOptions):
        # type: (types.FunctionType, Dict[str, Union[str, List[Entity]]]) -> None
        if type(options).__name__ != "dict":
            options = None
        else:
            options = EntityEventsOptions(options)

    def unsubscribe(self):
        pass
