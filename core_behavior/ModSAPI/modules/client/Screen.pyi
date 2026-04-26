# -*- coding: utf-8 -*-
import mod.client.extraClientApi as clientApi
from ..server_ui.UI import *

class Screen(object):
    "Contains a set of operations about screen."

    @property
    def isHud(self):
        # type: () -> bool
        """Returns true if this screen is a hud screen."""

