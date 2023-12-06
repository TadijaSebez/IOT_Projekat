import RPi.GPIO as GPIO
import time
import threading


def loop(uds):
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(uds.trig_pin, GPIO.OUT)
    GPIO.setup(uds.echo_pin, GPIO.IN)

    while True:
        dist = uds.detect_distance()
        if dist is not None:
            uds.callback(dist, uds.config)
        time.sleep(0.001)
        if uds.should_stop():
            break

class UDS:

    def __init__(self, config, stop_event, callback):
        self.config = config
        self.stop_event = stop_event
        self.callback = callback
        self.trig_pin = config["trig_pin"]
        self.echo_pin = config["echo_pin"]

    def get_distance(self):
        GPIO.output(self.trig_pin, False)
        time.sleep(0.2)
        GPIO.output(self.trig_pin, True)
        time.sleep(0.00001)
        GPIO.output(self.trig_pin, False)
        pulse_start_time = time.time()
        pulse_end_time = time.time()

        max_iter = 100

        iter = 0
        while GPIO.input(self.echo_pin) == 0:
            if iter > max_iter:
                return None
            pulse_start_time = time.time()
            iter += 1

        iter = 0
        while GPIO.input(self.echo_pin) == 1:
            if iter > max_iter:
                return None
            pulse_end_time = time.time()
            iter += 1

        pulse_duration = pulse_end_time - pulse_start_time
        distance = (pulse_duration * 34300)/2
        return distance

    def should_stop(self):
        return self.stop_event.is_set()

    def start(self):
        t = threading.Thread(target=loop, args=(self,))
        t.start()
        return t
