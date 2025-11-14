# -*- coding: utf-8 -*-
import random
import mod.client.extraClientApi as clientApi
# from mod.client.ui.controls.baseUIControl import *
import types

from ControlData import *
from ..Interfaces.Vector import Vector2
from ..Utils.Expression import *

ScreenNode = clientApi.GetScreenNodeCls()
ViewBinder = clientApi.GetViewBinderCls()
CComp = clientApi.GetEngineCompFactory()

RefreshSigns = {}

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


class ButtonCallbackManager:

    def __init__(self, button, ui, callbacks):
        # type: (Button, UI, ButtonTouchCallbacks) -> None
        self.arg = ButtonCallbackArgument(button, ui)
        self.callbacks = callbacks

    def onTouchUp(self, data):
        self.arg.pos = Vector2((data['TouchPosX'], data['TouchPosY']))
        self.callbacks.touchUp(self.arg)

    def onTouchDown(self, data):
        self.arg.pos = Vector2((data['TouchPosX'], data['TouchPosY']))
        self.callbacks.touchDown(self.arg)

    def onMoveIn(self, data):
        self.arg.pos = Vector2((data['TouchPosX'], data['TouchPosY']))
        self.callbacks.touchMoveIn(self.arg)

    def onMove(self, data):
        self.arg.pos = Vector2((data['TouchPosX'], data['TouchPosY']))
        self.callbacks.touchMove(self.arg)

    def onMoveOut(self, data):
        self.arg.pos = Vector2((data['TouchPosX'], data['TouchPosY']))
        self.callbacks.touchMoveOut(self.arg)

    def onScreenExit(self, data):
        self.arg.pos = Vector2((data['TouchPosX'], data['TouchPosY']))
        self.callbacks.screenExit(self.arg)

    def onTouchCancel(self, data):
        self.arg.pos = Vector2((data['TouchPosX'], data['TouchPosY']))
        self.callbacks.touchCancel(self.arg)

    def onHoverIn(self, data):
        self.arg.pos = Vector2((data['TouchPosX'], data['TouchPosY']))
        self.callbacks.hoverIn(self.arg)

    def onHoverOut(self, data):
        self.arg.pos = Vector2((data['TouchPosX'], data['TouchPosY']))
        self.callbacks.hoverOut(self.arg)


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
        self.buttonCallbackManagers = {}
        self.drawingData = {}
        self.traceData = {}

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
        data = controlData[controlName]
        if not data:
            return
        controlType = data['type']
        c = self.CreateChildControl("base_controls.custom_%s" % controlType, controlName, parentControl)
        bg = self.CreateChildControl("base_controls.background", "custom_ui_background_auto_generate", c).asImage()
        bg.SetSprite(data['bg'].texture)
        bg.SetAlpha(float(data['bg'].alpha))
        # bg.SetSpriteColor(data['bg'].color)
        bg.SetLayer(0)
        if not c:
            return
        if type(data['size'][0]) != str:
            size = (float(data['size'][0]), float(data['size'][1]))
            c.SetFullSize("x", {"absoluteValue": size[0]})
            c.SetFullSize("y", {"absoluteValue": size[1]})
        else:
            relativeSize = [0, 0]
            size = [0, 0]
            ori = data['size'] # type: list[str]
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
        if type(data['offset'][0]) != str:
            offset = (float(data['offset'][0]), float(data['offset'][1]))
            c.SetFullPosition("x", {"absoluteValue": offset[0]})
            c.SetFullPosition("y", {"absoluteValue": offset[1]})
        else:
            relativeSize = [0, 0]
            size = [0, 0]
            ori = data['offset'] # type: list[str]
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

        c.SetAnchorFrom(data['anchor'][0])
        c.SetAnchorTo(data['anchor'][1])
        alpha = data['alpha']
        c.SetAlpha(float(alpha))
        c.SetVisible(data['visible'])
        if controlType == "image":
            c.asImage().SetSprite(data['texture'])
        elif controlType == 'label':
            c.asLabel().SetText(data['text'])
        elif controlType == 'button':
            button = c.asButton()
            callbackManager = ButtonCallbackManager(data['base'], self.ui, data['callbacks'])
            self.buttonCallbackManagers[data['path']] = callbackManager
            button.AddTouchEventParams({"isSwallow": True})
            button.AddHoverEventParams({"isSwallow": True})
            button.SetButtonHoverInCallback(callbackManager.onHoverIn)
            button.SetButtonHoverOutCallback(callbackManager.onHoverOut)
            button.SetButtonTouchMoveInCallback(callbackManager.onMoveIn)
            button.SetButtonTouchMoveOutCallback(callbackManager.onMoveOut)
            button.SetButtonTouchMoveCallback(callbackManager.onMove)
            button.SetButtonScreenExitCallback(callbackManager.onScreenExit)
            button.SetButtonTouchCancelCallback(callbackManager.onTouchCancel)
            button.SetButtonTouchDownCallback(callbackManager.onTouchDown)
            button.SetButtonTouchUpCallback(callbackManager.onTouchUp)
            Data = []
            Data.append(data['textures'].default._generate())
            Data.append(data['textures'].hover._generate())
            Data.append(data['textures'].pressed._generate())
            Data.append(data['label']._generate())
            self.updateControl(path + "/" + controlName, Data)
        if data['isStatic']:
            controlData[controlName] = None
            return
        if data['controls']:
            for control in data['controls']:
                self.createControl(control, path + "/" + controlName)

    def Create(self):
        # type: () -> None
        if self.screenData:
            controls = self.screenData['screen']['controls']
            self.GetBaseUIControl("/screen").SetAnchorFrom("center")
            self.GetBaseUIControl("/screen").SetAnchorTo("center")
            # set background style
            bg = self.GetBaseUIControl("/screen/custom_ui_background_auto_generate").asImage()
            bg.SetSprite(self.ui.background.texture)
            bg.SetAlpha(float(self.ui.background.alpha))
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
        if self.ui._controlData.updateCallback:
            self.ui._controlData.updateCallback(self)
        if self.drawingData:
            for key in self.drawingData:
                data = self.drawingData[key]
                for p in data['lst']:
                    alpha = float(data['params']['alpha']) * float(data['parent']['alpha'])
                    color = data['params']['color']
                    c = self.GetBaseUIControl(p).asImage()
                    c.SetAlpha(alpha if 0 <= alpha <= 1 else (1 if alpha > 1 else 0))
                    c.SetSpriteColor((float(color[0] if 0 <= float(color[0]) <= 255 else (255 if float(color[0]) > 255 else 0)) / 255.0, float(color[1] if 0 <= float(color[1]) <= 255 else (1 if float(color[1]) > 255 else 0)) / 255.0, float(color[2] if 0 <= float(color[2]) <= 255 else (1 if float(color[2]) > 255 else 0)) / 255.0))
        if self.screenData:
            basePath = "/screen"
            controls = self.screenData['screen']['controls']
            self.updateControl(basePath, controls)
            bg = self.GetBaseUIControl("/screen/custom_ui_background_auto_generate")
            if bg:
                bg = bg.asImage()
                alpha = float(self.ui.background.alpha)
                color = self.ui.background.color
                bg.SetAlpha(alpha if 0 <= alpha <= 1 else (1 if alpha > 1 else 0))
                bg.SetSpriteColor((float(color[0] if 0 <= int(color[0]) <= 255 else 1 if int(color[0]) > 255 else 0) / 255.0, float(color[1] if 0 <= int(color[1]) <= 255 else 1 if int(color[1]) > 255 else 0) / 255.0, float(color[2] if 0 <= int(color[2]) <= 255 else 1 if int(color[2]) > 255 else 0)/ 255.0))
        if RefreshSigns.get(id(self.ui), 0):
            RefreshSigns[id(self.ui)] = 0
            newData = self.ui._controlData._generate()
            controls = newData['screen']['controls']
            for control in controls:
                if control not in self.screenData['screen']['controls']:
                    self.createControl(control)
            for control in self.screenData['screen']['controls']:
                if control not in controls:
                    self.RemoveChildControl(self.GetBaseUIControl("/screen/%s" % control.keys()[0]))
            self.screenData = newData

    def updateControl(self, path, controls):
        # type: (str, list[dict]) -> None
        if controls:
            for control in controls:
                controlName = control.keys()[0]
                controlData = control[controlName]
                if not controlData:
                    return
                c = self.GetBaseUIControl(path + "/" + controlName)
                if not c:
                    return
                controlType = controlData['type']
                if controlData['shouldTrace']:
                    self.draw(c, controlData)
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

                alpha = float(controlData['alpha'])
                c.SetAlpha(alpha if 0 <= alpha <= 1 else (1 if alpha > 1 else 0))
                c.SetVisible(controlData['visible'])
                if c.GetChildByName("custom_ui_background_auto_generate"):
                    bg = c.GetChildByName("custom_ui_background_auto_generate").asImage()
                    bg.SetSpriteColor((float(controlData['bg'].color[0]) / 255.0, float(controlData['bg'].color[1]) / 255.0, float(controlData['bg'].color[2] / 255.0)))
                    bg.SetAlpha(float(controlData['bg'].alpha))
                if controlType == 'button':
                    data = []
                    data.append(controlData['textures'].default._generate())
                    data.append(controlData['textures'].hover._generate())
                    data.append(controlData['textures'].pressed._generate())
                    data.append(controlData['label']._generate())
                    self.updateControl(path + "/" + controlName, data)
                if controlType == 'label':
                    c.asLabel().SetText(controlData['text'])
                self.updateControl(path + "/" + controlName, controlData['controls'])

    def draw(self, control, controlData):
        # type: (BaseUIControl, dict) -> None
        params = controlData['shouldTrace']
        if float(self.ui.age % params['interval']):
            return
        if not self.drawingData.get(control.GetPath(), None):
            self.drawingData[control.GetPath()] = {
                "expression": controlData['offset'],
                "params": params,
                "parent": {
                    "alpha": controlData['alpha']
                },
                "lst": []
            }
        else:
            name = '%s_p:%s' % (control.GetPath().split("/")[-1], int(self.ui.age))
            def dist(old, new):
                return math.sqrt((old[0] - new[0]) * (old[0] - new[0]) + (old[1] - new[1]) * (old[1] - new[1]))
            line = self.CreateChildControl("base_controls.background", name, self.GetBaseUIControl("/screen")).asImage()
            self.ui.age._change(float(self.ui.age) - params['interval'])
            oldPos = (self.drawingData[control.GetPath()]['expression'][0].staticValue, self.drawingData[control.GetPath()]['expression'][1].staticValue)
            self.ui.age._change(float(self.ui.age) + params['interval'])
            newPos = (self.drawingData[control.GetPath()]['expression'][0].staticValue, self.drawingData[control.GetPath()]['expression'][1].staticValue)
            line.SetFullSize("y", {"fit": False, "followType": "parent", "absoluteValue": params['width']})
            line.SetFullSize("x", {"fit": False, "followType": "parent", "absoluteValue": dist(oldPos, newPos)})
            line.SetFullPosition("x", {"fit": False, "followType": "none", "absoluteValue": (oldPos[0] + newPos[0]) / 2.0})
            line.SetFullPosition("y", {"fit": False, "followType": "none", "absoluteValue": (oldPos[1] + newPos[1]) / 2.0})
            if dist(oldPos, newPos):
                line.Rotate(math.asin((newPos[1] - oldPos[1]) / dist(oldPos, newPos)) * 180.0 / math.pi * (-1 if newPos[0] > oldPos[0] else 1))
            line.SetAlpha(params['alpha'])
            line.SetSpriteColor(params['color'])
            line.SetLayer(0)
            self.drawingData[control.GetPath()]['lst'].append("/screen/%s" % name)
            if len(self.drawingData[control.GetPath()]['lst']) > params['maxAmount']:
                path = self.drawingData[control.GetPath()]['lst'][0]
                self.RemoveChildControl(self.GetBaseUIControl(path))
                self.drawingData[control.GetPath()]['lst'].remove(path)

    def Destroy(self):
        self.ui.age._change(-1)


