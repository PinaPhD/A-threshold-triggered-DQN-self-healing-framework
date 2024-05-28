#!/usr/bin/python

import paho.mqtt.publish as publish
import time
import random

MQTT_BROKER = "localhost"  # Change this to the IP of your MQTT broker if it's not local
MQTT_PORT = 1883

# MQTT Topics for Wind Turbine (WT) parameters with 50Hz sampling rate
WT_topics = [
    "WT/Temp/GearOil",
    "WT/Temp/GearBearing",
    "WT/Temp/Generator",
    "WT/Temp/Nacelle",
    "WT/Temp/Ambient",
    "WT/Vibration/TowerXY",
    "WT/Displacement/ShaftVertical",
    "WT/Displacement/ShaftHorizontal",
    "WT/Displacement/Pitch",
    "WT/Speed/Rotor",
    "WT/Speed/Generator",
    "WT/Speed/WindSpeed",
    "WT/Direction/Yawing"
]

# Function to generate sensor data from the Wind Turbine 
def generate_sensor_data():
    sensor_values = {
        "GearOil": random.uniform(-20, 120),
        "GearBearing": random.uniform(-20, 150),
        "Generator": random.uniform(-20, 150),
        "Nacelle": random.uniform(-40, 70),
        "Ambient": random.uniform(-40, 45),
        "TowerXY": random.uniform(0, 5),
        "ShaftVertical": random.uniform(0, 10),
        "ShaftHorizontal": random.uniform(0, 10),
        "Pitch": random.uniform(0, 360),
        "Rotor": random.uniform(0, 30),  # Assuming 30 RPM for large wind turbines
        "Generator": random.uniform(0, 1800),  # Assuming a maximum of 1800 RPM
        "WindSpeed": random.uniform(0, 60),  # Assuming 60 m/s max wind speed
        "Yawing": random.uniform(0, 360)
    }
    return sensor_values

# Function to publish data at 50Hz
def publish_sensor_data():
    try:
        while True:
            sensor_data = generate_sensor_data()
            for topic in WT_topics:
                # Correctly extracting the last part of the topic as the sensor name
                sensor_name = topic.split('/')[-1]  # This is the actual sensor name.
                value = sensor_data.get(sensor_name, "Unknown Sensor")
                
                if value == "Unknown Sensor":
                    print(f"Sensor name '{sensor_name}' not found in sensor data.")
                    continue  # Skip this iteration if the sensor name is not found
                
                # Publish the sensor data to the topic
                publish.single(topic, payload=value, hostname=MQTT_BROKER, port=MQTT_PORT)
                print(f"Published {value:.2f} to {topic}")
            time.sleep(0.02)  # Sleep for 20 milliseconds
    except KeyboardInterrupt:
        print("\n\nPublishing stopped by publisher.\n\n")



# Run the publish function
if __name__ == '__main__':
    publish_sensor_data()
