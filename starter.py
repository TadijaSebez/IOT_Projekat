
def button_callback(pressed):
    if pressed:
        print("Button pressed")
    else:
        print("Button released")

def start_button(config, stop_event):
    if config["simulate"]:
        print("Simulating button")
        from simulation.button import Button
        button = Button(config, stop_event, button_callback)
    else:
        print("Starting button")
        from real.button import Button
        button = Button(config, stop_event, button_callback)
    t = button.start()
    print("Started button")
    return t


def light_callback(state):
    print("Light is", state)

def start_light(config, stop_event, pipe):
    if config["simulate"]:
        print("Simulating light")
        from simulation.light import Light
        light = Light(config, stop_event, light_callback, pipe)
    else:
        print("Starting light")
        from real.light import Light
        light = Light(config, stop_event, light_callback, pipe)
    t = light.start()
    print("Started light")
    return t


def uds_callback(distance):
    print("Detected distance", distance)

def start_uds(config, stop_event):
    if config["simulate"]:
        print("Simulating uds")
        from simulation.uds import UDS
        uds = UDS(config, stop_event, uds_callback)
    else:
        print("Starting uds")
        from real.uds import UDS
        uds = UDS(config, stop_event, uds_callback)
    t = uds.start()
    print("Started uds")
    return t


def buzzer_callback():
    print("Buzzing...")

def start_buzzer(config, stop_event, pipe):
    if config["simulate"]:
        print("Simulating buzzer")
        from simulation.buzzer import Buzzer
        buzzer = Buzzer(config, stop_event, buzzer_callback, pipe)
    else:
        print("Starting buzzer")
        from real.buzzer import Buzzer
        buzzer = Buzzer(config, stop_event, buzzer_callback, pipe)
    t = buzzer.start()
    print("Started buzzer")
    return t


def pir_callback():
    print("Motion detected")

def start_pir(config, stop_event):
    if config["simulate"]:
        print("Simulating pir")
        from simulation.pir import PIR
        pir = PIR(config, stop_event, pir_callback)
    else:
        print("Starting pir")
        from real.pir import PIR
        pir = PIR(config, stop_event, pir_callback)
    t = pir.start()
    print("Started pir")
    return t


def ms_callback(password):
    print("Detected password", password)

def start_ms(config, stop_event):
    if config["simulate"]:
        print("Simulating ms")
        from simulation.ms import MS
        ms = MS(config, stop_event, ms_callback)
    else:
        print("Starting ms")
        from real.ms import MS
        ms = MS(config, stop_event, ms_callback)
    t = ms.start()
    print("Started ms")
    return t


def dht_callback(humidity, temperature, code):
    print("Detected humidity", humidity, " and temperature", temperature, "( code", code, ")")

def start_dht(config, stop_event):
    if config["simulate"]:
        print("Simulating dht")
        from simulation.dht import DHT
        dht = DHT(config, stop_event, dht_callback)
    else:
        print("Starting dht")
        from real.dht import DHT
        dht = DHT(config, stop_event, dht_callback)
    t = dht.start()
    print("Started dht")
    return t
