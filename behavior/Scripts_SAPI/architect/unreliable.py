
class Unreliable:
    @staticmethod
    def _defaultErrorHandler(err):
        print(err)

    def __init__(self):
        self._errorHandler = Unreliable._defaultErrorHandler

    def onError(self, fn):
        self._errorHandler = fn

    def tryCall(self, fn, *args):
        try:
            return fn(*args), None
        except Exception as err:
            try:
                self._errorHandler(err)
                return (None, err)
            except Exception as err:
                print(err)
                return (None, err)
