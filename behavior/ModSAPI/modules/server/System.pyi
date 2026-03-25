# -*- coding: utf-8 -*-
import typing
from ...architect.scheduler import Scheduler
import mod.server.extraServerApi as serverApi

ServerSystem = serverApi.GetServerSystemCls()

class System(ServerSystem):
    """
    A class that provides system-level events and functions.
    """

    def run(self, callback: typing.Callable[[], None]) -> int:
        """
        Runs a specified function at the next available future time. 
        This is frequently used to implement delayed behaviors and game loops. 
        When run within the context of an event handler, this will generally run the code at the end of the same tick where the event occurred. 
        When run in other code (a system.run callout), this will run the function in the next tick. 
        
        Note, however, that depending on load on the system, running in the same or next tick is not guaranteed."""

    def runTimeout(self, callback: typing.Callable[[], None], tickDelay: int = 1) -> int:
        """
        Runs a set of code at a future time specified by tickDelay.
        """

    def runInterval(self, callback: typing.Callable[[], None], tickInterval: int = 1) -> int:
        """
        Runs a set of code on an interval.
        """

    def clearRun(self, runId: int):
        """
        Cancels the execution of a function run that was previously scheduled via @minecraft/server.System.run.
        """

    def send(self, player, eventName, data):
        """Send data to client"""
        
    def runJob(self, generator):
        """"""
    
    def clearJob(self, jobId):
        """"""
