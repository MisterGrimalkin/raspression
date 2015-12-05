__author__ = 'Barri Mason'


class AverageQueue:

    data = None
    size = None

    def __init__(self, size):
        self.size = size
        self.data = [0] * self.size

    def put_value(self, value):
        for i in range(self.size-1):
            self.data[i] = self.data[i+1]
        self.data[self.size-1] = value

    def is_ready(self):
        return self.size == len(self.data)

    def get_average(self):
        tot = 0.0
        for d in self.data:
            tot += d
        return tot / self.size





