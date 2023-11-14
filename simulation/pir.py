import random
import time
import threading


def loop(pir):
    while True:
        detected = pir.detect_motion()
        if detected:
            pir.callback()
        time.sleep(0.5)
        if pir.should_stop():
            break

class PIR:

    def __init__(self, config, stop_event, callback):
        self.stop_event = stop_event
        self.callback = callback

    def detect_motion(self):
        return random.randint(0, 1) == 1
    
    def should_stop(self):
        return self.stop_event.is_set()

    def start(self):
        t = threading.Thread(target=loop, args=(self,))
        t.start()
        return t
