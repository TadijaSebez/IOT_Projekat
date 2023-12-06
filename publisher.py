import threading
import json
import paho.mqtt.publish as publish


def publisher_task(publisher, event):
    while True:
        event.wait()
        with publisher.lock:
            local_batch = publisher.batch.copy()
            publisher.currrent_size = 0
            publisher.batch.clear()
        publish.multiple(local_batch, hostname=publisher.hostname, port=publisher.port)
        print(f'published {publisher.batch_size} values')
        event.clear()


class Publisher:
    def __init__(self, config):
        self.hostname = config['hostname']
        self.port = config['port']
        self.batch_size = config['batch_size'] if 'batch_size' in config else 5

        self.batch = []
        self.current_size = 0
        self.lock = threading.Lock()
        self.publish_event = threading.Event()

    def start_daemon(self):
        publisher_thread = threading.Thread(target=publisher_task, args=(self, self.publish_event))
        publisher_thread.daemon = True
        publisher_thread.start()

    def add_mesurement(self, topic, payload):
        with self.lock:
            self.batch.append((topic, json.dumps(payload), 0, True))
            self.current_size += 1

        if self.current_size >= self.batch_size:
            self.publish_event.set()

