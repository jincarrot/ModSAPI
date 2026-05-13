# -*- coding: utf-8 -*-
import mod.server.extraServerApi as serverApi

ServerSystem = serverApi.GetServerSystemCls()

class Modules(ServerSystem):
    """Contains all modules of ModSAPI."""

    @property
    def ItemStack(self):
        from ..modules.server.ItemStack import ItemStack as i
        return i
    
    @property
    def CustomForm(self):
        from ..modules.server_ui.FormData import CustomForm as c
        return c
    
    @property
    def Observable(self):
        from ..modules.server_ui.FormData import Observable as o
        return o

    @property
    def MoreUI(self):
        from ..modules.server_ui.FormData import MoreUI as m
        return m
    
    @property
    def MolangVariableMap(self):
        from ..modules.server.MolangVariableMap import MolangVariableMap as m
        return m
    
    @property
    def ActionFormData(self):
        from ..modules.server_ui.FormData import ActionFormData as a
        return a
    
    @property
    def ModalFormData(self):
        from ..modules.server_ui.FormData import ModalFormData as m
        return m
    