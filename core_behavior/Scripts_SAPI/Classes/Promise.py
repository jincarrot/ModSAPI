# -*- coding: utf-8 -*-
import random
import mod.server.extraServerApi as serverApi
from ..minecraft import *

class GamePromise(object):
    """
    This is not equals to promise in js.
    """
    _ID = 0
    
    def __init__(self, callback):
        """
        Create promise.
        
        :param callback: Defines when this promise finished.
        """
        self._id = GamePromise._ID
        self._state = False
        self._callback = None
        GamePromise._ID += 1
        def temp():
            if self._state:
                comp.CreateGame(serverApi.GetLevelId()).CancelTimer(timerId)
                return
            if callback():
                self._state = True
                if self._callback:
                    self._callback()
        timerId = comp.CreateGame(serverApi.GetLevelId()).AddRepeatedTimer(0.03, temp)

    def then(self, callback):
        self._callback = callback

