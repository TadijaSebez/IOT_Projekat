import RPi.GPIO as GPIO
import time
import threading


def loop(button):
    GPIO.setup(button.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(button.pin, GPIO.RISING, callback=lambda x: button.callback(True), bouncetime=100)
    GPIO.add_event_detect(button.pin, GPIO.FALLING, callback=lambda x: button.callbac(False), bouncetime=100)
    while True:
        time.sleep(0.001)
        if button.should_stop():
            GPIO.remove_event_detect(button.pin)
            break

class Button:

    def __init__(self, config, stop_event, callback):
        self.stop_event = stop_event
        self.callback = callback
        self.pin = config["pin"]

    def should_stop(self):
        return self.stop_event.is_set()

    def start(self):
        t = threading.Thread(target=loop, args=(self,))
        t.start()
        return t
