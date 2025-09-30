# -*- coding: utf-8 -*-
import mod.client.extraClientApi as clientApi

from ControlData import *

ScreenNode = clientApi.GetScreenNodeCls()

class _CustomUI(ScreenNode):
    """Custom UI"""

    class Player:
        def showUI(self, ui):
            pass

    def __init__(self, namespace, name, param):
        # type: (str, str, dict) -> None
        ScreenNode.__init__(self, namespace, name, param)
        self.screenData = param['screenData']

    def Create(self):
        # type: () -> None
        pass


class Control(object):
    """Base class of all controls"""

    def __init__(self, parent=None):
        # type: (Control | UI) -> None
        self._controlData = ControlData(parent._controlData)
        self._parent = parent

    @property
    def parent(self):
        # type: () -> Control | UI
        """the parent control"""
        return self._parent

    @property
    def size(self):
        # type: () -> list[int | str]
        """Size of this control."""
        return self._controlData.size
    
    @size.setter
    def size(self, value):
        # type: (list[int | str] | tuple[int | str]) -> None
        if type(value) in [list, tuple] and len(value) == 2:
            self._controlData.size = value
        else:
            print("Set size error! size must be a list or tuple which has two elements.")

    def addPanel(self, panelData={}):
        # type: (dict) -> Panel
        """
        Add a new panel.
        """
        panel = Panel(self)
        self._controlData.addControl(panel._controlData)
        return panel
    
    def addImage(self, imageData={}):
        # type: (dict) -> Image
        """
        Add a new image.
        """
        image = Image(self)
        self._controlData.addControl(image._controlData)
        return image
    
    def addControl(self, control):
        # type: (Control) -> bool
        temp = self
        while temp:
            if id(temp) == id(control):
                print("add control error! cannot add a parent control.")
                return False
            temp = temp.parent if isinstance(temp, Control) else None
        self._controlData.addControl(control._controlData)
        return True

    def copy(self):
        # type: () -> Control
        """Create a copy of this control"""
        newControl = self.__class__(self.parent)
        newControl._controlData = self._controlData.copy()
        return newControl
    
class Panel(Control):
    """Panel class"""

    def __init__(self, parent=None):
        # type: (Control | UI) -> None
        self._controlData = PanelData(parent._controlData if parent else None)
        self._parent = parent

class Image(Control):
    """Image class"""

    def __init__(self, parent=None):
        # type: (Control | UI) -> None
        self._controlData = ImageData(parent._controlData if parent else None)
        self._parent = parent

class UI(object):
    """Custom UI (ModSAPI only)"""

    def __init__(self):
        self._controlData = ScreenData()

    def addPanel(self, panelData={}):
        # type: (dict) -> Panel
        """
        Add a new panel
        """
        panel = Panel(self)
        self._controlData.addControl(panel._controlData)
        return panel
    
    def addImage(self, imageData={}):
        # type: (dict) -> Image
        """
        Add a new image.
        """
        image = Image(self)
        self._controlData.addControl(image._controlData)
        return image
    
    def show(self, player):
        # type: (_CustomUI.Player) -> None
        player.showUI(self)

    def addControl(self, control):
        # type: (Control) -> None
        self._controlData.addControl(control._controlData)
