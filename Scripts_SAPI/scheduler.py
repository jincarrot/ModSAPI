# coding=utf-8
from threading import Thread
from time import time
from types import *


class Task:
    taskId = 0

    def __init__(self, fn, once):
        self.thread = Thread(target=fn)  # type: Thread
        self.once = once  # type: bool
        self.id = Task.taskId
        Task.taskId += 1


class Scheduler:
    def __init__(self):
        pass

    scheduleSequence = (
        'BeforeUpdate',
        'Update',
        'AfterUpdate',
    )

    _scheduleQueues = {}  # type: dict[str, list[Task]]
    _executingThreads = []  # type: list[Task]

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
            self._executingThreads.append(t)
            t.thread.start()

        for t in self._executingThreads:
            t.thread.join()
            self._executingThreads.remove(t)
            if t.once:
                queue.remove(t)

    def executeAsync(self, scheduleName):
        # type: (str) -> Future
        return Future.runAsync(lambda: self.execute(scheduleName))

    def addTask(self, scheduleName, fn, once=False):
        # type: (str, FunctionType, bool) -> int
        """
        :return: 移除任务的函数
        """
        queue = self._getTaskQueue(scheduleName)
        task = Task(fn, once)
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

    _sequenceExecuting = False
    _lastExecutedTime = time()
    _skippedUpdates = 0
    _innerTicks = 0

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

    def _timeoutWrapper(self, fn, ticks):
        startTick = self._innerTicks

        def wrapper():
            if (self._innerTicks - startTick) % ticks <= 0:
                fn()

        return wrapper

    def runTimer(self, fn, ticks=1, interval=False):
        return self.addTask(
            'SchedulerTask',
            self._timeoutWrapper(fn, max(1, ticks)),
            not interval
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