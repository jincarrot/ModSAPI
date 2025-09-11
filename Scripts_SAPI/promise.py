"""
Javascript Promises/A+ specification implementation
"""
from types import FunctionType

def empty_fn():
    pass

class Thenable:
    def then(self, onFulfilled, onRejected):
        pass

class PromiseResolvers:
    def __init__(self, promise, resolve, reject):
        self.promise = promise
        self.resolve = resolve
        self.reject = reject

class ref:
    def __init__(self, value):
        self.value = value

class Promise(Thenable):

    PENDING = 0
    FULFILLED = 1
    REJECTED = 2

    def __init__(self, executor):
        self._state = Promise.PENDING
        self._value = None
        self._reason = None
        self._onFulfilledCallbacks = []
        self._onRejectedCallbacks = []

        def resolve(value):
            if self._state == Promise.PENDING:
                self._state = Promise.FULFILLED
                self._value = value
                for fn in self._onFulfilledCallbacks:
                    fn(value)

        def reject(reason):
            if self._state == Promise.PENDING:
                self._state = Promise.REJECTED
                self._reason = reason
                for fn in self._onRejectedCallbacks:
                    fn(reason)

        try:
            executor(resolve, reject)
        except Exception as e:
            reject(e)

    def __resolve(promise, x, re, rej):
        if promise == x:
            return rej(TypeError('Promise and x refer to the same object'))

        if isinstance(x, Promise):
            x.then(re, rej)
            return
        
        re(x)

    def then(self, onFulfilled, onRejected):
        # type: (FunctionType, FunctionType) -> Promise
        realFullfilled = lambda v: v if not callable(onFulfilled) else onFulfilled
        realRejected = lambda r: r if not callable(onRejected) else onRejected

        if self._state == Promise.PENDING:
            self._onFulfilledCallbacks.append(realFullfilled)
            self._onRejectedCallbacks.append(realRejected)

        if self._state == Promise.FULFILLED:
            promise2 = None
            def executor(res, rej):
                try:
                    if not callable(onFulfilled):
                        res(self._value)
                    else:
                        v = realFullfilled(self._value)
                        Promise.__resolve(promise2, v, res, rej)

                    res(self._value)
                except Exception as e:
                    rej(e)

            promise2 = Promise(executor)
            return promise2

        if self._state == Promise.REJECTED:
            promise2 = None
            def executor(res, rej):
                try:
                    if not callable(onRejected):
                        rej(self._reason)
                    else:
                        v = realRejected(self._value)
                        Promise.__resolve(promise2, v, res, rej)

                    res(self._value)
                except Exception as e:
                    rej(e)

            promise2 = Promise(executor)
            return promise2

    def catch(self, onRejected):
        return self.then(empty_fn, onRejected)
    
    def finally_(self, onFinally):
        return self.then(lambda v: onFinally(), lambda r: onFinally())

    @staticmethod
    def withResolvers():
        resolve = ref(None)
        reject = ref(None)

        def executor(res, rej):
            resolve.value = res
            reject.value = rej

        promise = Promise(executor)
        return PromiseResolvers(promise, resolve.value, reject.value)

    @staticmethod
    def resolve(value):
        return Promise(lambda res, _: res(value))
    
    @staticmethod
    def reject(reason):
        return Promise(lambda _, rej: rej(reason))
    
    @staticmethod
    def all(promises):
        def executor(res, rej):
            if len(promises) == 0:
                return res([])

            results = []
            for i in range(len(promises)):
                def onfulfill(val):
                    results[i] = val
                    if len(results) == len(promises):
                        res(results)

                def onreject(reason):
                    rej(reason)

                promises[i].then(onfulfill, onreject)


        return Promise(executor)
    
    @staticmethod
    def race(promises):
        def executor(res, rej):
            for promise in promises:
                def onfulfill(val):
                    res(val)

                def onreject(reason):
                    rej(reason)

                promise.then(onfulfill, onreject)

        return Promise(executor)
    
    @staticmethod
    def any(promises):
        def executor(res, rej):
            for promise in promises:
                def onfulfill(val):
                    res(val)

                def onreject(reason):
                    pass

                promise.then(onfulfill, onreject)

        return Promise(executor)
    
    @staticmethod
    def allSettled(promises):
        def executor(res, rej):
            results = []
            for promise in promises:
                def onfulfill(val):
                    results.append({'status': 'fulfilled', 'value': val})

                    if len(results) == len(promises):
                        res(results)

                def onreject(reason):
                    results.append({'status': 'rejected', 'reason': reason})

                    if len(results) == len(promises):
                        res(results)

                promise.then(onfulfill, onreject)

        return Promise(executor)
