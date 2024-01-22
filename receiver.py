#!/usr/bin/env python3

import paho.mqtt.client as mqtt
import time

# The broker name or IP address.
broker = "localhost"

# The MQTT client.
client = mqtt.Client()

def process_message(client, userdata, message):
    # Decode message.
    message_decoded = (str(message.payload.decode("utf-8")))

    print(message_decoded)

def connect_to_broker():
    # Connect to the broker.
    client.connect(broker)
    # Send message about connection.
    client.on_message = process_message
    client.loop_start()
    client.subscribe("cardID/time")

def disconnect_from_broker():
    # Disconnect the client.
    client.loop_stop()
    client.disconnect()

def run_receiver():
    connect_to_broker()
    while True:
        pass
    disconnect_from_broker()

if __name__ == "__main__":
    run_receiver()
