__author__ = 'grimalkin'

import threading
import time


class Linear(threading.Thread):

    sensor = -1

    current_value = 0
    target_value = 0
    delta = 0
    func = None

    tick = 0.1
    running = True

    def __init__(self, sensor):
        super(Linear, self).__init__()
        self.sensor = sensor

    def run(self):
        super(Linear, self).run()

        while self.running:
            distance = self.current_value - self.target_value

            if self.delta != 0:
                if abs(distance) <= abs(self.delta):
                    self.current_value = self.target_value
                    self.delta = 0
                else:
                    self.current_value += self.delta

                self.current_value = int(self.current_value)

                if self.func is not None:
                    self.func(self.sensor, self.current_value)

            time.sleep(self.tick)

    def slide_to(self, value, duration, func):
        self.target_value = value
        if duration == 0:
            self.delta = self.target_value - self.current_value
        else:
            self.delta = (self.target_value - self.current_value) / (duration / self.tick)
        self.func = func

    def stop(self):
        self.running = False


class Instant(threading.Thread):

    sensor = -1

    tick = 0.001
    running = True

    def __init__(self, sensor):
        super(Instant, self).__init__()
        self.sensor = sensor

    def run(self):
        super(Instant, self).run()

        while self.running:
            time.sleep(self.tick)

    def slide_to(self, value, duration, func):
        if func is not None:
            func(self.sensor, value)

    def stop(self):
        self.running = False
