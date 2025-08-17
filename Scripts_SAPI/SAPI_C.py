# coding=utf-8
import mod.client.extraClientApi as clientApi
import math, time
from Classes.ClientEvents import *
from Classes.Request import *
from scheduler import Scheduler

ClientSystem = clientApi.GetClientSystemCls()

CComp = clientApi.GetEngineCompFactory()


class SAPI_C(ClientSystem):
    frameScheduler = Scheduler()
    scriptScheduler = Scheduler()

    def __init__(self, namespace, systemName):
        ClientSystem.__init__(self, namespace, systemName)
        self.__ListenEvent()
        self._initScheduler()
        print("SAPI_C loaded")

    def __ListenEvent(self):
        self.ListenForEvent("SAPI", "world", "getData", self, self.getData)
        self.ListenForEvent("SAPI", "world", "sendToast", self, self.sendToast)

    def getData(self, data):
        """receive request from server"""
        requestId = data['requestId']
        requestDataName = data['dataName']
        data = None
        if requestDataName == 'clientSystemInfo':
            data = {
                "maxRenderDistance": None,
                "platformType": clientApi.GetPlatform()
            }
        request.update(requestId, data)

    def sendToast(self, data):
        CComp.CreateGame(clientApi.GetLevelId()).SetPopupNotice(data['message'], data['title'])

    def _OnScriptTickClient(self):
        self.scriptScheduler.executeSequenceAsync()
    
    def _OnGameRenderTick(self):
        self.frameScheduler.executeSequenceAsync()

    def _initScheduler(self):
        self.ListenForEvent(
            clientApi.GetEngineNamespace(),
            clientApi.GetEngineSystemName(),
            "OnScriptTickClient",
            self,
            self._OnScriptTickClient
        )

        self.ListenForEvent(
            clientApi.GetEngineNamespace(),
            clientApi.GetEngineSystemName(),
            "GameRenderTickEvent",
            self,
            self._OnGameRenderTick
        )


class Client(ClientSystem):

    def __init__(self, namespace, systemName):
        ClientSystem.__init__(self, namespace, systemName)
        self.__afterEvents = ClientAfterEvents()
        self.__beforeEvents = ClientBeforeEvents()
        print("SAPI: client loaded")

    @property
    def afterEvents(self):
        return self.__afterEvents
    
    @property
    def beforeEvents(self):
        return self.__beforeEvents

