# coding=utf-8
import mod.client.extraClientApi as clientApi
import math, time
from Classes.Request import *

ClientSystem = clientApi.GetClientSystemCls()


class SAPI_C(ClientSystem):

    def __init__(self, namespace, systemName):
        ClientSystem.__init__(self, namespace, systemName)
        self.__ListenEvent()
        print("SAPI_C loaded")

    def __ListenEvent(self):
        self.ListenForEvent("SAPI", "world", "getData", self, self.getData)

    def getData(self, data):
        """receive request from server"""
        requestId = data['requestId']
        request.update(requestId, "test")

