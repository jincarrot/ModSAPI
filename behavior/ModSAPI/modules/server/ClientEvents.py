# -*- coding: utf-8 -*-
# from typing import Union, Dict
import mod.client.extraClientApi as clientApi

CComp = clientApi.GetEngineCompFactory()


class ClientAfterEvents(object):
    """
    Contains a set of events that are available across the scope of the Client System.
    """

    def __init__(self):
        pass

    @property
    def tapRelease(self):
        return

class ClientBeforeEvents(object):
    """
    Contains a set of events that are available across the scope of the Client System.
    """

    def __init__(self):
        pass
