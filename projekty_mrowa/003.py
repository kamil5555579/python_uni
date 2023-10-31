import time
import numpy as np

class TimeStatistics:
    def __init__(self, func):
        self.func = func
        self.times = []

    def __call__(self, *args, **kwds):
        start = time.time()
        self.func(*args, **kwds)
        end = time.time()
        self.times.append(end - start)
        print(f"Function {self.func.__name__} took {end - start} seconds to execute")

    def statistics(self):
        return {"mean": np.mean(self.times), "std": np.std(self.times), "min": np.min(self.times), "max": np.max(self.times)}

@TimeStatistics
def test(n=5):
    time.sleep(n)

test(2)
test(3)
test(4)
print(test.statistics())