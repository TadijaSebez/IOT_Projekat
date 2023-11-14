import random
import time
import threading


def loop(button):
    while True:
        pressed = button.detect_press()
        if pressed is not None:
            button.callback(pressed)
        time.sleep(0.5)
        if button.should_stop():
            break

class Button:

    def __init__(self, config, stop_event, callback):
        self.stop_event = stop_event
        self.callback = callback
        self.pressed = False

    def detect_press(self):
        newState = random.randint(0, 1) == 1
        if newState != self.pressed:
            self.pressed = newState
            return self.pressed
        else:
            return None
    
    def should_stop(self):
        return self.stop_event.is_set()

    def start(self):
        t = threading.Thread(target=loop, args=(self,))
        t.start()
        return t
