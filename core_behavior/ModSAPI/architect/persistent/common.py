class DBSource:
    def getData(self, key):
        pass
    
    def setData(self, key, value):
        pass

    def removeData(self, key):
        pass

    def clearData(self):
        pass

    def createView(self, key):
        return DatabaseView(self, key)
    
    def createArrayView(self, key):
        return DatabaseArrayView(self, key)

class DatabaseView:
    def __init__(self, db, key):
        # type: (DBSource, str) -> None
        self.cache = db.getData(key) or {}
        self.db = db
        self.key = key

    def get(self, item, default=None):
        v = self.cache.get(item)
        if v is None:
            self.set(item, default)
            return default
        return v
    
    def set(self, key, value):
        self.cache[key] = value
        self.db.setData(self.key, self.cache)

    def has(self, item):
        return item in self.cache

    def batch(self, updater):
        cache = self.cache
        for k, v in self.cache.items():
            updater(v, k, cache)

class DatabaseArrayView:
    def __init__(self, db, key):
        # type: (DBSource, str) -> None
        self.cache = list(db.getData(key)) or []
        self.db = db
        self.key = key

    def get(self, item, default=None):
        v = self.cache[item]
        if v is None:
            self.set(item, default)
            return default
        return v
    
    def set(self, key, value):
        self.cache[key] = value
        self.db.setData(self.key, self.cache)

    def batch(self, updater):
        cache = self.cache
        for i, v in enumerate(self.cache):
            updater(v, i, cache)

    def size(self):
        return len(self.cache)

    def iter(self):
        return self.cache