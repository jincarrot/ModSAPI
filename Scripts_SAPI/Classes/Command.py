# -*- coding: utf-8 -*-
# from typing import Union, Dict
from ..Classes.Entity import *

class CommandResult(object):
    """
    Contains return data on the result of a command execution.
    """

    def __init__(self, data):
        # type: (dict) -> None
        self.__successCount = data['successCount']

    @property
    def successCount(self):
        # type: () -> int
        """
        If the command operates against a number of entities, blocks, or items,
        this returns the number of successful applications of this command.

        Note: this may takes wrong value
        """
        return self.__successCount