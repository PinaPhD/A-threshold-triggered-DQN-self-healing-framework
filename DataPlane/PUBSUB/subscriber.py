# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 22:13:15 2024

@author: amwangi254
"""

import paho.mqtt.client as mqtt
import json
import time
import logging
import os
from datetime import datetime

# Setup logging
log_file = "/home/amwangi254/Documents/jp3/DataPlane/logs/subscriber.log"
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s %(message)s')

def on_message(client, userdata, message):
    logging.info("Received message: %s", message.payload.decode())

def should_continue_running():
    current_date = datetime.now()
    end_date = datetime(2024, 10, 30)
    return current_date <= end_date

broker_address = "10.0.1.20"   # Eclipse Mosquitto MQTT broker (Q1)
client = mqtt.Client("Subscriber")

client.on_message = on_message

try:
    client.connect(broker_address)
    logging.info("Connected to broker at %s", broker_address)
    client.subscribe("wind_turbine/data")
    client.loop_start()

    while should_continue_running():
        time.sleep(5)  # Adjust the sleep time as needed
except Exception as e:
    logging.error("An error occurred: %s", str(e))
finally:
    client.loop_stop()
    client.disconnect()
    logging.info("Disconnected from broker")

logging.info("Script stopped running as the date exceeded 30th October 2024")
