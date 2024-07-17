# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 21:53:24 2024

@author: amwangi254
"""

import paho.mqtt.client as mqtt
import json
import time
import random
import logging
import os
from datetime import datetime

# Setup logging
log_file = "/home/amwangi254/Documents/jp3/DataPlane/logs/publisher.log"
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s %(message)s')

def generate_sensor_data():
    data = {
        "turbine_operational_data": {
            "rotor_speed": round(random.uniform(5, 25), 2),
            "blade_pitch_angle": round(random.uniform(0, 90), 2),
            "power_output": round(random.uniform(0, 5), 2),
            "generator_speed": round(random.uniform(1000, 2000), 2),
            "gearbox_temperature": round(random.uniform(40, 100), 2)
        },
        "protection_and_control_traffic": {
            "circuit_breaker_status": random.choice(["open", "closed"]),
            "protection_relay_status": random.choice(["normal", "tripped"]),
            "control_commands": random.choice(["start", "stop"])
        },
        "condition_monitoring_data": {
            "vibration_levels": round(random.uniform(0, 5), 2),
            "oil_quality": round(random.uniform(0, 100), 2),
            "bearing_temperature": round(random.uniform(40, 90), 2),
            "structural_integrity": round(random.uniform(0, 100), 2)
        },
        "meteorological_data": {
            "wind_speed": round(random.uniform(0, 25), 2),
            "wind_direction": round(random.uniform(0, 360), 2),
            "ambient_temperature": round(random.uniform(-10, 35), 2),
            "humidity": round(random.uniform(0, 100), 2)
        },
        "event_driven_maintenance_data": {
            "maintenance_alerts": random.choice(["none", "minor", "major"]),
            "fault_logs": random.choice(["none", "minor fault", "major fault"]),
            "component_replacement_records": random.choice(["none", "gearbox", "bearing", "blade"])
        }
    }
    return data

def should_continue_running():
    current_date = datetime.now()
    end_date = datetime(2024, 10, 30)
    return current_date <= end_date

broker_address = "10.0.1.20"  # Eclipse Mosquitto MQTT broker (Q1)
broker_port = 1883  # Default MQTT port
client = mqtt.Client("Publisher")

try:
    client.connect(broker_address, broker_port)
    logging.info("Connected to the MQTT broker at %s:%d", broker_address, broker_port)
    
    while should_continue_running():
        data = generate_sensor_data()
        client.publish("wind_turbine/data", json.dumps(data))
        logging.info("Published data: %s", data)
        time.sleep(2)  # Publish sensor data every 2 seconds
except Exception as e:
    logging.error("An error occurred: %s", str(e))
finally:
    client.disconnect()
    logging.info("Disconnected from the MQTT broker")

logging.info("Script stopped running as the date exceeded 30th October 2024")
