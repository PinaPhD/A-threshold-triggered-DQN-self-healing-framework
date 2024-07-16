# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 14:01:26 2024

@author: amwangi254
"""

# publisher.py
import paho.mqtt.client as mqtt
import json
import time
import random

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

broker_address = "10.0.1.30"  # Configuring ECP Node (e1) as the MQTT Broker
client = mqtt.Client("Publisher")
client.connect(broker_address)

try:
    while True:
        data = generate_sensor_data()
        client.publish("wind_turbine/data", json.dumps(data))
        time.sleep(1)  # Sends the sensor data every 1 second
finally:
    client.disconnect()
