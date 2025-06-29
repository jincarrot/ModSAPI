# -*- coding: utf-8 -*-
# from typing import Union, Dict

from ..Events.EntityEventSignals import *
from ..Events.PlayerEventSignals import *
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
        self.__chatSend = ChatSendAfterEventSignal()
        self.__itemUse = ItemUseAfterEventSignal()

    @property
    def entityDie(self):
        """
        Supports registering for an event that fires after an entity has died.
        """
        return self.__entityDie

    @property
    def _effectAdd(self):
        """
        error
        
        This event fires when an effect, like poisoning, is added to an entity.
        """
        return self.__effectAdd

    @property
    def _entityHealthChanged(self):
        """
        This event fires when entity health changes in any degree.
        """
        return self.__entityHealthChanged

    @property
    def _entityHitBlock(self):
        """
        This event fires when entity health changes in any degree.
        """
        return self.__entityHitBlock

    @property
    def _entityHurt(self):
        """
        This event fires when an entity is hurt (takes damage).
        """
        return self.__entityHurt
    
    @property
    def chatSend(self):
        """
        This event is triggered after a chat message has been broadcast or sent to players.
        """
        return self.__chatSend
    
    @property
    def itemUse(self):
        """
        This event fires when an item is successfully used by a player.
        """
        return self.__itemUse


class WorldBeforeEvents(object):
    pass
