# -*- coding: utf-8 -*-
import mod.client.extraClientApi as clientApi
from ..Interfaces.Vector import *

CComp = clientApi.GetEngineCompFactory()

class Particle(object):
    "Contains a set of operations about particles"

    def __init__(self, playerId=clientApi.GetLocalPlayerId()):
        self.__id = playerId

    def spawnParticle(self, effectName, location, molangVariables=None):
        # type: (str, Vector3, None) -> None
        """生成粒子"""
        CComp.CreateParticleSystem(None).Create(effectName, location)

