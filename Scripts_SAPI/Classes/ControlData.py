# -*- coding: utf-8 -*-
from ..Utils.Expression import *
import copy

class BackgroundData(object):

    def __init__(self):
        self.__texture = "textures/ui/white_bg"
        self.__color = (Expression(255), Expression(255), Expression(255))
        self.__alpha = Expression(0.0)

    @property
    def texture(self):
        """背景图片，默认为'textures/ui/white_bg'"""
        return self.__texture
    
    @texture.setter
    def texture(self, value):
        # type: (str) -> None
        if type(value) == str:
            self.__texture = value
        else:
            print("[Error][ModSAPI][TypeError] 属性 texture 是字符串类型")

    @property
    def color(self):
        """
        颜色，使用rgb格式，默认为(255, 255, 255)

        支持表达式
        """
        return self.__color
    
    @color.setter
    def color(self, value):
        # type: (tuple[int | Expression] | list[int | Expression]) -> None
        if type(value) in [list, tuple]:
            if len(value) != 2:
                print("[Error][ModSAPI][TypeError] 属性 color 长度为2")
                return
            # process value
            temp = [0, 0, 0]
            for i in range(3):
                if type(value[i]) in [int, float]:
                    temp[i] = value[i]
                elif isinstance(value[i], Expression):
                    temp[i] = value[i]
                else:
                    print("[Error][ModSAPI][TypeError] 属性 color 只接受元素类型为 int | float | Expression 的元组或列表")
                    return
                self.color[0]._change(temp[0])
                self.color[1]._change(temp[1])
                self.color[2]._change(temp[2])
        elif type(value) == str:
            if value == 'black':
                self.color[0]._change(0)
                self.color[1]._change(0)
                self.color[2]._change(0)
            elif value == 'white':
                self.color[0]._change(255)
                self.color[1]._change(255)
                self.color[2]._change(255)
        else:
            print("[Error][ModSAPI][TypeError] 属性 color 只接受元组或列表类型值")

    @property
    def alpha(self):
        """
        透明度，默认为0.0
        
        支持表达式
        """
        return self.__alpha
    
    @alpha.setter
    def alpha(self, value):
        if type(value) in [int, float] or isinstance(value, Expression):
            self.__alpha._change(value)
        else:
            print("[Error][ModSAPI][TypeError] 属性 alpha 可接受的类型为 float | Expression")
    
class ControlData(object):
    """Base class of all controls"""

    def __init__(self, parentData=None):
        # type: (ControlData) -> None
        self.parent = parentData
        """parent control"""
        self.controls = [] # type: list[ControlData]
        """child controls"""
        self.size = [Expression(100), Expression(100)] # type: list[Expression]
        """size of this control"""
        self.controlName = "custom_control"
        """name of this control"""
        self.offset = [Expression(0), Expression(0)] # type: list[Expression]
        """offset (position) of this control"""
        self.anchor = ["center", "center"]
        """anchor of this control. ["from", "to"]"""
        self.alpha = Expression(1.0)
        """alpha of this control."""
        self.background = BackgroundData()
        """background of this control"""

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
                "offset": self.offset,
                "anchor": self.anchor,
                "alpha": self.alpha,
                "bg": self.background
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

    def _generate(self):
        baseData = ControlData._generate(self)
        baseData[self.controlName]['texture'] = self.texture
        return baseData

class LabelData(ControlData):
    """Image class"""

    def __init__(self, parentData=None):
        ControlData.__init__(self, parentData)
        self.text = ""

    def _generate(self):
        baseData = ControlData._generate(self)
        baseData[self.controlName]['text'] = self.text
        return baseData

class ScreenData(object):
    """Screen data"""

    def __init__(self):
        self.controls = [] # type: list[ControlData]
        """child controls"""
        self.size = [Expression(0), Expression(0)]
        self.background = BackgroundData()

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
            print("[Error][ModSAPI] 添加控件失败！")

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
                "controls": controls,
                "bg": self.background
            }
        }
        return data
    