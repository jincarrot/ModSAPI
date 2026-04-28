# -*- coding: utf-8 -*-
import mod.client.extraClientApi as clientApi

ScreenNode = clientApi.GetScreenNodeCls()

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
            self.Clone("%s/dynamic_button" % path, path, "dynamic_button%s" % buttonId)
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
        self.RemoveComponent("%s/dynamic_button" % path, path)
        self.refreshId = clientApi.GetEngineCompFactory().CreateGame(clientApi.GetLevelId()).AddRepeatedTimer(0.2, self.refreshImage)

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
