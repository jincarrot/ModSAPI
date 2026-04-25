import time

def TimeCost(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print("Time cost: ", end - start, "s")
        return result
    return wrapper