
def start_light(config, stop_event, pipe, publisher):

    def light_callback(state, config):
        if 'verbose' in config and config['verbose']:
            print("Light is", state)

        payload = config
        payload['state'] = state
        publisher.add_mesurement("Light", payload)

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
