# -*- coding: utf-8 -*-
import mod.server.extraServerApi as serverApi
from ..modules.server.ItemStack import ItemStack
from ..modules.server_ui.FormData import CustomForm, Observable
ServerSystem = serverApi.GetServerSystemCls()

class Modules(ServerSystem):
    """Contains all modules of ModSAPI."""

    @property
    def ItemStack(self) -> ItemStack: ...
    
    @property
    def CustomForm(self) -> CustomForm: ...

    @property
    def Observable(self) -> Observable: ...

    