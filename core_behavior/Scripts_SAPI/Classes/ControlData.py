# -*- coding: utf-8 -*-
from ..Utils.Expression import *
import copy
import mod.client.extraClientApi as clientApi

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
            if len(value) != 3:
                print("[Error][ModSAPI][TypeError] 属性 color 长度为3")
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
    
class TraceData(object):

    def __init__(self):
        self.width = 1
        """追踪线条的宽度"""
        self.interval = 1
        """追踪记录的间隔，间隔越大性能越好"""
        self.amount = 50
        """追踪线条数量，数量越小线条越短，性能越好"""
        self.__color = (Expression(255.0), Expression(255.0), Expression(255.0))
        self.__alpha = Expression(1.0)

    @property
    def color(self):
        """线条颜色"""
        return self.__color
    
    @color.setter
    def color(self, value):
        if type(value) in [list, tuple]:
            if len(value) != 3:
                print("[Error][ModSAPI][TypeError] 属性 color 长度为3")
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
                self.__color[0]._change(temp[0])
                self.__color[1]._change(temp[1])
                self.__color[2]._change(temp[2])
        elif type(value) == str:
            if value == 'black':
                self.__color[0]._change(0)
                self.__color[1]._change(0)
                self.__color[2]._change(0)
            elif value == 'white':
                self.__color[0]._change(255)
                self.__color[1]._change(255)
                self.__color[2]._change(255)
        else:
            print("[Error][ModSAPI][TypeError] 属性 color 只接受元组或列表类型值")

    @property
    def alpha(self):
        """线条透明度"""
        return self.__alpha
    
    @alpha.setter
    def alpha(self, value):
        # type: (float) -> None
        if type(value) in [int, float] or isinstance(value, Expression):
            self.__alpha._change(value)
        else:
            print("[Error][ModSAPI][TypeError] 属性 alpha 可接受的值为 float | Expression")

class ControlData(object):
    """Base class of all controls"""

    def __init__(self, parentData=None, inst=None):
        # type: (ControlData, Control) -> None
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
        self.visible = True
        """visibility of this control"""
        self.isStatic = False
        self.shouldTrace = False
        self.inst=inst
        """instance of this control"""

    def __str__(self):
        controlStr = []
        for c in self.controls:
            controlStr.append(str(c))
        data = {
            self.__class__.__name__[:-4:]: controlStr
        }
        return "%s" % data

    @property
    def path(self):
        """控件路径"""
        p = "/%s" % self.controlName
        cur = self
        while(hasattr(cur, "parent") and getattr(cur, "parent")):
            p = ("/%s" % cur.parent.controlName) + p
            cur = cur.parent
        return p
    
    def addControl(self, controlData):
        # type: (ControlData) -> None
        """add a new control to current control"""
        if isinstance(controlData, ControlData):
            self.controls.append(controlData)
            import UI as custom_ui
            custom_ui.RefreshSigns[id(self.inst)] = True
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
                "bg": self.background,
                "visible": self.visible,
                "isStatic": self.isStatic,
                "shouldTrace": self.shouldTrace,
                "path": self.path,
                "instance": self.inst
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

    def __init__(self, parentData=None, inst=None):
        ControlData.__init__(self, parentData, inst)

class ImageData(ControlData):
    """Image class"""

    def __init__(self, parentData=None, inst=None):
        ControlData.__init__(self, parentData, inst)
        self.texture = ""
        self.rotation = Expression(0.0)
        self.color = (Expression(255), Expression(255), Expression(255))
        self.uv_origin = (Expression(0.0), Expression(0.0))
        self.uv_size = (Expression(self.size[0]), Expression(self.size[1]))

    def _generate(self):
        baseData = ControlData._generate(self)
        baseData[self.controlName]['texture'] = self.texture
        baseData[self.controlName]['rotation'] = self.rotation
        baseData[self.controlName]['color'] = self.color
        baseData[self.controlName]['uv'] = self.uv_origin
        baseData[self.controlName]['uv_size'] = self.uv_size
        return baseData

class ScrollPanelData(ControlData):

    def __init__(self, parentData=None, inst=None):
        ControlData.__init__(self, parentData, inst)
        self.content = None # type: PanelData

    def _generate(self):
        baseData = ControlData._generate(self)
        baseData[self.controlName]['content'] = self.content
        return baseData

