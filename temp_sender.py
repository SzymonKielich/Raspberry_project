#!/usr/bin/env python3

import paho.mqtt.client as mqtt
import time
import RPi.GPIO as GPIO
from config import * # pylint: disable=unused-wildcard-import
from datetime import datetime
import w1thermsensor
import time
import os
import neopixel
import board
import busio
import adafruit_bme280.advanced as adafruit_bme280

# The terminal ID - can be any string.
terminal_id = "T0"
# The broker name or IP address.
broker = "localhost"
# The MQTT client.
client = mqtt.Client()

execute = True
prev_card = False
dt = datetime.now()

def connect_to_broker():
    client.connect(broker)
    client.publish("info", "Client connected")

def disconnect_from_broker():
    client.publish("info", "Client disconnected")
    client.disconnect()

def bme280_config():
    i2c = busio.I2C(board.SCL, board.SDA)
    global bme280
    bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c, 0x76)
    bme280.sea_level_pressure = 1013.25
    bme280.standby_period = adafruit_bme280.STANDBY_TC_500
    bme280.iir_filter = adafruit_bme280.IIR_FILTER_X16

def bme280_temperature():
    bme280.overscan_temperature = adafruit_bme280.OVERSCAN_X2
    return bme280.temperature

def bme280_humidity():
    bme280.overscan_humidity = adafruit_bme280.OVERSCAN_X1
    return bme280.humidity

def bme280_pressure():
    bme280.overscan_pressure = adafruit_bme280.OVERSCAN_X16
    return bme280.pressure

def tempRead():
    client.publish("temp", str(bme280_temperature()))
    time.sleep(1)

def buttonPressedCallback(channel):
    global execute
    execute = False
    print("Red button pressed")

def run_sender():
    connect_to_broker()
    GPIO.add_event_detect(buttonRed, GPIO.FALLING, callback=buttonPressedCallback, bouncetime=200)

    while execute:
        tempRead()

    disconnect_from_broker()
    GPIO.cleanup()

if __name__ == "__main__":
    run_sender()