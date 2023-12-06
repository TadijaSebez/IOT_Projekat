
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
