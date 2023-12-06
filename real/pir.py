import RPi.GPIO as GPIO
import time
import threading


def loop(pir):
    GPIO.setup(pir.pin, GPIO.IN)
    GPIO.add_event_detect(pir.pin, GPIO.RISING, callback=lambda x: pir.callback(pir.config))
    while True:
        time.sleep(0.001)
        if pir.should_stop():
            GPIO.remove_event_detect(pir.pin)
            break

class PIR:

    def __init__(self, config, stop_event, callback):
        self.config = config
        self.stop_event = stop_event
        self.callback = callback
        self.pin = config["pin"]

    def should_stop(self):
        return self.stop_event.is_set()

    def start(self):
        t = threading.Thread(target=loop, args=(self,))
        t.start()
        return t
