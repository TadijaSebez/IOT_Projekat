
def pir_callback():
    print("Motion detected")

def start_pir(config, stop_event):
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
