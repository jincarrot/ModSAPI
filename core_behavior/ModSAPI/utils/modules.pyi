# -*- coding: utf-8 -*-
import mod.server.extraServerApi as serverApi
from ..modules.server.ItemStack import ItemStack
ServerSystem = serverApi.GetServerSystemCls()

class Modules(ServerSystem):
    """Contains all modules of ModSAPI."""

    @property
    def ItemStack(self) -> ItemStack: ...
    