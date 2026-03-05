# -*- coding: utf-8 -*-
import mod.client.extraClientApi as clientApi

ScreenNode = clientApi.GetScreenNodeCls()
ViewBinder = clientApi.GetViewBinderCls()

class ActionForm(ScreenNode):
    """Action Form from SAPI"""

    def __init__(self, namespace, name, param):
        # type: (str, str, dict) -> None
        ScreenNode.__init__(self, namespace, name, param)
        self.data = param or {
            "title": "vanilla",
            "body": "example",
            "button": [
                ["button1", "textures/ui/achievements"],
                ["button2", None]
            ]
        }
        """contains a set of button's data.
        
        for example: {
            "title": "vanilla",
            "body": "example",
            "button": {
                "button1": "textures/ui/example"
                "button2": None
            }
        }"""
        self.buttons_panel = None
        """the panel of dynamic buttons"""
        self.BUTTON_PANEL_TOUCH = "/panel/panel_indent/inside_header_panel/scrolling_panel/scroll_touch/scroll_view/panel/background_and_viewport/scrolling_view_port/scrolling_content/wrapping_panel/long_form_dynamic_buttons_panel"
        """the path of the buttons' panel when input mode is 'touch'"""
        self.BUTTON_PANEL_MOUSE = "/panel/panel_indent/inside_header_panel/scrolling_panel/scroll_mouse/scroll_view/stack_panel/background_and_viewport/scrolling_view_port/scrolling_content/wrapping_panel/long_form_dynamic_buttons_panel"
        """the path of the buttons' panel when input mode is 'mouse'"""
        self.BODY_LABEL_TOUCH = "/panel/panel_indent/inside_header_panel/scrolling_panel/scroll_touch/scroll_view/panel/background_and_viewport/scrolling_view_port/scrolling_content/label_offset_panel/main_label"
        """the path of the buttons' panel when input mode is 'touch'"""
        self.BODY_LABEL_MOUSE = "/panel/panel_indent/inside_header_panel/scrolling_panel/scroll_mouse/scroll_view/stack_panel/background_and_viewport/scrolling_view_port/scrolling_content/label_offset_panel/main_label"
        """the path of the buttons' panel when input mode is 'mouse'"""
        self.mode = "touch"
        """input mode"""
        if not param:
            param = {}
        self.ID = param['formId'] if 'formId' in param else 0
        """special id"""
        self.refreshId = None

    def Create(self):
        # type: () -> None
        # buttons' panel, contains a set of buttons, each of them has a image and a button
        # get the panel by switch
        self.buttons_panel = self.GetBaseUIControl(self.BUTTON_PANEL_TOUCH)
        if not self.buttons_panel:
            self.mode = "mouse"
            self.buttons_panel = self.GetBaseUIControl(self.BUTTON_PANEL_MOUSE)
        path = self.BUTTON_PANEL_MOUSE if self.mode == 'mouse' else self.BUTTON_PANEL_TOUCH
        # set form title
        self.GetBaseUIControl("/panel/title_label/common_dialogs_0").asLabel().SetText(self.data['title'])
        # set body label
        self.GetBaseUIControl(self.BODY_LABEL_TOUCH if self.mode == 'touch' else self.BODY_LABEL_MOUSE).asLabel().SetText(self.data['body'])
        # add callback of close button
        close = self.GetBaseUIControl("/panel/common_panel/close_button_holder/close").asButton()
        close.AddTouchEventParams({"isSwallow": True})
        close.SetButtonTouchUpCallback(self.onClose)
        # create buttons by data
        buttonId = 0
        for buttonData in self.data['button']:
            # create a new button
            self.CreateChildControl("server_form.dynamic_button", "dynamic_button%s" % buttonId, self.GetBaseUIControl(path))
            # self.Clone("%s/dynamic_button" % path, path, "dynamic_button%s" % buttonId)
            current = self.GetBaseUIControl("%s/dynamic_button%s" % (path, buttonId))
            current.GetChildByPath('/form_button').asButton().AddTouchEventParams({"isSwallow": True})
            current.GetChildByPath('/form_button').asButton().SetButtonTouchUpCallback(self.onTouch)
            # set button's label
            for state in ['default', 'hover', 'pressed']:
                current.GetChildByPath("/form_button/%s/button_content/common_buttons.new_ui_binding_button_label" % state).asLabel().SetText(buttonData[0])
            # set button's image
            if buttonData[1]:
                current.GetChildByPath("/panel_name/image").asImage().SetSprite(buttonData[1])
            # remove component and fit
            else:
                self.RemoveComponent("%s/dynamic_button%s/panel_name" % (path, buttonId), "%s/dynamic_button%s" % (path, buttonId))
                current.GetChildByPath('/form_button').SetFullSize("x", {"followType": "parent", "relativeValue": 1})
            buttonId += 1
        # remove the default button
        # self.RemoveComponent("%s/dynamic_button" % path, path)
        #self.refreshId = clientApi.GetEngineCompFactory().CreateGame(clientApi.GetLevelId()).AddRepeatedTimer(0.2, self.refreshImage)

    def refreshImage(self):
        # refresh button's image
        path = self.BUTTON_PANEL_MOUSE if self.mode == 'mouse' else self.BUTTON_PANEL_TOUCH
        buttonId = 0
        for buttonData in self.data['button']:
            current = self.GetBaseUIControl("%s/dynamic_button%s" % (path, buttonId))
            # set button's image
            if buttonData[1]:
                current.GetChildByPath("/panel_name/image").asImage().SetSprite(buttonData[1])
                current.GetChildByPath("/panel_name/progress").SetVisible(False)
            buttonId += 1

    def onTouch(self, data):
        clientApi.GetSystem("SAPI", "SAPI_C").NotifyToServer("ActionFormResponse", {"id": self.ID, "playerId": clientApi.GetLocalPlayerId(), "buttonId": int(data['ButtonPath'][-13]), "canceled": False})
        clientApi.PopScreen()
        clientApi.GetEngineCompFactory().CreateGame(clientApi.GetLevelId()).CancelTimer(self.refreshId)

    def onClose(self, __data):
        clientApi.GetSystem("SAPI", "SAPI_C").NotifyToServer("ActionFormResponse", {"id": self.ID, "playerId": clientApi.GetLocalPlayerId(), "buttonId": -1, "canceled": True})
        clientApi.PopScreen()
        clientApi.GetEngineCompFactory().CreateGame(clientApi.GetLevelId()).CancelTimer(self.refreshId)

