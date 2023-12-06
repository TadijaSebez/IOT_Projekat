import json
import threading
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
    
def start_all(config, stop_event, threads):
    publisher = Publisher(config['mqtt'])
    publisher.start_daemon()

    config = config['devices']

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
    threads.append(start_dht(config["RDH1"], stop_event, publisher))
    threads.append(start_dht(config["RDH2"], stop_event, publisher))

    while True:
        command = input()
        if command == "e":
            stop_event.set()
            break
        elif command == "l":
            light_pipe_send.send("l")
        elif command == "b":
            buzzer_pipe_send.send("b")

if __name__ == "__main__":
    config = load_config()

    stop_event = threading.Event()
    threads = []

    start_all(config, stop_event, threads)
