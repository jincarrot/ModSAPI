# coding=utf-8
from threading import Thread
from time import time
from types import *


class Task:
    taskId = 0

    def __init__(self, fn):
        self.fn = fn  # type: FunctionType
        self.id = Task.taskId
        self.finished = False  # type: bool
        Task.taskId += 1

class Scheduler:
    def __init__(self):
        self._sequenceExecuting = False
        self._lastExecutedTime = time()
        self._skippedUpdates = 0
        self._innerTicks = 0
        self._scheduleQueues = {}  # type: dict[str, list[Task]]
        self._executingThreads = []  # type: list[Task]
        self.scheduleSequence = (
            'BeforeUpdate',
            'Update',
            'AfterUpdate',
        )
        self._shouldRemoveTaskFns = []


    def _getTaskQueue(self, scheduleName):
        # type: (str) -> list[Task]
        queue = self._scheduleQueues.get(scheduleName)
        if queue is None:
            queue = []
            self._scheduleQueues[scheduleName] = queue

        return queue

    def execute(self, scheduleName):
        queue = self._getTaskQueue(scheduleName)
        for t in queue:
            if t.fn in self._shouldRemoveTaskFns:
                queue.remove(t)
                self._shouldRemoveTaskFns.remove(t.fn)
                continue

            self._executingThreads.append(t)

        for t in self._executingThreads:
            thread = Thread(target=t.fn)
            thread.start()
            thread.join()
            self._executingThreads.remove(t)

    def executeAsync(self, scheduleName):
        # type: (str) -> Future
        return Future.runAsync(lambda: self.execute(scheduleName))

    def addTask(self, scheduleName, fn):
        # type: (str, FunctionType) -> int
        queue = self._getTaskQueue(scheduleName)
        task = Task(fn)
        queue.append(task)
        return task.id

    def removeTask(self, scheduleName, taskId=-1):
        # type: (str, int) -> None
        queue = self._getTaskQueue(scheduleName)
        if taskId != -1:
            for task in queue:
                if task.id == taskId:
                    queue.remove(task)
                    return
        else:
            queue.clear()

    def executeSequence(self):
        """
        :rtype: tuple[float, int]
        :return: (deltaTime, skippedUpdates)
        """
        self._innerTicks += 1
        if self._sequenceExecuting:
            self._skippedUpdates += 1
            return 0.0, self._skippedUpdates

        self._sequenceExecuting = True
        self.execute('SchedulerTask')
        for scheduleName in self.scheduleSequence:
            self.execute(scheduleName)

        dt = time() - self._lastExecutedTime
        self._lastExecutedTime = time()
        self._sequenceExecuting = False

        return dt, self._skippedUpdates

    def executeSequenceAsync(self):
        # type: () -> Future[tuple[float, int], Exception]
        return Future.runAsync(lambda: self.executeSequence())

    def _timeoutWrapper(self, fn, ticks, once=False):
        startTick = self._innerTicks

        def wrapper():
            if (self._innerTicks - startTick) % ticks <= 0:
                fn()
                if once:
                    self._shouldRemoveTaskFns.append(wrapper)

        return wrapper

    def runTimer(self, fn, ticks=1, interval=False):
        return self.addTask(
            'SchedulerTask',
            self._timeoutWrapper(fn, max(1, ticks), not interval),
        )

    def run(self, fn):
        return self.runTimer(fn)


class Future:
    def _wrapper(self, fn):
        def wrapper():
            try:
                self._value = fn()
            except Exception as e:
                self._error = e

        return wrapper

    def __init__(self, executor):
        # type: (FunctionType) -> None
        self._executor = Thread(target=self._wrapper(executor))
        self._value = None
        self._error = None

    def start(self):
        self._executor.start()

    def wait(self):
        # type: () -> tuple[object, Exception]
        self._executor.join()
        return self._value, self._error

    def result(self, onReturn, onError):
        # type: (FunctionType, FunctionType) -> type
        (result, error) = self.wait()
        return onReturn(result) if error is None else onError(error)

    @staticmethod
    def runAsync(fn):
        ftr = Future(fn)
        ftr.start()
        return ftr