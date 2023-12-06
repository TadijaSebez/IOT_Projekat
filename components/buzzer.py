
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
