# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 20:34:00 2024

@author: amwangi254
"""

import socket
import logging
import random
import time
from datetime import datetime
import json

# Setup logging
log_file = "/tmp/client_socket.log"
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s %(message)s')

client_ip = "10.0.1.50"  # LDAQ 1
server_ip_range = ["10.0.1.30", "10.0.1.31", "10.0.1.32", "10.0.1.33", "10.0.1.34"]
server_ip = random.choice(server_ip_range)
server_port = 50000

end_date = datetime(2024, 10, 31)

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

try:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))
    logging.info("Connected to server %s:%d", server_ip, server_port)
    
    while datetime.now() <= end_date:
        sensor_data = generate_sensor_data()
        data_str = json.dumps(sensor_data)
        client_socket.send(data_str.encode())
        logging.info("Sent data: %s", data_str)
        time.sleep(random.uniform(1, 5))  # Send data at random intervals
finally:
    client_socket.close()
    logging.info("Client stopped")