class Control(object):
    """控件基类"""

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
        panel.name = "panel%s" % random.randint(0, 2147483648)
        self._controlData.addControl(panel._controlData)
        return panel
    
    def addImage(self, imageData={}):
        # type: (dict) -> Image
        """
        Add a new image.
        """
        image = Image(self)
        image.name = "image%s" % random.randint(0, 2147483648)
        self._controlData.addControl(image._controlData)
        return image
    
    def addLabel(self, labelData={}):
        # type: (dict) -> Label
        """添加文本控件"""
        label = Label(self)
        label.name = "label%s" % random.randint(0, 2147483648)
        self._controlData.addControl(label._controlData)
        return label
    
    def addButton(self, buttonData={}):
        # type: (dict) -> Button
        """添加文本控件"""
        button = Button(self)
        button.name = "button%s" % random.randint(0, 2147483648)
        self._controlData.addControl(button._controlData)
        return button
    
    def addControl(self, control):
        # type: (Control) -> bool
        temp = self
        while temp:
            if id(temp) == control.GetPath():
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
    
    def __refresh(self):
        """刷新控件，重新生成子控件，计算值等"""
        pass

    def trace(self, interval=1, maxAmount=50, width=2, alpha=1, color=(1, 1, 1)):
        # type: (int, int, int, int, tuple) -> None
        """记录轨迹"""
        self._controlData.shouldTrace = {"interval": interval, "maxAmount": maxAmount, "width": width, "alpha": alpha, "color": color}
    
    def asStaticControl(self):
        """将此控件作为静态控件，即不会更新size等表达式。主要用于降低性能消耗。"""
        self._controlData.isStatic = True

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

