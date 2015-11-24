__author__ = 'grimalkin'
import threading
import time


class Transition(threading.Thread):

    running = True

    current_value = 0
    target_value = 0
    delta = 0

    tick = 0.00001

    def run(self):
        super(Transition, self).run()
        while self.running:
            if self.is_update():
                self.current_value += self.delta

            if not self.is_update():
                self.current_value = self.target_value

            print self.current_value
            time.sleep(self.tick)

    def is_update(self):
        return (self.delta > 0 and self.current_value < self.target_value) \
            or (self.delta < 0 and self.current_value > self.target_value)

    def slide_to(self, value, duration):
        self.target_value = value
        self.delta = (self.target_value - self.current_value) / (duration / self.tick)

    def stop(self):
        self.running = False


t = Transition()
t.start()
t.slide_to(10, 1)

time.sleep(3)

t.slide_to(50, 8)

time.sleep(9)

t.slide_to(2, 3)

time.sleep(5)

t.slide_to(1000, 3)

time.sleep(5)

t.slide_to(500, 7)

time.sleep(5)

t.slide_to(1000, 3)

time.sleep(5)

t.slide_to(-1000, 9)

time.sleep(4.5)

t.stop()

