# -*- coding: utf-8 -*-
import mod.client.extraClientApi as clientApi
from ..server_ui.UI import *

class Screen(object):
    "Contains a set of operations about screen."

    @property
    def isHud(self):
        # type: () -> bool
        """returns true if the screen is hud."""
        return clientApi.GetTopUI() == "hud_screen"
    
    @property
    def top(self):
        """the top ui object of this screen"""
        return 
    
    @top.setter
    def top(self, newScreen):
        # type: (UI) -> None
        self.popUI()
        self.pushUI(newScreen)
    
    def pushUI(self, customUI):
        # type: (UI) -> None
        """show a custom ui to player"""
        # Screens[id(customUI)] = customUI
        clientApi.PushScreen("modsapi", "CustomUI", {"screenId": id(customUI)})

    def popUI(self):
        """remove the top ui"""
        clientApi.PopScreen()

    def _attachUI(self, customUI):
        # Screens[id(customUI)] = customUI
        clientApi.CreateUI("modsapi", "CustomUI", {"screenId": id(customUI), "isHud": 1})

