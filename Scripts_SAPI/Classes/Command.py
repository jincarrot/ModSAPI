# -*- coding: utf-8 -*-
# from typing import Union, Dict
from ..Classes.Entity import *

class CommandResult(object):
    """
    Contains return data on the result of a command execution.
    """

    def __init__(self, data):
        # type: (dict) -> None
        self.__successCount = data['seccessCount']

    @property
    def successCount(self):
        # type: () -> int
        return self.__successCount