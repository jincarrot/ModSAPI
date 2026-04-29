# coding=utf-8
import mod.client.extraClientApi as clientApi
from client import systems
from ..interfaces.Vector import Vector3

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
        client.afterEvents.serverEventReceive.subscribe("modsapi.dimension.spawnParticle", self.spawnParticle)
        self.ListenForEvent(clientApi.GetEngineNamespace(), clientApi.GetEngineSystemName(), "UiInitFinished", self, self.initUI)

    def spawnParticle(self, arg):
        data = arg.data
        effectName = data['effectName']
        location = data['location']
        molangVariables = data['molangVariables']
        particle = systems.client.spawnParticle(effectName, Vector3(location))
        for molang, value in (molangVariables or {}).items():
            if value['type'] == 'rgb':
                particle.setMolang("%s.r" % molang, value['value']['red'])
                particle.setMolang("%s.g" % molang, value['value']['green'])
                particle.setMolang("%s.b" % molang, value['value']['blue'])
            elif value['type'] == 'rgba':
                particle.setMolang("%s.r" % molang, value['value']['red'])
                particle.setMolang("%s.g" % molang, value['value']['green'])
                particle.setMolang("%s.b" % molang, value['value']['blue'])
                particle.setMolang("%s.a" % molang, value['value']['alpha'])
            elif value['type'] == 'float':
                particle.setFloat(molang, value['value'])
            elif value['type'] == 'speed_and_direction':
                particle.setMolang("%s.speed" % molang, value['value']['speed'])
                particle.setMolang("%s.direction_x" % molang, value['value']['direction'][0])
                particle.setMolang("%s.direction_y" % molang, value['value']['direction'][1])
                particle.setMolang("%s.direction_z" % molang, value['value']['direction'][2])
            elif value['type'] == 'vector3':
                particle.setMolang("%s.x" % molang, value['value'][0])
                particle.setMolang("%s.y" % molang, value['value'][1])
                particle.setMolang("%s.z" % molang, value['value'][2])

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