class ButtonTouchCallbacks:

    def __init__(self):
        from UI import ButtonCallbackArgument
        def default(arg):
            # type: (ButtonCallbackArgument) -> None
            pass
        self.__hoverIn = default
        """鼠标挪入按钮区域时触发函数"""
        self.__hoverOut = default
        """鼠标挪出按钮区域时触发函数"""
        self.__screenExit = default
        """按钮所在画布退出时触发函数"""
        self.__touchCancel = default
        """按下按钮后在按钮区域外抬起时触发函数"""
        self.__touchDown = default
        """按下按钮（未抬起）时触发函数"""
        self.__touchUp = default
        """按下按钮并抬起时触发"""
        self.__touchMove = default
        """手指在按钮区域内挪动时触发"""
        self.__touchMoveIn = default
        """手指挪入按钮区域时触发函数"""
        self.__touchMoveOut = default
        """手指挪出按钮区域时触发函数"""

    @property
    def hoverIn(self):
        """鼠标挪入按钮区域时触发函数"""
        return self.__hoverIn

    @hoverIn.setter
    def hoverIn(self, value):
        if callable(value):
            self.__hoverIn = value
        else:
            print("[Error][ModSAPI][TypeError] 属性 hoverIn 必须为可调用对象")

    @property
    def hoverOut(self):
        """鼠标挪出按钮区域时触发函数"""
        return self.__hoverOut

    @hoverOut.setter
    def hoverOut(self, value):
        if callable(value):
            self.__hoverOut = value
        else:
            print("[Error][ModSAPI][TypeError] 属性 hoverOut 必须为可调用对象")

    @property
    def screenExit(self):
        """按钮所在画布退出时触发函数"""
        return self.__screenExit

    @screenExit.setter
    def screenExit(self, value):
        if callable(value):
            self.__screenExit = value
        else:
            print("[Error][ModSAPI][TypeError] 属性 screenExit 必须为可调用对象")

    @property
    def touchCancel(self):
        """按下按钮后在按钮区域外抬起时触发函数"""
        return self.__touchCancel

    @touchCancel.setter
    def touchCancel(self, value):
        if callable(value):
            self.__touchCancel = value
        else:
            print("[Error][ModSAPI][TypeError] 属性 touchCancel 必须为可调用对象")

    @property
    def touchDown(self):
        """按下按钮（未抬起）时触发函数"""
        return self.__touchDown

    @touchDown.setter
    def touchDown(self, value):
        if callable(value):
            self.__touchDown = value
        else:
            print("[Error][ModSAPI][TypeError] 属性 touchDown 必须为可调用对象")

    @property
    def touchUp(self):
        """按下按钮并抬起时触发"""
        return self.__touchUp

    @touchUp.setter
    def touchUp(self, value):
        if callable(value):
            self.__touchUp = value
        else:
            print("[Error][ModSAPI][TypeError] 属性 touchUp 必须为可调用对象")

    @property
    def touchMove(self):
        """手指在按钮区域内挪动时触发"""
        return self.__touchMove

    @touchMove.setter
    def touchMove(self, value):
        if callable(value):
            self.__touchMove = value
        else:
            print("[Error][ModSAPI][TypeError] 属性 touchMove 必须为可调用对象")

    @property
    def touchMoveIn(self):
        """手指挪入按钮区域时触发函数"""
        return self.__touchMoveIn

    @touchMoveIn.setter
    def touchMoveIn(self, value):
        if callable(value):
            self.__touchMoveIn = value
        else:
            print("[Error][ModSAPI][TypeError] 属性 touchMoveIn 必须为可调用对象")

    @property
    def touchMoveOut(self):
        """手指挪出按钮区域时触发函数"""
        return self.__touchMoveOut

    @touchMoveOut.setter
    def touchMoveOut(self, value):
        if callable(value):
            self.__touchMoveOut = value
        else:
            print("[Error][ModSAPI][TypeError] 属性 touchMoveOut 必须为可调用对象")

class ButtonTextures:

    def __init__(self):
        self.default = ImageData()
        self.default.texture = "textures/netease/common/button/default"
        self.default.controlName = "default"
        self.hover = ImageData()
        self.hover.texture = "textures/netease/common/button/hover"
        self.hover.controlName = "hover"
        self.pressed = ImageData()
        self.pressed.texture = "textures/netease/common/button/pressed"
        self.pressed.controlName = "pressed"

class ButtonData(ControlData):
    """Button class"""

    def __init__(self, parentData=None, buttonInstance=None):
        ControlData.__init__(self, parentData, buttonInstance)
        self.buttonInstance = buttonInstance
        self.callbacks = ButtonTouchCallbacks()
        """按钮回调函数"""
        self.label = LabelData()
        """按钮文本"""
        self.label.controlName = "button_label"
        self.textures = ButtonTextures()
        """按钮贴图"""

    def _generate(self):
        baseData = ControlData._generate(self)
        baseData[self.controlName]['callbacks'] = self.callbacks
        baseData[self.controlName]['label'] = self.label
        baseData[self.controlName]['textures'] = self.textures
        baseData[self.controlName]['base'] = self.buttonInstance
        return baseData
    
class DragableButtonData(ButtonData):
    """Dragable button data"""

    def __init__(self, parentData=None, inst=None):
        ButtonData.__init__(self, parentData, inst)
    
class LabelData(ControlData):
    """Lable class"""

    def __init__(self, parentData=None, inst=None):
        ControlData.__init__(self, parentData, inst)
        self.text = ""
        self.align = "center"
        self.fontSize = Expression(1.0)
        self.linePadding = Expression(0.0)
        self.color = (Expression(255), Expression(255), Expression(255))

    def _generate(self):
        baseData = ControlData._generate(self)
        baseData[self.controlName]['text'] = self.text
        baseData[self.controlName]['align'] = self.align
        baseData[self.controlName]['fontSize'] = self.fontSize
        baseData[self.controlName]['linePadding'] = self.linePadding
        baseData[self.controlName]['color'] = self.color
        return baseData

class ScreenData(object):
    """Screen data"""

    def __init__(self, inst=None):
        self.controls = [] # type: list[ControlData]
        """child controls"""
        size = clientApi.GetEngineCompFactory().CreateGame(clientApi.GetLevelId()).GetScreenSize()
        self.size = [Expression(size[0]), Expression(size[1])]
        self.alpha = Expression(1.0)
        self.background = BackgroundData()
        self.updateCallback = None
        self.controlName = "screen"
        self.inst = inst

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
            import UI as custom_ui
            custom_ui.RefreshSigns[id(self.inst)] = True
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
    