class ModalForm(ScreenNode):
    """Modal Form from SAPI"""

    def __init__(self, namespace, name, param):
        # type: (str, str, dict) -> None
        ScreenNode.__init__(self, namespace, name, param)
        self.MAIN_PANEL_MOUSE = "/panel/panel_indent/inside_header_panel/scroll_mouse/scroll_view/stack_panel/background_and_viewport/scrolling_view_port/scrolling_content"
        """path of main panel (mouse mode)"""
        self.MAIN_PANEL_TOUCH = "/panel/panel_indent/inside_header_panel/scroll_touch/scroll_view/panel/background_and_viewport/scrolling_view_port/scrolling_content"
        """path of main panel (touch mode)"""
        self.mode = "touch"
        """input mode"""
        self.data = param or {
            "title": "vanilla",
            "elements": [
                {
                    "type": "step_slider",
                    "label": "custom slider"
                },
                {
                    "type": "input",
                    "label": "custom text field"
                },
                {
                    "type": "toggle",
                    "label": "custom toggle"
                }
            ]
        }
        """contains a set of data"""
        self.main_panel = None
        self.ID = param['formId'] if 'formId' in param else 0

    def Create(self):
        # get the input mode
        self.main_panel = self.GetBaseUIControl(self.MAIN_PANEL_TOUCH)
        path = self.MAIN_PANEL_TOUCH
        if not self.main_panel:
            self.main_panel = self.GetBaseUIControl(self.MAIN_PANEL_MOUSE)
            self.mode = "mouse"
            path = self.MAIN_PANEL_MOUSE
        # set the title
        self.GetBaseUIControl("/panel/title_label/common_dialogs_0").asLabel().SetText(self.data['title'])
        # read data and generate ui
        els = self.data['elements']
        LABEL_PATH = "/option_generic_core/two_line_layout/option_label_panel/option_label"
        LABEL_PATH_DROPDOWN = "/dropdown/option_generic_core/two_line_layout/option_label_panel/option_label"
        LABEL_PATH_ONELINE = "/option_generic_core/one_line_layout/option_label"
        for id in range(0, len(els)):
            typeId = els[id]['type']
            self.CreateChildControl("server_form.custom_%s" % typeId, "%s" % id, self.main_panel)
            self.GetBaseUIControl(path + "/%s" % id + (LABEL_PATH_ONELINE if typeId == 'toggle' else ( LABEL_PATH_DROPDOWN if typeId =='dropdown' else LABEL_PATH))).asLabel().SetText(els[id]['label'])
        # refresh the submit button
        self.Clone(path + "/submit_button", path, "submit")
        self.RemoveComponent(path + "/submit_button", path)
        submit = self.GetBaseUIControl(path + '/submit').asButton()
        submit.AddTouchEventParams({"isSwallow": True})
        submit.SetButtonTouchUpCallback(self.submit)
        close = self.GetBaseUIControl("/panel/common_panel/close_button_holder/close").asButton()
        close.AddTouchEventParams({"isSwallow": True})
        close.SetButtonTouchUpCallback(self.onClose)
        for state in ['default', 'hover', 'pressed']:
                self.GetBaseUIControl(path + "/submit/%s/button_content/common_buttons.new_ui_binding_button_label" % state).asLabel().SetText("确定")

    def submit(self, data):
        SLIDER_PATH = "/option_generic_core/two_line_layout/settings_common.option_slider_control/slider"
        TOGGLE_PATH = "/option_generic_core/one_line_layout/settings_common.option_toggle_control"
        TEXT_EDIT_PATH = "/option_generic_core/two_line_layout/settings_common.option_text_edit_control"
        els = self.data['elements']
        path = self.MAIN_PANEL_TOUCH if self.mode == 'touch' else self.MAIN_PANEL_MOUSE
        values = []
        for id in range(0, len(els)):
            if els[id]['type'] == 'toggle':
                values.append(self.GetBaseUIControl(path + '/%s%s/checked' % (id, TOGGLE_PATH)).GetVisible())
            elif els[id]['type'] == 'step_slider':
                values.append(self.GetBaseUIControl(path + '/%s%s' % (id, SLIDER_PATH)).asSlider().GetSliderValue())
            elif els[id]['type'] == 'input':
                values.append(self.GetBaseUIControl(path + '/%s%s' % (id, TEXT_EDIT_PATH)).asTextEditBox().GetEditText())
        clientApi.GetSystem("SAPI", "SAPI_C").NotifyToServer("ModalFormResponse", {"id": self.ID, "playerId": clientApi.GetLocalPlayerId(), "data": values, "canceled": False})
        clientApi.PopScreen()

    def onClose(self, data):
        clientApi.GetSystem("SAPI", "SAPI_C").NotifyToServer("ModalFormResponse", {"id": self.ID, "playerId": clientApi.GetLocalPlayerId(), "data": None, "canceled": True})
        clientApi.PopScreen()

