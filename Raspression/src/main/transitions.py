__author__ = 'grimalkin'

import threading
import time


class Linear(threading.Thread):

    sensor = -1

    current_value = 0
    target_value = 0
    delta = 0
    func = None

    tick = 0.001
    running = True

    def __init__(self, sensor):
        super(Linear, self).__init__()
        self.sensor = sensor

    def run(self):
        super(Linear, self).run()

        while self.running:
            if self.current_value != self.target_value:
                if self.is_update():
                    self.current_value += self.delta

                if not self.is_update():
                    self.current_value = self.target_value

                if self.func is not None:
                    self.func(self.sensor, self.current_value)

            time.sleep(self.tick)

    def is_update(self):
        return (self.delta > 0 and self.current_value < self.target_value) \
            or (self.delta < 0 and self.current_value > self.target_value)

    def slide_to(self, value, duration, func):
        self.target_value = value
        if duration == 0:
            self.delta = self.target_value - self.current_value
        else:
            self.delta = (self.target_value - self.current_value) / (duration / self.tick)
        self.func = func

    def stop(self):
        self.running = False
