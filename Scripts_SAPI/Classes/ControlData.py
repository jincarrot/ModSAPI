# -*- coding: utf-8 -*-
import copy

class ControlData(object):
    """Base class of all controls"""

    def __init__(self, parentData=None):
        # type: (ControlData) -> None
        self.parent = parentData
        """parent control"""
        self.controls = [] # type: list[ControlData]
        """child controls"""
        self.size = ["100%", "100%"]
        """size of this control"""
        self.controlName = "custom_control"
        """name of this control"""
        self.offset = [0, 0]
        """offset (position) of this control"""

    def __str__(self):
        controlStr = []
        for c in self.controls:
            controlStr.append(str(c))
        data = {
            self.__class__.__name__[:-4:]: controlStr
        }
        return "%s" % data

    def addControl(self, controlData):
        # type: (ControlData) -> None
        """add a new control to current control"""
        if isinstance(controlData, ControlData):
            self.controls.append(controlData)
        else:
            print("param error! Not a control.")

    def removeControl(self, controlData):
        # type: (ControlData) -> bool
        """
        remove a control.

        Returns True if target control exist.
        """
        length = len(self.controls)
        self.controls.remove(controlData)
        return length > len(self.controls)
    
    def _generate(self):
        # type: () -> dict
        """generate data"""
        controls = []
        for control in self.controls:
            controls.append(control._generate())
        data = {
            self.controlName: {
                "type": self.__class__.__name__[:-4:].lower(),
                "controls": controls,
                "size": self.size,
                "offset": self.offset
            }
        }
        return data
    
    def copy(self):
        # type: () -> ControlData
        """Create a copy."""
        newData = copy.deepcopy(self)
        return newData

class PanelData(ControlData):
    """Panel class"""

    def __init__(self, parentData=None):
        ControlData.__init__(self, parentData)

class ImageData(ControlData):
    """Image class"""

    def __init__(self, parentData=None):
        ControlData.__init__(self, parentData)
        self.texture = ""


class ScreenData(object):
    """Screen data"""

    def __init__(self):
        self.controls = [] # type: list[ControlData]
        """child controls"""

    def __str__(self):
        controlStr = []
        for c in self.controls:
            controlStr.append(str(c))
        data = {
            self.__class__.__name__[:-4:]: controlStr
        }
        return "%s" % data

    def addControl(self, controlData):
        # type: (ControlData) -> None
        """add a new control to current control"""
        if isinstance(controlData, ControlData):
            self.controls.append(controlData)
        else:
            print("param error! Not a control.")

    def removeControl(self, controlData):
        # type: (ControlData) -> bool
        """
        remove a control.

        Returns True if target control exist.
        """
        length = len(self.controls)
        self.controls.remove(controlData)
        return length > len(self.controls)
    
    def _generate(self):
        """generate data"""
        controls = []
        for control in self.controls:
            controls.append(control._generate())
        data = {
            "screen": {
                "type": "screen",
                "controls": controls
            }
        }
        return data
    