class CustomFormUI(ScreenNode):
    """Custom form."""
    
    def __init__(self, namespace, name, params):
        ScreenNode.__init__(self, namespace, name, params)
        self.titleLabel = params['title']
        self.formId = params['formId']
        self.data = params['data']
        self.TOUCH_PATH = "/panel/scroll_touch/scroll_view/panel/background_and_viewport/background"
        self.MOUSE_PATH = "/panel/scroll_mouse/scroll_view/stack_panel/background_and_viewport/background"
        self.content = None
        self.title = None
        self.close_btn = None
        self.panel = None
        self.move_btn = None
        self.resize_btn = None
        self.movable = params['options']['movable']
        self.resizable = params['options']['resizable']
        self.style = params['options']['style']
        self.textFields = []
        self.toggles = []
        self.sliders = []
        self.dropdowns = []

    @ViewBinder.binding(ViewBinder.BF_ButtonClickUp, '#custom_form_close')
    def Close(self, args):
        clientApi.PopScreen()

    def Create(self):
        self.panel = self.GetBaseUIControl("/panel")
        self.content = self.GetBaseUIControl("/panel").asScrollView().GetScrollViewContentControl()
        self.title = self.GetBaseUIControl(self.TOUCH_PATH + "/title")
        self.close_btn = self.GetBaseUIControl(self.TOUCH_PATH + "/close")
        if not self.title:
            self.title = self.GetBaseUIControl(self.MOUSE_PATH + "/title")
            self.close_btn = self.GetBaseUIControl(self.MOUSE_PATH + "/close")
        if not self.title:
            raise Exception("Create form error!")
        self.close_btn = self.close_btn.asButton()
        self.close_btn.AddTouchEventParams({"isSwallow": True})
        self.close_btn.SetButtonTouchUpCallback(lambda x: clientApi.PopScreen())
        self.title = self.title.asLabel()
        self.title.SetText(self.titleLabel)
        self.move_btn = self.GetBaseUIControl("/move").asButton()
        self.move_btn.AddTouchEventParams({"isSwallow": True})
        self.move_btn.SetButtonTouchMoveCallback(self.move)
        self.resize_btn = self.GetBaseUIControl("/resize").asButton()
        self.resize_btn.AddTouchEventParams({"isSwallow": True})
        self.resize_btn.SetButtonTouchMoveCallback(self.resize)
        self.move_btn.SetVisible(self.movable)
        self.resize_btn.SetVisible(self.resizable)
        self.update({"data": self.data, "title": self.titleLabel, "formId": self.formId})

    def Update(self):
        for (textField, obId, value) in self.textFields:
            text = textField.GetEditText()
            if text != value:
                clientApi.GetSystem("SAPI", "SAPI_C").NotifyToServer(
                    "updateObservable%s" % obId, 
                    {"value": text}
                )
        for (toggle, obId, value) in self.toggles:
            toggled = toggle.GetToggleState()
            if toggled != value:
                clientApi.GetSystem("SAPI", "SAPI_C").NotifyToServer(
                    "updateObservable%s" % obId, 
                    {"value": toggled}
                )
        for (slider, obId, value, minValue, maxValue) in self.sliders:
            steps = maxValue - minValue
            cur = int(round(slider.GetSliderValue() * steps) + minValue)
            if cur != value:
                clientApi.GetSystem("SAPI", "SAPI_C").NotifyToServer(
                    "updateObservable%s" % obId, 
                    {"value": cur}
                )

    def update(self, data):
        self.data = data['data']
        self.titleLabel = data['title']
        self.textFields = []
        self.toggles = []
        self.sliders = []
        self.dropdowns = []
        index = 0
        height = 0
        self.title.SetText(data['title'])
        for controlData in data['data']:
            if not controlData['visible']:
                continue
            control = self.content.GetChildByName("c%s" % index)
            if controlData['type'] == 'button':
                if control:
                    if control.asButton():
                        # Control created and is the same type, only cauculate this height.
                        control.SetFullPosition("y", {"absoluteValue": height + 5})
                        height += 35
                    else:
                        # Control created but is not the same type, delete and create it again.
                        self.RemoveChildControl(control)
                        control = self.CreateChildControl("oreui_controls.normal_btn", "c%s" % index, self.content).asButton()
                        control.SetFullPosition("y", {"absoluteValue": height + 5})
                        height += 35
                else:
                    # Control not created, create now.
                    control = self.CreateChildControl("oreui_controls.normal_btn", "c%s" % index, self.content).asButton()
                    control.SetFullPosition("y", {"absoluteValue": height + 5})
                    height += 35
                # Add callbacks.
                control = control.asButton()
                control.AddTouchEventParams({"isSwallow": True})
                control.SetButtonTouchUpCallback(self.onButtonClick)
                # Update labels.
                control.GetChildByPath("/default/button_label").asLabel().SetText(controlData['label'])
                control.GetChildByPath("/hover/button_label").asLabel().SetText(controlData['label'])
                control.GetChildByPath("/pressed/button_label").asLabel().SetText(controlData['label'])
            elif controlData['type'] == 'label':
                if control:
                    if control.asLabel():
                        # Control created and is the same type, only cauculate this height.
                        pass
                    else:
                        # Control created but is not the same type, delete and create it again.
                        self.RemoveChildControl(control)
                        control = self.CreateChildControl("oreui_controls.label", "c%s" % index, self.content).asLabel()
                else:
                    # Control not created, create now.
                    control = self.CreateChildControl("oreui_controls.label", "c%s" % index, self.content).asLabel()
                control.asLabel().SetText(controlData['text'])
                control.SetFullPosition("y", {"absoluteValue": height + 5})
                height += int(control.GetSize()[1])
            elif controlData['type'] == 'divider':
                if control:
                    if control.GetChildByName("bg2"):
                        # Control created and is the same type, only cauculate this height.
                        control.SetFullPosition("y", {"absoluteValue": height + 10})
                        height += 20
                    else:
                        # Control created but is not the same type, delete and create it again.
                        self.RemoveChildControl(control)
                        control = self.CreateChildControl("oreui_controls.divider", "c%s" % index, self.content)
                        control.SetFullPosition("y", {"absoluteValue": height + 10})
                        height += 20
                else:
                    # Control not created, create now.
                    control = self.CreateChildControl("oreui_controls.divider", "c%s" % index, self.content)
                    control.SetFullPosition("y", {"absoluteValue": height + 10})
                    height += 20
            elif controlData['type'] == 'textField':
                if control:
                    if control.asTextEditBox():
                        # Control created and is the same type, only cauculate this height.
                        control.SetFullPosition("y", {"absoluteValue": height + 20})
                        height += 50
                    else:
                        # Control created but is not the same type, delete and create it again.
                        self.RemoveChildControl(control)
                        control = self.CreateChildControl("oreui_controls.textfield", "c%s" % index, self.content)
                        control.SetFullPosition("y", {"absoluteValue": height + 20})
                        height += 50
                else:
                    # Control not created, create now.
                    control = self.CreateChildControl("oreui_controls.textfield", "c%s" % index, self.content)
                    control.SetFullPosition("y", {"absoluteValue": height + 20})
                    height += 50
                control = control.asTextEditBox()
                # Set title and the value.
                control.GetChildByPath("/default/title").asLabel().SetText(controlData['label'])
                control.GetChildByPath("/hover/title").asLabel().SetText(controlData['label'])
                control.GetChildByPath("/pressed/title").asLabel().SetText(controlData['label'])
                control.SetEditText(controlData['text'])
                if controlData['clientWritable']:
                    self.textFields.append((control, controlData['textId'], controlData['text']))
            elif controlData['type'] == 'toggle':
                if control:
                    if control.GetChildByName("toggle"):
                        # Control created and is the same type, only cauculate this height.
                        control.SetFullPosition("y", {"absoluteValue": height})
                        height += 25
                    else:
                        # Control created but is not the same type, delete and create it again.
                        self.RemoveChildControl(control)
                        control = self.CreateChildControl("oreui_controls.toggle", "c%s" % index, self.content)
                        control.SetFullPosition("y", {"absoluteValue": height})
                        height += 25
                else:
                    # Control not created, create now.
                    control = self.CreateChildControl("oreui_controls.toggle", "c%s" % index, self.content)
                    control.SetFullPosition("y", {"absoluteValue": height})
                    height += 25
                # Set label and the value.
                control.GetChildByName("title").asLabel().SetText(controlData['label'])
                toggle = control.GetChildByName("toggle").asSwitchToggle()
                toggle.SetToggleState(controlData['toggled'])
                if controlData['clientWritable']:
                    self.toggles.append((toggle, controlData['toggledId'], controlData['toggled']))
            elif controlData['type'] == 'slider':
                if control:
                    if control.GetChildByName("slider"):
                        # Control created and is the same type, only cauculate this height.
                        control.SetFullPosition("y", {"absoluteValue": height})
                        height += 35
                    else:
                        # Control created but is not the same type, delete and create it again.
                        self.RemoveChildControl(control)
                        control = self.CreateChildControl("oreui_controls.slider", "c%s" % index, self.content)
                        control.SetFullPosition("y", {"absoluteValue": height})
                        height += 35
                else:
                    # Control not created, create now.
                    control = self.CreateChildControl("oreui_controls.slider", "c%s" % index, self.content)
                    control.SetFullPosition("y", {"absoluteValue": height})
                    height += 35
                # Set label and the current value.
                control.GetChildByName("label").asLabel().SetText(controlData['label'])
                slider = control.GetChildByName("slider").asSlider()
                steps = float(controlData['maxValue'] - controlData['minValue'])
                slider.SetSliderValue(((controlData['value'] - controlData['minValue']) / steps) if steps else 0)
                control.GetChildByName("value").asLabel().SetText("%s" % controlData['value'])
                if controlData['clientWritable']:
                    self.sliders.append((slider, controlData['valueId'], controlData['value'], controlData['minValue'], controlData['maxValue']))
            index += 1
        self.content.SetFullSize("y", {"absoluteValue": height + 20})
        # Clear visible controls.
        while self.content.GetChildByName("c%s" % index):
            self.RemoveChildControl(self.content.GetChildByName("c%s" % index))
            index += 1

    def onButtonClick(self, data):
        clientApi.GetSystem("SAPI", "SAPI_C").NotifyToServer(
            "updateForm%s" % self.formId, 
            {
                "selection": int(data['ButtonPath'][-1]),
                "operation": "buttonClick"
            }
        )

    def move(self, data):
        size = self.panel.GetSize()
        posX = self.move_btn.GetPosition()[0]
        posY = self.move_btn.GetPosition()[1]
        self.panel.SetPosition((posX - size[0] / 2 + 8, posY))
        self.resize_btn.SetPosition((posX + size[0] / 2 - 8, posY + size[1] - 25))

    def resize(self, data):
        posX = self.resize_btn.GetPosition()[0]
        posY = self.resize_btn.GetPosition()[1]
        ori = self.panel.GetPosition()
        ori_size = self.panel.GetSize()
        size = (posX - ori[0] + 16, posY - ori[1] + 25)
        move_ori_pos = self.move_btn.GetPosition()
        self.panel.SetSize(size, True)
        self.panel.SetPosition(ori)
        self.move_btn.SetPosition((move_ori_pos[0] + size[0] / 2 - ori_size[0] / 2, move_ori_pos[1]))

class More(ScreenNode):
    pass
