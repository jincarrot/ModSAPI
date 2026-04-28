# coding=utf-8
import mod.client.extraClientApi as clientApi

ClientSystem = clientApi.GetClientSystemCls()

CComp = clientApi.GetEngineCompFactory()


class Core(ClientSystem):
    def __init__(self, namespace, systemName):
        ClientSystem.__init__(self, namespace, systemName)
        self.__ListenEvent()

    def __ListenEvent(self):
        from client import systems
        client = systems.client
        client.afterEvents.serverEventReceive.subscribe("sendCustomForm", self.sendCustomForm)
        client.afterEvents.serverEventReceive.subscribe("updateCustomForm", self.updateCustomForm)
        client.afterEvents.serverEventReceive.subscribe("closeCustomForm", self.closeCustomForm)
        self.ListenForEvent(clientApi.GetEngineNamespace(), clientApi.GetEngineSystemName(), "UiInitFinished", self, self.initUI)

    def initUI(self, data):
        clientApi.RegisterUI("server_ui", "CustomForm", "ModSAPI.modules.server_ui.Forms.CustomFormUI", "server_forms.custom_form")
        clientApi.RegisterUI("server_ui", "MoreUI", "ModSAPI.modules.server_ui.Forms.MoreUI", "server_forms.moreui")
        clientApi.RegisterUI("ModSAPI", "CustomUI", "ModSAPI.modules.server_ui.UI._CustomUI", "server_forms.custom_ui")

    def sendCustomForm(self, data):
        data = data.data
        screen = clientApi.GetTopScreen()
        if hasattr(screen, "isMoreUI"):
            for form in screen.forms:
                if form.formId == data['formId']:
                    screen.GetBaseUIControl(form.basePath).SetVisible(True)
        if hasattr(screen, "update"):
            return
        clientApi.PushScreen("server_ui", "CustomForm", data)

    def updateCustomForm(self, data):
        data = data.data
        screen = clientApi.GetTopScreen()
        if hasattr(screen, "update"):
            screen.update(data)

    def closeCustomForm(self, data):
        data = data.data
        screen = clientApi.GetTopScreen()
        if hasattr(screen, "onButtonClick"):
            clientApi.PopScreen()
        if hasattr(screen, "isMoreUI"):
            for form in screen.forms:
                if form.formId == data['formId']:
                    form.close({})
