
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
