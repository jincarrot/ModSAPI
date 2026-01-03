from ..ref import Ref
from ..unreliable import Unreliable            

class Delegate(Unreliable):
    def __init__(self):
        Unreliable.__init__(self)
        self.__fn = None

    def bind(self, fn):
        self.__fn = fn

    def call(self, *args):
        if self.__fn is not None:
            self.__fn(*args)

    def unbind(self):
        self.__fn = None

    def __call__(self, *args):
        self.call(*args)


class EventSignal(Unreliable):
    def __init__(self):
        Unreliable.__init__(self)
        self.__handlers = []

    def on(self, fn):
        self.__handlers.append(fn)

    def off(self, fn):
        self.__handlers.remove(fn)

    def emit(self, *args):
        for fn in self.__handlers:
            self.tryCall(fn, *args)


class EventTarget:
    def __init__(self):
        self.__events = {}

    def addListener(self, event, fn):
        if event not in self.__events:
            self.__events[event] = EventSignal()
        self.__events[event].on(fn)

    def removeListener(self, event, fn):
        if event in self.__events:
            self.__events[event].off(fn)

    def dispatch(self, event, *args):
        if event in self.__events:
            self.__events[event].emit(*args)

class ChainedEvent:
    def __init__(self, eventType, interruptRef, data):
        self.eventType = eventType
        self._interruptRef = interruptRef
        self._data = data

    def stop(self):
        """停止事件传递"""
        self._interruptRef.value = True

    def prevent(self):
        """阻止默认事件 (cancel 设置为 True)"""
        if 'cancel' in self._data:
            self._data['cancel'] = True

    def dict(self):
        return self._data
    
    def setEvent(self, p, v):
        self._data[p] = v

    def __getattr__(self, name):
        if name in self._data:
            return self._data[name]

class EventChain(Unreliable):
    def __init__(self):
        Unreliable.__init__(self)
        self.__handlers = []
        """顺序触发监听器，通过 stop() 决定是否结束事件传递"""
        self.guarded = True
        """当为 True 时, 上一个事件监听器出错后，后续事件监听器将不会执行"""
        self.useCapture = False
        """当为 True 时, 事件监听器将按添加顺序执行（捕获）"""

    def capture(self, fn):
        """添加事件监听器（捕获）"""
        self.__handlers.append(fn)

    def addListener(self, fn):
        """添加事件监听器（冒泡）"""
        self.__handlers.insert(0, fn)

    def removeListener(self, fn):
        self.__handlers.remove(fn)

    def dispatch(self, evType, _ev):
        shouldBreak = Ref(False)
        ev = ChainedEvent(evType, shouldBreak, _ev)
        handlers = self.__handlers if self.useCapture else reversed(self.__handlers)
        for fn in handlers:
            _, err = self.tryCall(fn, ev)
            if err and self.guarded:
                return

            if shouldBreak.value:
                break