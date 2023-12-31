import random
import time
import threading


def loop(ms):
    while True:
        password = ms.detect_password()
        if password is not None:
            ms.callback(password, ms.config)
        time.sleep(0.5)
        if ms.should_stop():
            break

class MS:

    def __init__(self, config, stop_event, callback):
        self.config = config
        self.stop_event = stop_event
        self.callback = callback
        self.max_length = config["maximum_length"] if "maximum_length" in config else 16

    def detect_password(self):
        if random.randint(0, 4) != 0:
            return None
        length = random.randint(1, self.max_length)
        password = ""
        for i in range(length):
            code = random.randint(0, 15)
            if code < 10:
                password += str(code)
            elif code == 10:
                password += "*"
            elif code == 11:
                password += "#"
            elif code == 12:
                password += "A"
            elif code == 13:
                password += "B"
            elif code == 14:
                password += "C"
            elif code == 15:
                password += "D"      
        return password
    
    def should_stop(self):
        return self.stop_event.is_set()

    def start(self):
        t = threading.Thread(target=loop, args=(self,))
        t.start()
        return t
