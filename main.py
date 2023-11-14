import json
import threading
from multiprocessing import Pipe
from starter import start_button, start_buzzer, start_dht, start_light, start_ms, start_pir, start_uds


def load_config():
    with open("settings.json", "r") as f:
        return json.load(f)
    
def start_all(config, stop_event, threads):
    threads.append(start_button(config["DS1"], stop_event))
    light_pipe_send, light_pipe_recv = Pipe()
    threads.append(start_light(config["DL"], stop_event, light_pipe_recv))
    threads.append(start_uds(config["DUS1"], stop_event))
    buzzer_pipe_send, buzzer_pipe_recv = Pipe()
    threads.append(start_buzzer(config["DB"], stop_event, buzzer_pipe_recv))
    threads.append(start_pir(config["DPIR1"], stop_event))
    threads.append(start_ms(config["DMS"], stop_event))
    threads.append(start_pir(config["RPIR1"], stop_event))
    threads.append(start_pir(config["RPIR2"], stop_event))
    threads.append(start_dht(config["RDH1"], stop_event))
    threads.append(start_dht(config["RDH2"], stop_event))

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
