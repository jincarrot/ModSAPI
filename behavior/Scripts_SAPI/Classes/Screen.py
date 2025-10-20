# -*- coding: utf-8 -*-
import mod.client.extraClientApi as clientApi

class Screen(object):
    "Contains a set of operations about screen"

    def __init__(self, playerId):
        self.__id = playerId

    @property
    def isHud(self):
        pass
