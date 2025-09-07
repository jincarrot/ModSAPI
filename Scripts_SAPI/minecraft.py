# -*- coding: utf-8 -*-
import mod.server.extraServerApi as serverApi
import SAPI_S as SAPI
from Classes.ItemStack import *
import Classes.FormData as fd

def getWorld():
    # type: () -> SAPI.World
    return serverApi.GetSystem("SAPI", "world")

def getSystem():
    # type: () -> SAPI.System
    return serverApi.GetSystem("SAPI", "system")

def getActionFormData():
    # type: () -> fd.ActionFormData
    if serverApi.GetSystem("SAPI", "Base"):
        return serverApi.GetSystem("SAPI", "Base").getActionFormData()

world = getWorld()
system = getSystem()
ActionFormData = getActionFormData()

ServerSystem = serverApi.GetServerSystemCls()

class SAPIS(ServerSystem):
    """
    base system of this addon
    """

    def __init__(self, namespace, systemName):
        ServerSystem.__init__(self, namespace, systemName)
        self.__ListenEvents()
        self.formTasks = {}

    def __ListenEvents(self):
        self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "ServerChatEvent", self, self.debug)
        self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "LoadServerAddonScriptsAfter", self, self.Init)
        self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "CustomCommandTriggerServerEvent", self, self.customCommand)
        self.ListenForEvent("SAPI", "SAPI_C", "ActionFormResponse", self, self.responseActionForm)
    
    def debug(self, data):
        global world
        msg = data['message']
        if msg.find('debug ') == 0:
            msg = msg[6:]
            if not world:
                world = getWorld()
            print(msg)
            exec(compile(msg, "<string>", "exec"))

    @staticmethod
    def Init(__data):
        global world, ActionFormData
        world = getWorld()
        ActionFormData = getActionFormData()

    def customCommand(self, data):
        if data['command'] == 'modsapi':
            args = data['args']
            origin = data['origin']['entityId']
            if origin:
                if args[0]['value'] == 'debug':
                    self.debug({"message": "debug %s" % args[1]['value']})
            data['return_failed'] = False

    def responseActionForm(self, data):
        if data['id'] in self.formTasks:
            self.formTasks[data['id']](fd.ActionFormResponse(data))

    def getActionFormData(self):
        return fd.ActionFormData
    
    def setFormCallback(self, id, callback):
        self.formTasks[id] = callback
