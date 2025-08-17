# -*- coding: utf-8 -*-
import mod.server.extraServerApi as serverApi
import SAPI_S as SAPI
from Classes.ItemStack import *

def getWorld():
    # type: () -> SAPI.World
    return serverApi.GetSystem("SAPI", "world")

def getSystem():
    # type: () -> SAPI.System
    return serverApi.GetSystem("SAPI", "system")

world = getWorld()
system = getSystem()

ServerSystem = serverApi.GetServerSystemCls()

class SAPIS(ServerSystem):
    """
    base system of this addon
    """

    def __init__(self, namespace, systemName):
        ServerSystem.__init__(self, namespace, systemName)
        self.__ListenEvents()

    def __ListenEvents(self):
        self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "ServerChatEvent", self, self.debug)
        self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "LoadServerAddonScriptsAfter", self, self.Init)
        self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "CustomCommandTriggerServerEvent", self, self.customCommand)
    
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
        global world
        world = getWorld()

    def customCommand(self, data):
        if data['command'] == 'modsapi':
            args = data['args']
            origin = data['origin']['entityId']
            if origin:
                if args[0]['value'] == 'debug':
                    self.debug({"message": "debug %s" % args[1]['value']})
            data['return_failed'] = False
