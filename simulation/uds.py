import random
import time
import threading


def loop(uds):
    while True:
        dist = uds.detect_distance()
        if dist is not None:
            uds.callback(dist)
        time.sleep(0.5)
        if uds.should_stop():
            break

class UDS:

    def __init__(self, config, stop_event, callback):
        self.stop_event = stop_event
        self.callback = callback
        self.dist = config["initial_distance"] if "initial_distance" in config else 50
        self.min_dist = config["minimum_distance"] if "minimum_distance" in config else 1
        self.max_dist = config["maximum_distance"] if "maximum_distance" in config else 100

    def detect_distance(self):
        self.dist += random.randint(-5, 5)
        if self.dist >= self.min_dist or self.dist <= self.max_dist:
            return self.dist
        else:
            return None
    
    def should_stop(self):
        return self.stop_event.is_set()

    def start(self):
        t = threading.Thread(target=loop, args=(self,))
        t.start()
        return t
