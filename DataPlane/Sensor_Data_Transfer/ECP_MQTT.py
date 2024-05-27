#!/usr/bin/python

import paho.mqtt.client as mqtt
import random

# MQTT Broker settings
MQTT_BROKER = "localhost"  # Change this to the IP of your MQTT broker if it's not local
MQTT_PORT = 1883

# Define your topic lists
WT_topics = [
    "WT/Temp/GearOil",
    "WT/Temp/GearBearing",
    "WT/Temp/Generator",
    "WT/Temp/Nacelle",
    "WT/Temp/Ambient",
    "WT/TowerVibration/XY",
    "WT/ShaftDisplacement/Vertical",
    "WT/ShaftDisplacement/Horizontal",
    "WT/PitchPosition",
    "WT/RotorSpeed",
    "WT/GeneratorSpeed",
    "WT/WindSpeed",
    "WT/YawingDirection"
]

# Additional MQTT Topics for parameters with 20kHz sampling rate
high_freq_topics = [
    "WT/EC/Va", "WT/EC/Vb","WT/EC/Vc",
    "WT/EC/Ia","WT/EC/Ib","WT/EC/Ic",
    "WT/Vibration",
    "WT/Displacement"
]


# Combine all topics for subscription
all_topics = WT_topics + high_freq_topics
# Convert to a list of tuples with QoS level 0 for each topic
mqtt_topics = [(topic, 0) for topic in all_topics]

# Define callback functions for the MQTT client
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    # Subscribe to all topics
    for topic in mqtt_topics:
        client.subscribe(topic)

def on_message(client, userdata, msg):
    print(f"Received '{msg.payload.decode()}' from '{msg.topic}' topic")

# Set up the MQTT client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

try:
    # Connect to the MQTT broker
    client.connect(MQTT_BROKER, MQTT_PORT, 60)

    # Start the MQTT client
    client.loop_forever()
except KeyboardInterrupt:
    print("\n\nSubscription stopped by O&M Personnel\n\n")
    client.disconnect()
