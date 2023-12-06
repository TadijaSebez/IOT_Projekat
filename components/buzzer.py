
def start_buzzer(config, stop_event, pipe, publisher):

    def buzzer_callback(config):
        if 'verbose' in config and config['verbose']:
            print("Buzzing...")

        payload = config
        payload['buzzing'] = True
        publisher.add_mesurement("Buzzer", payload)

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
