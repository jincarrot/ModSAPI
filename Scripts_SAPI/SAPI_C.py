# coding=utf-8
import mod.client.extraClientApi as clientApi
import math

ClientSystem = clientApi.GetClientSystemCls()


class SAPI_C(ClientSystem):

    def __init__(self, namespace, systemName):
        ClientSystem.__init__(self, namespace, systemName)
        print("SAPI_C loaded")
