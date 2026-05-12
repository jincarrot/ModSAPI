# -*- coding: utf-8 -*-
import mod.client.extraClientApi as clientApi

ScreenNode = clientApi.GetScreenNodeCls()

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

    def getScreenNode(self):
        return ScreenNode

    def registerUI(self, identifier, uiDef, uiClass):
        # type: (str, str, str | any) -> None
        """Register a ui."""
        if ":" not in identifier:
            identifier = "modsapi:%s" % identifier
        namespace = identifier.split(":")[0]
        name = identifier.split(":")[1]
        if isinstance(uiClass, str):
            uiClassPath = uiClass
        elif isinstance(uiClass, ScreenNode):
            uiClassPath = "%s.%s" % (uiClass.__module__, uiClass.__name__)
        else:
            raise TypeError("Register UI error! param 'UIClass' should be type str | ScreenNode, but got %s." % uiClass.__class__.__name__)
        clientApi.RegisterUI(namespace, name, uiClassPath, uiDef)

    def pushUI(self, identifier, extraData={}):
        # type: (str, dict) -> None
        """Push a UI to screen."""
        if ":" not in identifier:
            identifier = "modsapi:%s" % identifier
        namespace = identifier.split(":")[0]
        name = identifier.split(":")[1]
        clientApi.PushScreen(namespace, name, extraData)

    def popUI(self):
        """Remove the top ui."""
        clientApi.PopScreen()

    def _attachUI(self, customUI):
        # Screens[id(customUI)] = customUI
        clientApi.CreateUI("modsapi", "CustomUI", {"screenId": id(customUI), "isHud": 1})

