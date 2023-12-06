import random
import time
import threading


def loop(dht):
    while True:
        code, humidity, temperature = dht.detect_values()
        dht.callback(humidity, temperature, code, dht.config)
        time.sleep(0.5)
        if dht.should_stop():
            break

class DHT:

    def __init__(self, config, stop_event, callback):
        self.config = config
        self.stop_event = stop_event
        self.callback = callback
        self.humidity = config["initial_humidity"] if "initial_humidity" in config else 50
        self.temperature = config["initial_temperature"] if "initial_temperature" in config else 23
        self.min_temp = config["minimum_temperature"] if "minimum_temperature" in config else -20
        self.max_temp = config["maximum_temperature"] if "maximum_temperature" in config else 70

    def detect_values(self):
        self.humidity += random.randint(-3, 3)
        self.humidity = max(0, min(100, self.humidity))
        self.temperature += random.randint(-1, 1)
        self.temperature = max(self.min_temp, min(self.max_temp, self.temperature))
        return "DHTLIB_OK", self.humidity, self.temperature
    
    def should_stop(self):
        return self.stop_event.is_set()

    def start(self):
        t = threading.Thread(target=loop, args=(self,))
        t.start()
        return t
