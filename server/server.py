from flask import Flask, jsonify, request
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import paho.mqtt.client as mqtt
import json


app = Flask(__name__)


# InfluxDB Configuration
token = "0tlbldCfzZPvLSRbtktLBbWHbu6wXQQZANmxBqAaw0Pl-dn5DzyL75krjlR_OKw8TMPqnrzHdCysI1qc-z7eAQ=="
org = "FTN"
url = "http://localhost:8086"
bucket = "example_db"
influxdb_client = InfluxDBClient(url=url, token=token, org=org)


# MQTT Configuration
mqtt_client = mqtt.Client()
mqtt_client.connect("localhost", 1883, 60)
mqtt_client.loop_start()

def on_connect(client, userdata, flags, rc):
    client.subscribe("Temperature")
    client.subscribe("Humidity")
    client.subscribe("Motion")
    client.subscribe("Distance")
    client.subscribe("Password")
    client.subscribe("Button")
    client.subscribe("Buzzer")
    client.subscribe("Light")

mqtt_client.on_connect = on_connect
mqtt_client.on_message = lambda client, userdata, msg: save_to_db(msg.topic, json.loads(msg.payload.decode('utf-8')))

tags = ["simulated", "runs_on", "name", "verbose", "pin"]

def save_to_db(topic, data):
    write_api = influxdb_client.write_api(write_options=SYNCHRONOUS)
    point = Point(topic)
        
    for key, value in data.items():
        if key in tags:
            point = point.tag(key, value)
        else:
            point = point.field(key, value)
    
    write_api.write(bucket=bucket, org=org, record=point)

if __name__ == '__main__':
    app.run(debug=True)
