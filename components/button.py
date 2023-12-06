
def start_button(config, stop_event, publisher):

    def button_callback(pressed, config):
        if 'verbose' in config and config['verbose']:
            if pressed:
                print("Button pressed")
            else:
                print("Button released")

        payload = config
        payload['pressed'] = pressed
        publisher.add_mesurement("Button", payload)

    if config["simulate"]:
        print("Simulating button")
        from simulation.button import Button
        button = Button(config, stop_event, button_callback)
    else:
        print("Starting button")
        from real.button import Button
        button = Button(config, stop_event, button_callback)
    t = button.start()
    print("Started button")
    return t
