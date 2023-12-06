
def uds_callback(distance):
    print("Detected distance", distance)

def start_uds(config, stop_event):
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
