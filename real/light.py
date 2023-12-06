import RPi.GPIO as GPIO
import time
import threading


def loop(light):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(light.pin, GPIO.OUT)
    while True:
        try:
            command = light.pipe.recv()
        except:
            break
        if command == "l":
            light.change_state()
        state = light.get_state()
        light.callback(state, light.config)
        time.sleep(0.001)
        if light.should_stop():
            break

class Light:

    def __init__(self, config, stop_event, callback, pipe):
        self.config = config
        self.stop_event = stop_event
        self.callback = callback
        self.pipe = pipe
        self.state = "off"
        self.pin = config["pin"]

    def change_state(self):
        if self.state == "off":
            self.state = "on"
            GPIO.output(self.pin, GPIO.HIGH)
        else:
            self.state ="off"
            GPIO.output(self.pin, GPIO.LOW)
        return self.state
    
    def get_state(self):
        return self.state
    
    def should_stop(self):
        return self.stop_event.is_set()

    def start(self):
        t = threading.Thread(target=loop, args=(self,))
        t.start()
        return t
