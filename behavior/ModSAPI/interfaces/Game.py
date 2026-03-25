# -*- coding: utf-8 -*-

import mod.server.extraServerApi as serverApi

comp = serverApi.GetEngineCompFactory()


class GameRules(object):
    """
    Game rules. These values can also be controlled via the /gamerule command.
    """

    def __init__(self):
        pass