class Button(Control):
    """button class."""
    
    def __init__(self, parent=None):
        # type: (Control | UI) -> None
        self._controlData = ButtonData(parent._controlData if parent else None, self)
        self._parent = parent

    @property
    def callbacks(self):
        """按钮回调函数"""
        return self._controlData.callbacks
    
    @property
    def textures(self):
        """贴图集"""
        return self._controlData.textures
    
    @property
    def label(self):
        """文本"""
        return self._controlData.label
    
class DragableButton(Button):
    """dragable button class."""
    
    def __init__(self, parent=None):
        # type: (Control | UI) -> None
        self._controlData = DragableButtonData(parent._controlData if parent else None, self)
        self._parent = parent


class ButtonCallbackArgument(object):
    """按钮回调函数参数"""

    def __init__(self, button, ui, pos=(0, 0)):
        # type: (Button, UI, tuple) -> None
        self.button = button
        self.ui = ui
        self.pos = Vector2(pos)


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
        Add a new panel.
        """
        panel = Panel(self)
        panel.name = "panel%s" % random.randint(0, 2147483648)
        self._controlData.addControl(panel._controlData)
        return panel
    
    def addImage(self, imageData={}):
        # type: (dict) -> Image
        """
        Add a new image.
        """
        image = Image(self)
        image.name = "image%s" % random.randint(0, 2147483648)
        self._controlData.addControl(image._controlData)
        return image
    
    def addLabel(self, labelData={}):
        # type: (dict) -> Label
        """添加文本控件"""
        label = Label(self)
        label.name = "label%s" % random.randint(0, 2147483648)
        self._controlData.addControl(label._controlData)
        return label
    
    def addButton(self, buttonData={}):
        # type: (dict) -> Button
        """添加文本控件"""
        button = Button(self)
        button.name = "button%s" % random.randint(0, 2147483648)
        self._controlData.addControl(button._controlData)
        return button
    
    def show(self):
        # type: () -> None
        from ..SAPI_C import Screens
        Screens[id(self)] = self
        clientApi.PushScreen("modsapi", "CustomUI", {"screenId": id(self)})

    def addControl(self, control):
        # type: (Control) -> None
        self._controlData.addControl(control._controlData)

    def onUpdate(self, callback):
        # type: (types.FunctionType) -> None
        """设置界面刷新时要执行的函数"""
        self._controlData.updateCallback = callback

    def __refresh(self):
        RefreshSigns[id(self)] = 1


class ScreenUI(UI):

    def __init__(self):
        self._controlData = ScreenData()
        self.__age = Expression(-1)
        UI.__init__(self)

    @property
    def age(self):
        # type: () -> Expression
        """
        UI寿命(从弹出界面开始),单位: tick(1秒30tick)

        未弹出界面时返回-1

        支持表达式
        """
        return self.__age

