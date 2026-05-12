# -*- coding: utf-8 -*-
import mod.client.extraClientApi as clientApi

class Screen(object):
    "Contains a set of operations about screen."

    @property
    def isHud(self):
        # type: () -> bool
        """Returns true if this screen is a hud screen."""

    def getScreenNode(self) -> clientApi.ScreenNode:
        """Gets the ScreenNode class."""

    def registerUI(self, identifier, uiDef, uiClass):
        # type: (str, str, str | any) -> None
        """Register a ui."""

    def pushUI(self, identifier, extraData={}):
        # type: (str, dict) -> None
        """Push a UI to screen."""

    def popUI(self):
        """Remove the top ui."""

