
def start_ms(config, stop_event, publisher):

    def ms_callback(password, config):
        if 'verbose' in config and config['verbose']:
            print("Detected password", password)
        
        payload = config
        payload['password'] = password
        publisher.add_mesurement("Password", payload)

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
