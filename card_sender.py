#!/usr/bin/env python3

import paho.mqtt.client as mqtt
import time
import RPi.GPIO as GPIO
from config import *  # pylint: disable=unused-wildcard-import
from mfrc522 import MFRC522
from PIL import Image, ImageDraw, ImageFont
import lib.oled.SSD1331 as SSD1331
from datetime import datetime

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
    client.subscribe("auth")


def disconnect_from_broker():
    client.publish("info", "Client disconnected")
    client.disconnect()


def oled_config():
    global disp
    disp = SSD1331.SSD1331()
    disp.Init()


def process_message(client, userdata, message):
    # format: "Hello" +"&"+ name+"&"+card_number

    image = Image.new("RGB", (disp.width, disp.height), "WHITE")
    draw = ImageDraw.Draw(image)
    fontSmall = ImageFont.truetype('./lib/oled/Font.ttf', 18)
    # format: "Hello" +"&"+ name+"&"+card_number
    message_decoded = (str(message.payload.decode("utf-8"))).split("&")
    if message_decoded[0] == "Unauthorized":
        draw.text((5, 20), f"Unauthorized access!", font=fontSmall, fill="BLACK")
    else:
        draw.text((5, 5), f"{message_decoded[0]} {message_decoded[1]}", font=fontSmall, fill="BLACK")
        draw.text((5, 35), f"Card UID: {message_decoded[2]}", font=fontSmall, fill="BLACK")
        buzzer()


    disp.ShowImage(image, 0, 0)


def rfidRead():
    global dt
    global prev_card
    MIFAREReader = MFRC522()
    (status, TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
    if status == MIFAREReader.MI_OK:
        dt = datetime.now()
        if prev_card == False:
            (status, uid) = MIFAREReader.MFRC522_Anticoll()
            if status == MIFAREReader.MI_OK:
                num = 0
                for i in range(0, len(uid)):
                    num += uid[i] << (i * 8)
                dt = datetime.now()
                client.publish("raspberry2/card", str(num))

                prev_card = True
                dt = datetime.now()
    else:
        if (datetime.now() - dt).total_seconds() > 0.1:
            prev_card = False
            disp.clear()


def buzzer():
    GPIO.output(buzzerPin, 0)
    time.sleep(0.5)
    GPIO.output(buzzerPin, 1)


def buttonPressedCallback(channel):
    global execute
    execute = False
    print("Red button pressed")


def run_sender():
    connect_to_broker()
    oled_config()
    GPIO.add_event_detect(buttonRed, GPIO.FALLING, callback=buttonPressedCallback, bouncetime=200)

    while execute:
        rfidRead()

    disconnect_from_broker()
    disp.clear()
    disp.reset()
    GPIO.cleanup()


if __name__ == "__main__":
    run_sender()
