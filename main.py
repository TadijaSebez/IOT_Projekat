import json
import threading
import sys
from multiprocessing import Pipe

from components.button import start_button
from components.buzzer import start_buzzer
from components.dht import start_dht
from components.light import start_light
from components.ms import start_ms
from components.pir import start_pir
from components.uds import start_uds

from publisher import Publisher

def load_config():
    with open("settings.json", "r") as f:
        return json.load(f)
    
def start_pi1(config, pi, stop_event, threads):
    publisher = Publisher(config['mqtt'])
    publisher.start_daemon()

    config = config[pi]

    threads.append(start_button(config["DS1"], stop_event, publisher))
    light_pipe_send, light_pipe_recv = Pipe()
    threads.append(start_light(config["DL"], stop_event, light_pipe_recv, publisher))
    threads.append(start_uds(config["DUS1"], stop_event, publisher))
    buzzer_pipe_send, buzzer_pipe_recv = Pipe()
    threads.append(start_buzzer(config["DB"], stop_event, buzzer_pipe_recv, publisher))
    threads.append(start_pir(config["DPIR1"], stop_event, publisher))
    threads.append(start_ms(config["DMS"], stop_event, publisher))
    threads.append(start_pir(config["RPIR1"], stop_event, publisher))
    threads.append(start_pir(config["RPIR2"], stop_event, publisher))
    threads.append(start_dht(config["RDHT1"], stop_event, publisher))
    threads.append(start_dht(config["RDHT2"], stop_event, publisher))

    while True:
        command = input()
        if command == "e":
            stop_event.set()
            break
        elif command == "l":
            light_pipe_send.send("l")
        elif command == "b":
            buzzer_pipe_send.send("b")

def start_pi2(config, pi, stop_event, threads):
    publisher = Publisher(config['mqtt'])
    publisher.start_daemon()

    config = config[pi]

    threads.append(start_button(config["DS2"], stop_event, publisher))
    threads.append(start_uds(config["DUS2"], stop_event, publisher))
    threads.append(start_pir(config["DPIR2"], stop_event, publisher))
    threads.append(start_dht(config["GDHT"], stop_event, publisher))
    # TODO: GLCD
    # TODO: GSG
    threads.append(start_pir(config["RPIR3"], stop_event, publisher))
    threads.append(start_dht(config["RDHT3"], stop_event, publisher))

    while True:
        command = input()
        if command == "e":
            stop_event.set()
            break

def start_pi3(config, pi, stop_event, threads):
    publisher = Publisher(config['mqtt'])
    publisher.start_daemon()

    config = config[pi]

    threads.append(start_pir(config["RPIR4"], stop_event, publisher))
    threads.append(start_dht(config["RDHT4"], stop_event, publisher))
    buzzer_pipe_send, buzzer_pipe_recv = Pipe()
    threads.append(start_buzzer(config["BB"], stop_event, buzzer_pipe_recv, publisher))
    # TODO: B4SD
    # TODO: BIR
    # TODO: BRGB

    while True:
        command = input()
        if command == "e":
            stop_event.set()
            break
        elif command == "b":
            buzzer_pipe_send.send("b")

if __name__ == "__main__":
    config = load_config()

    stop_event = threading.Event()
    threads = []

    pi = sys.argv[1] if len(sys.argv) > 1 else "PI1"

    if pi == "PI1":
        start_pi1(config, pi, stop_event, threads)
    elif pi == "PI2":
        start_pi2(config, pi, stop_event, threads)
    elif pi == "PI3":
        start_pi3(config, pi, stop_event, threads)
    else:
        print("Usage: main.py [PI1/PI2/PI3]")
