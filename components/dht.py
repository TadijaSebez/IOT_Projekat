
def start_dht(config, stop_event, publisher):

    def dht_callback(humidity, temperature, code, config):
        if 'verbose' in config and config['verbose']:
            print("Detected humidity", humidity, " and temperature", temperature, "( code", code, ")")
        
        payload = config
        payload['humidity'] = humidity
        payload['code'] = code
        publisher.add_mesurement("Humidity", payload)

        payload = config
        payload['temperature'] = temperature
        payload['code'] = code
        publisher.add_mesurement("Temperature", payload)

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
