import random
import time
import threading


def loop(light):
    while True:
        try:
            command = light.pipe.recv()
        except:
            break
        if command == "l":
            light.change_state()
        state = light.get_state()
        light.callback(state)
        time.sleep(0.5)
        if light.should_stop():
            break

class Light:

    def __init__(self, config, stop_event, callback, pipe):
        self.stop_event = stop_event
        self.callback = callback
        self.pipe = pipe
        self.state = "off"

    def change_state(self):
        if self.state == "off":
            self.state = "on"
        else:
            self.state ="off"
        return self.state
    
    def get_state(self):
        return self.state
    
    def should_stop(self):
        return self.stop_event.is_set()

    def start(self):
        t = threading.Thread(target=loop, args=(self,))
        t.start()
        return t
