#!/usr/bin/env python3
import sqlite3

import paho.mqtt.client as mqtt
from gui import LaboratoryApp

import time

broker = "localhost"

# The MQTT client.
client = mqtt.Client()

def process_message(client, userdata, message):
    if message.topic == "raspberry1/temp":
        gui.temperature = float(message.payload.decode("utf-8"))
        # format: str(bme280_temperature())

    elif message.topic == "raspberry2/card":
        message_decoded = (str(message.payload.decode("utf-8")))
        user_authorization(message_decoded[0])
        # format: str(num))

    # message_decoded = (str(message.payload.decode("utf-8")))
    #
    # print(message_decoded)

def user_authorization(str_card_number):
    connection = sqlite3.connect("items.db")
    cursor = connection.cursor()
    cursor.execute("SELECT user_name FROM users WHERE card_number = ?", (str_card_number,))
    result = cursor.fetchone()

    connection.close()
    if result:
        update_staff_in_lab(str_card_number, result[0])

    else:
        client.publish("auth", "Unauthorized")

def update_staff_in_lab(card_number, name):
    
    if name in gui.staff:
        gui.staff.remove(name)
        client.publish("auth", "Goodbye" +"&"+ name+"&"+card_number)
    else:
        gui.staff.append(name)
        client.publish("auth", "Hello" + "&" + name+"&"+card_number)
def connect_to_broker():
    client.connect(broker)
    client.on_message = process_message
    client.loop_start()
    client.subscribe("raspberry2/card")
    client.subscribe("raspberry1/temp")

def disconnect_from_broker():
    client.loop_stop()
    client.disconnect()

def run_receiver():
    connect_to_broker()
    global gui
    gui = LaboratoryApp()
    disconnect_from_broker()

if __name__ == "__main__":
    run_receiver()