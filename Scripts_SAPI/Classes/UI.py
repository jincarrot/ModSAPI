# -*- coding: utf-8 -*-
import mod.client.extraClientApi as clientApi

from ControlData import *
from ..Utils.Expression import *

ScreenNode = clientApi.GetScreenNodeCls()
ViewBinder = clientApi.GetViewBinderCls()

class Variables(object):

    def __init__(self):
        pass

    @staticmethod
    def ui_age(ui):
        # type: (UI) -> Expression
        """
        The age of this ui from creation, in ticks. (1 second has 30 ticks.)
        
        Returns -1 if this has not been showed.
        """
        return ui.age

v = Variables()


class _CustomUI(ScreenNode):
    """Custom UI"""

    class Player:
        def showUI(self, ui):
            pass

    def __init__(self, namespace, name, param):
        # type: (str, str, dict) -> None
        ScreenNode.__init__(self, namespace, name, param)
        from ..SAPI_C import Screens
        self.ui = Screens.get(param['screenId'], None) # type: UI
        self.screenData = self.ui._controlData._generate()

    @ViewBinder.binding(ViewBinder.BF_ButtonClickUp, '#custom_ui_close')
    def Close(self, __args):
        clientApi.PopScreen()

    def createControl(self, controlData, path="/screen"):
        # type: (dict, str) -> None
        parentControl = self.GetBaseUIControl(path)
        if not parentControl:
            print("Error! Parent control '%s' dosen't exist!" % path)
            return
        controlName = controlData.keys()[0]
        controlData = controlData[controlName]
        controlType = controlData['type']
        c = self.CreateChildControl("base_controls.custom_%s" % controlType, controlName, parentControl)
        bg = self.CreateChildControl("base_controls.background", "custom_ui_background_auto_generate", c).asImage()
        bg.SetSprite(controlData['bg']['texture'])
        bg.SetAlpha(controlData['bg']['alpha'])
        bg.SetSpriteColor((float(controlData['bg']['color'][0]) / 255.0, float(controlData['bg']['color'][1]) / 255.0, float(controlData['bg']['color'][2] / 255.0)))
        c.SetAnchorFrom(controlData['anchor'][0])
        c.SetAnchorTo(controlData['anchor'][1])
        if controlData['controls']:
            for control in controlData['controls']:
                self.createControl(control, path + "/" + controlName)
        if controlType == "image":
            c.asImage().SetSprite(controlData['texture'])

    def Create(self):
        # type: () -> None
        if self.screenData:
            controls = self.screenData['screen']['controls']
            self.GetBaseUIControl("/screen").SetAnchorFrom("center")
            self.GetBaseUIControl("/screen").SetAnchorTo("center")
            # set background style
            bg = self.GetBaseUIControl("/screen/custom_ui_background_auto_generate").asImage()
            bg.SetSprite(self.ui.background.texture)
            bg.SetAlpha(self.ui.background.alpha)
            bg.SetSpriteColor((float(self.ui.background.color[0]) / 255.0, float(self.ui.background.color[1]) / 255.0, float(self.ui.background.color[2] / 255.0)))
            baseSize = self.GetBaseUIControl("/screen").GetSize()
            # get base size
            self.ui.size[0]._change(baseSize[0])
            self.ui.size[1]._change(baseSize[1])
            # create child control
            for control in controls:
                self.createControl(control)

    def Update(self):
        self.ui.age._change(int(self.ui.age + 1))
        if self.screenData:
            basePath = "/screen"
            controls = self.screenData['screen']['controls']
            self.updateControl(basePath, controls)

    def updateControl(self, path, controls):
        # type: (str, list[dict]) -> None
        if controls:
            for control in controls:
                controlName = control.keys()[0]
                controlData = control[controlName]
                c = self.GetBaseUIControl(path + "/" + controlName)
                if not c:
                    return
                if type(controlData['size'][0]) != str:
                    size = (float(controlData['size'][0]), float(controlData['size'][1]))
                    c.SetFullSize("x", {"absoluteValue": size[0]})
                    c.SetFullSize("y", {"absoluteValue": size[1]})
                else:
                    relativeSize = [0, 0]
                    size = [0, 0]
                    ori = controlData['size'] # type: list[str]
                    oriX = ori[0]
                    oriY = ori[1]
                    if "+" in oriX:
                        temp = oriX.split("+")
                        for el in temp:
                            if "%" in el:
                                relativeSize[0] = int(el.split("%")[0])
                            elif "px" in el:
                                size[0] = int(el.split("px")[0])
                    elif "-" in oriX:
                        temp = oriX.split("+")
                        for el in temp:
                            if "%" in el:
                                relativeSize[0] = int(el.split("%")[0])
                            elif "px" in el:
                                size[0] = int(el.split("px")[0])
                    if "+" in oriY:
                        temp = oriX.split("+")
                        for el in temp:
                            if "%" in el:
                                relativeSize[1] = int(el.split("%")[0])
                            elif "px" in el:
                                size[1] = int(el.split("px")[0])
                    elif "-" in oriY:
                        temp = oriX.split("+")
                        for el in temp:
                            if "%" in el:
                                relativeSize[1] = int(el.split("%")[0])
                            elif "px" in el:
                                size[1] = int(el.split("px")[0])
                    c.SetFullSize("x", {"fit": True, "followType": "parent", "absoluteValue": size[0], "relativeValue": relativeSize[0]})
                    c.SetFullSize("y", {"fit": True, "followType": "parent", "absoluteValue": size[1], "relativeValue": relativeSize[1]})
                if type(controlData['offset'][0]) != str:
                    offset = (float(controlData['offset'][0]), float(controlData['offset'][1]))
                    c.SetFullPosition("x", {"absoluteValue": offset[0]})
                    c.SetFullPosition("y", {"absoluteValue": offset[1]})
                else:
                    relativeSize = [0, 0]
                    size = [0, 0]
                    ori = controlData['offset'] # type: list[str]
                    oriX = ori[0]
                    oriY = ori[1]
                    if "+" in oriX:
                        temp = oriX.split("+")
                        for el in temp:
                            if "%" in el:
                                relativeSize[0] = int(el.split("%")[0])
                            elif "px" in el:
                                size[0] = int(el.split("px")[0])
                    elif "-" in oriX:
                        temp = oriX.split("+")
                        for el in temp:
                            if "%" in el:
                                relativeSize[0] = int(el.split("%")[0])
                            elif "px" in el:
                                size[0] = int(el.split("px")[0])
                    if "+" in oriY:
                        temp = oriX.split("+")
                        for el in temp:
                            if "%" in el:
                                relativeSize[1] = int(el.split("%")[0])
                            elif "px" in el:
                                size[1] = int(el.split("px")[0])
                    elif "-" in oriY:
                        temp = oriX.split("+")
                        for el in temp:
                            if "%" in el:
                                relativeSize[1] = int(el.split("%")[0])
                            elif "px" in el:
                                size[1] = int(el.split("px")[0])
                    c.SetFullPosition("x", {"fit": True, "followType": "parent", "absoluteValue": size[0], "relativeValue": relativeSize[0]})
                    c.SetFullPosition("y", {"fit": True, "followType": "parent", "absoluteValue": size[1], "relativeValue": relativeSize[1]})

                alpha = controlData['alpha']
                c.SetAlpha(float(alpha))
                self.updateControl(path + "/" + controlName, controlData['controls'])

    def Destroy(self):
        self.ui.age._change(-1)


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
        """
        控件尺寸
        
        支持表达式
        """
        return self._controlData.size
    
    @size.setter
    def size(self, value):
        # type: (list[int | str] | tuple[int | str]) -> None
        if type(value) in [list, tuple] and len(value) == 2:
            # if value is str, switch to expression.
            if type(value[0]) == str:
                if type(value[1]) == str:
                    relativeSize = [0, 0]
                    size = [0, 0]
                    oriX = value[0]
                    oriY = value[1]
                    # cauculate the value
                    if "+" in oriX:
                        temp = oriX.split("+")
                        for el in temp:
                            if "%" in el:
                                relativeSize[0] = int(el.split("%")[0])
                            elif "px" in el:
                                size[0] = int(el.split("px")[0])
                    elif "-" in oriX:
                        temp = oriX.split("+")
                        for el in temp:
                            if "%" in el:
                                relativeSize[0] = int(el.split("%")[0])
                            elif "px" in el:
                                size[0] = int(el.split("px")[0])
                    else:
                        if "%" in oriX:
                            relativeSize[0] = int(oriX.split("%")[0])
                        elif "px" in oriX:
                            size[0] = int(oriX.split("px")[0])
                    if "+" in oriY:
                        temp = oriX.split("+")
                        for el in temp:
                            if "%" in el:
                                relativeSize[1] = int(el.split("%")[0])
                            elif "px" in el:
                                size[1] = int(el.split("px")[0])
                    elif "-" in oriY:
                        temp = oriX.split("+")
                        for el in temp:
                            if "%" in el:
                                relativeSize[1] = int(el.split("%")[0])
                            elif "px" in el:
                                size[1] = int(el.split("px")[0])
                    else:
                        if "%" in oriY:
                            relativeSize[0] = int(oriY.split("%")[0])
                        elif "px" in oriY:
                            size[0] = int(oriY.split("px")[0])
                    # set value
                    if self.parent:
                        value = [relativeSize[0] / 100.0 * self.parent.size[0] + size[0], relativeSize[0] / 100.0 * self.parent.size[0] + size[0]]
            self._controlData.size[0]._change(value[0])
            self._controlData.size[1]._change(value[1])
        else:
            print("Set size error! size must be a list or tuple which has two elements.")

    @property
    def name(self):
        """控件名称"""
        return self._controlData.controlName
    
    @name.setter
    def name(self, value):
        self._controlData.controlName = value
    
    @property
    def offset(self):
        """
        控件位移（位置）
        
        支持表达式"""
        return self._controlData.offset
    
    @offset.setter
    def offset(self, value):
        # type: (list[int | str] | tuple[int | str]) -> None
        if type(value) in [list, tuple] and len(value) == 2:
            # if value is str, switch to expression.
            if type(value[0]) == str:
                if type(value[1]) == str:
                    relativeSize = [0, 0]
                    size = [0, 0]
                    oriX = value[0]
                    oriY = value[1]
                    # cauculate the value
                    if "+" in oriX:
                        temp = oriX.split("+")
                        for el in temp:
                            if "%" in el:
                                relativeSize[0] = int(el.split("%")[0])
                            elif "px" in el:
                                size[0] = int(el.split("px")[0])
                    elif "-" in oriX:
                        temp = oriX.split("+")
                        for el in temp:
                            if "%" in el:
                                relativeSize[0] = int(el.split("%")[0])
                            elif "px" in el:
                                size[0] = int(el.split("px")[0])
                    else:
                        if "%" in oriX:
                            relativeSize[0] = int(oriX.split("%")[0])
                        elif "px" in oriX:
                            size[0] = int(oriX.split("px")[0])
                    if "+" in oriY:
                        temp = oriX.split("+")
                        for el in temp:
                            if "%" in el:
                                relativeSize[1] = int(el.split("%")[0])
                            elif "px" in el:
                                size[1] = int(el.split("px")[0])
                    elif "-" in oriY:
                        temp = oriX.split("+")
                        for el in temp:
                            if "%" in el:
                                relativeSize[1] = int(el.split("%")[0])
                            elif "px" in el:
                                size[1] = int(el.split("px")[0])
                    else:
                        if "%" in oriY:
                            relativeSize[0] = int(oriY.split("%")[0])
                        elif "px" in oriY:
                            size[0] = int(oriY.split("px")[0])
                    # set value
                    if self.parent:
                        value = [relativeSize[0] / 100.0 * self.parent.size[0] + size[0], relativeSize[0] / 100.0 * self.parent.size[0] + size[0]]
            self._controlData.offset[0]._change(value[0])
            self._controlData.offset[1]._change(value[1])
        else:
            print("Set offset error! offset must be a list or tuple which has two elements.")

    @property
    def anchor(self):
        """
        控件锚点

        存储一个列表，0为父控件锚点（anchorFrom）,1为自身锚点（anchorTo）
        """
        return self._controlData.anchor
    
    @anchor.setter
    def anchor(self, value):
        if type(value) in [list, tuple] and len(value) == 2 and type(value[0]) == str and type(value[1]) == str:
            self._controlData.anchor = value
        else:
            print("Set anchor error! anchor must be a list or tuple which has two elements.")

    @property
    def alpha(self):
        """
        控件透明度
        
        支持表达式"""
        return self._controlData.alpha
    
    @alpha.setter
    def alpha(self, value):
        # type: (float) -> None
        if type(value) == float or isinstance(value, Expression):
            self._controlData.alpha._change(value)
        else:
            print("[Error][ModSAPI][TypeError] 属性 alpha 可接受的值为 float | Expression")
    
    @property
    def background(self):
        # type: () -> Image
        return self._controlData.background
    
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
    
    def refresh(self):
        """刷新控件，重新生成子控件，计算值等"""
        pass
    
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

    @property
    def texture(self):
        """Texture path of this image."""
        return self._controlData.texture
    
    @texture.setter
    def texture(self, value):
        # type: (str) -> None
        self._controlData.texture = value

class Label(Control):
    """label class."""
    
    def __init__(self, parent=None):
        # type: (Control | UI) -> None
        self._controlData = LabelData(parent._controlData if parent else None)
        self._parent = parent

    @property
    def text(self):
        """Content of this label."""
        return self._controlData.text
    
    @text.setter
    def text(self, value):
        # type: (str) -> None
        self._controlData.text = value


class UI(object):
    """Custom UI (ModSAPI only)"""

    def __init__(self):
        self._controlData = ScreenData()
        self.__age = Expression(-1)

    @property
    def age(self):
        # type: () -> Expression
        """
        UI寿命(从弹出界面开始),单位: tick(1秒30tick)

        未弹出界面时返回-1

        支持表达式
        """
        return self.__age

    @property
    def size(self):
        """
        屏幕尺寸，仅已弹出的界面可以获取值，未弹出的为0
        
        手动设置无效
        
        支持表达式"""
        return self._controlData.size
    
    @size.setter
    def size(self, value):
        self._controlData.size = value

    @property
    def background(self):
        """背景数据"""
        return self._controlData.background
    
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
