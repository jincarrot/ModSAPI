# -*- coding: utf-8 -*-
import mod.server.extraServerApi as serverApi
from ..modules.server.ItemStack import ItemStack
from ..modules.server_ui.FormData import CustomForm, Observable
from ..modules.server.MolangVariableMap import MolangVariableMap
ServerSystem = serverApi.GetServerSystemCls()

class Modules:
    """Contains all modules of ModSAPI."""

    @property
    def ItemStack(self) -> ItemStack: ...
    
    @property
    def CustomForm(self) -> CustomForm: ...

    @property
    def Observable(self) -> Observable: ...

    @property
    def MolangVariableMap(self) -> MolangVariableMap: ...
