
def light_callback(state):
    print("Light is", state)

def start_light(config, stop_event, pipe):
    if config["simulate"]:
        print("Simulating light")
        from simulation.light import Light
        light = Light(config, stop_event, light_callback, pipe)
    else:
        print("Starting light")
        from real.light import Light
        light = Light(config, stop_event, light_callback, pipe)
    t = light.start()
    print("Started light")
    return t
