# -*- coding: utf-8 -*-
from ...architect.scheduler import Scheduler
import mod.server.extraServerApi as serverApi

ServerSystem = serverApi.GetServerSystemCls()

class System(ServerSystem):
    """
    A class that provides system-level events and functions.
    """

    _scriptScheduler = Scheduler()

    def __init__(self, namespace, systemName):
        ServerSystem.__init__(self, namespace, systemName)
        self._initScheduler()

    def _OnScriptTickServer(self):
        self._scriptScheduler.executeSequenceAsync()

    def _initScheduler(self):
        self.ListenForEvent(
            serverApi.GetEngineNamespace(),
            serverApi.GetEngineSystemName(),
            "OnScriptTickServer",
            self,
            self._OnScriptTickServer
        )

    def run(self, callback):
        """
        Runs a specified function at the next available future time. 
        This is frequently used to implement delayed behaviors and game loops. 
        When run within the context of an event handler, this will generally run the code at the end of the same tick where the event occurred. 
        When run in other code (a system.run callout), this will run the function in the next tick. 
        
        Note, however, that depending on load on the system, running in the same or next tick is not guaranteed."""
        return self._scriptScheduler.run(callback)

    def runTimeout(self, callback, tickDelay=1):
        """
        Runs a set of code at a future time specified by tickDelay.
        """
        return self._scriptScheduler.runTimer(callback, tickDelay)

    def runInterval(self, callback, tickInterval=1):
        """
        Runs a set of code on an interval.
        """
        return self._scriptScheduler.runTimer(callback, tickInterval, True)

    def clearRun(self, runId):
        """
        Cancels the execution of a function run that was previously scheduled via @minecraft/server.System.run.
        """
        self._scriptScheduler.removeTask('SchedulerTask', runId)

    def send(self, player, eventName, data):
        """Send data to client"""
        
    def runJob(self, generator):
        return self._scriptScheduler.addSuspendableTask('SchedulerTask', generator)
    
    def clearJob(self, jobId):
        self.clearRun(jobId)
