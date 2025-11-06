# -*- coding: utf-8 -*-
import mod.client.extraClientApi as clientApi
from ..Classes.UI import *

class Screen(object):
    "Contains a set of operations about screen"

    def __init__(self, playerId=clientApi.GetLocalPlayerId()):
        self.__id = playerId

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
        from ..SAPI_C import Screens
        Screens[id(customUI)] = customUI
        clientApi.PushScreen("modsapi", "CustomUI", {"screenId": id(customUI)})

    def popUI(self):
        """remove the top ui"""
        clientApi.PopScreen()

    def _attachUI(self, customUI):
        from ..SAPI_C import Screens
        Screens[id(customUI)] = customUI
        clientApi.CreateUI("modsapi", "CustomUI", {"screenId": id(customUI), "isHud": 1})

