
def button_callback(pressed):
    if pressed:
        print("Button pressed")
    else:
        print("Button released")

def start_button(config, stop_event):
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
