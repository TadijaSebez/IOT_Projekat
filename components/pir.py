
def start_pir(config, stop_event, publisher):

    def pir_callback(config):
        if 'verbose' in config and config['verbose']:
            print("Motion detected")
        
        payload = config
        payload['detected'] = True
        publisher.add_mesurement("Motion", payload)

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
