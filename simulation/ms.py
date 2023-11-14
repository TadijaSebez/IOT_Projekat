import random
import time
import threading


def loop(ms):
    while True:
        password = ms.detect_password()
        if password is not None:
            ms.callback(password)
        time.sleep(0.5)
        if ms.should_stop():
            break

class MS:

    def __init__(self, config, stop_event, callback):
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
            match code:
                case num if num in range(10):
                    password += str(code)
                case 10:
                    password += "*"
                case 11:
                    password += "#"
                case 12:
                    password += "A"
                case 13:
                    password += "B"
                case 14:
                    password += "C"
                case 15:
                    password += "D"      
        return password
    
    def should_stop(self):
        return self.stop_event.is_set()

    def start(self):
        t = threading.Thread(target=loop, args=(self,))
        t.start()
        return t
