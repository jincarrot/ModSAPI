# -*- coding: utf-8 -*-
# from typing import Union, Dict

class CommandResult(object):
    """
    Contains return data on the result of a command execution.
    """
    @property
    def successCount(self):
        # type: () -> int
        """
        If the command operates against a number of entities, blocks, or items,
        this returns the number of successful applications of this command.

        Note: this may takes wrong value
        """