# -*- coding: utf-8 -*-
# from typing import Union, Dict

from ..Events.EntityEventSignals import *
import mod.server.extraServerApi as serverApi
import mod.client.extraClientApi as clientApi

SComp = serverApi.GetEngineCompFactory()
CComp = clientApi.GetEngineCompFactory()


class WorldAfterEvents(object):
    """
    Contains a set of events that are available across the scope of the World.
    """

    def __init__(self):
        self.__entityDie = EntityDieAfterEventSignal()
        self.__effectAdd = EffectAddAfterEventSignal()
        self.__entityHealthChanged = EntityHealthChangedAfterEventSignal()
        self.__entityHitBlock = EntityHitBlockAfterEventSignal()
        self.__entityHitEntity = EntityHitEntityAfterEventSignal()
        self.__entityHurt = EntityHurtAfterEventSignal()
        self.__entityLoad = EntityLoadAfterEventSignal()
        self.__entityRemove = EntityRemoveAfterEventSignal()
        self.__entitySpawn = EntitySpawnAfterEventSignal()

    @property
    def entityDie(self):
        """
        Supports registering for an event that fires after an entity has died.
        """
        return self.__entityDie

    @property
    def effectAdd(self):
        """
        error
        
        This event fires when an effect, like poisoning, is added to an entity.
        """
        return self.__effectAdd

    @property
    def entityHealthChanged(self):
        """
        This event fires when entity health changes in any degree.
        """
        return self.__entityHealthChanged

    @property
    def entityHitBlock(self):
        """
        This event fires when entity health changes in any degree.
        """
        return self.__entityHitBlock

    @property
    def entityHurt(self):
        """
        This event fires when an entity is hurt (takes damage).
        """
        return self.__entityHurt


class WorldBeforeEvents(object):
    pass
