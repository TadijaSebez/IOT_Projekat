import random
import time
import threading

def buzzing_loop(stop_event, callback):
    while True:
        callback()
        time.sleep(0.5)
        if stop_event.is_set():
            break

def loop(buzzer):
    while True:
        try:
            command = buzzer.pipe.recv()
        except:
            break
        if command == "b":
            buzzer.change_state()
            state = buzzer.get_state()
            if state == "on":
                buzzer.start_buzzing()
            else:
                buzzer.stop_buzzing()
        time.sleep(0.5)
        if buzzer.should_stop():
            if buzzer.get_state() == "on":
                buzzer.stop_buzzing()
            break

class Buzzer:

    def __init__(self, config, stop_event, callback, pipe):
        self.stop_event = stop_event
        self.callback = callback
        self.pipe = pipe
        self.state = "off"
        self.buzzing_thread = None
        self.buzzing_stop_event = None

    def change_state(self):
        if self.state == "off":
            self.state = "on"
        else:
            self.state ="off"
        return self.state
    
    def get_state(self):
        return self.state
    
    def start_buzzing(self):
        self.buzzing_stop_event = threading.Event()
        self.buzzing_thread = threading.Thread(target=buzzing_loop, args=(self.buzzing_stop_event, self.callback))
        self.buzzing_thread.start()
    
    def stop_buzzing(self):
        self.buzzing_stop_event.set()
    
    def should_stop(self):
        return self.stop_event.is_set()

    def start(self):
        t = threading.Thread(target=loop, args=(self,))
        t.start()
        return t
