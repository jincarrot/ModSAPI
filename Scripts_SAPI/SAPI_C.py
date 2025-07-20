# coding=utf-8
import mod.client.extraClientApi as clientApi
import math, time
from Classes.ClientEvents import *
from Classes.Request import *

ClientSystem = clientApi.GetClientSystemCls()

CComp = clientApi.GetEngineCompFactory()


class SAPI_C(ClientSystem):

    def __init__(self, namespace, systemName):
        ClientSystem.__init__(self, namespace, systemName)
        self.__ListenEvent()
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

