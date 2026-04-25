# -*- coding: utf-8 -*-
import mod.server.extraServerApi as serverApi

ServerSystem = serverApi.GetServerSystemCls()

class Modules(ServerSystem):
    """Contains all modules of ModSAPI."""

    @property
    def ItemStack(self):
        from ..modules.server.ItemStack import ItemStack as i
        return i