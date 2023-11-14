import RPi.GPIO as GPIO
import time
import threading


def loop(ms):
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(ms.R1, GPIO.OUT)
    GPIO.setup(ms.R2, GPIO.OUT)
    GPIO.setup(ms.R3, GPIO.OUT)
    GPIO.setup(ms.R4, GPIO.OUT)

    GPIO.setup(ms.C1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(ms.C2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(ms.C3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(ms.C4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    while True:
        password = ms.detect_password()
        if password != "":
            ms.callback(password)
        time.sleep(0.001)
        if ms.should_stop():
            break

class MS:

    def __init__(self, config, stop_event, callback):
        self.stop_event = stop_event
        self.callback = callback
        self.R1 = config["R1"]
        self.R2 = config["R2"]
        self.R3 = config["R3"]
        self.R4 = config["R4"]
        self.C1 = config["C1"]
        self.C2 = config["C2"]
        self.C3 = config["C3"]
        self.C4 = config["C4"]
        self.password = ""

    def read(self, line, chars):
        GPIO.output(line, GPIO.HIGH)
        if (GPIO.input(self.C1) == 1):
            self.password += chars[0]
        if (GPIO.input(self.C2) == 1):
            self.password += chars[1]
        if (GPIO.input(self.C3) == 1):
            self.password += chars[2]
        if (GPIO.input(self.C4) == 1):
            self.password += chars[3]
        GPIO.output(line, GPIO.LOW)

    def detect_password(self):
        self.read(self.R1, ["1", "2", "3", "A"])
        self.read(self.R2, ["4", "5", "6", "B"])
        self.read(self.R3, ["7", "8", "9", "C"])
        self.read(self.R4, ["*", "0", "#", "D"])
        return self.password
        
    def should_stop(self):
        return self.stop_event.is_set()

    def start(self):
        t = threading.Thread(target=loop, args=(self,))
        t.start()
        return t
