class QueryCache:
    def __init__(self, getter):
        self._getter = getter
        self._cache = getter()

    def get(self):
        return self._cache
    
    def update(self):
        self._cache = self._getter()

def cache(getter, default=None):
    return QueryCache(getter).get