# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 14:16:44 2024

@author: amwangi254
"""

import paho.mqtt.client as mqtt

def on_message(client, userdata, message):
    print(f"Received message: {message.payload.decode()}")

broker_address = "10.0.1.30"  # Configuring ECP Node (e1) as the MQTT Broker
client = mqtt.Client("Subscriber")
client.connect(broker_address)
client.subscribe("wind_turbine/data")
client.on_message = on_message

client.loop_forever()
