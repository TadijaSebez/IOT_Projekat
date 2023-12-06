
def start_uds(config, stop_event, publisher):

    def uds_callback(distance, config):
        if 'verbose' in config and config['verbose']:
            print("Detected distance", distance)
        
        payload = config
        payload['distance'] = distance
        publisher.add_mesurement("Distance", payload)

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
