# -*- coding: utf-8 -*-
import random
import mod.server.extraServerApi as serverApi
from ..minecraft import *

class Request(object):
    """
    a class to get data between client and server
    """

    def __init__(self):
        self.__requests = {}

    def create(self, target, dataName):
        # type: (int, str) -> int
        """create request"""
        requestId = random.randint(0, 32767)
        self.__requests[requestId] = {
            "state": 0,
            "value": None
        }
        world.NotifyToClient(target, "getData", {"requestId": requestId, "dataName": dataName})
        return requestId

    def getState(self, requestId):
        # type: (int) -> bool
        return self.__requests[requestId]['state']
    
    def getValue(self, requestId):
        # type: (int) -> 0
        while(True):
            if requestId not in self.__requests:
                return None
            if self.__requests[requestId]['state']:
                value = self.__requests[requestId]['value']
                del self.__requests[requestId]
                return value
    
    def update(self, requestId, value):
        # type: (int, 0) -> bool
        """update value of request. return False if this request is updated or not exist"""
        if requestId not in self.__requests or self.__requests[requestId]['state']:
            return False
        else:
            self.__requests[requestId]['value'] = value
            self.__requests[requestId]['state'] = 1
            return True
     

request = Request()
