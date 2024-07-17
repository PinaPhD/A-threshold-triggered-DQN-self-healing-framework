#!/usr/bin/env python3

'''
    Designing the IIoT to Edge Computing Nodes data acquisition system
    Author: Agrippina W. Mwangi
    Created on: July 2024
    DATA PLANE: IIoT-Edge Computing Nodes 
'''

# publisher_socket.py
import socket
import json
import time
import random
import logging
from datetime import datetime

# Setup logging
log_file = "/tmp/publisher_socket.log"
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

server_ip = "10.0.1.33"  # IP Address for the receiving ECP node (e2)
server_port = 53000  # Socket Port number

end_date = datetime(2024, 10, 31)

try:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))
    logging.info("Connected to server at %s:%d", server_ip, server_port)
    
    while datetime.now() <= end_date:
        data = generate_sensor_data()
        client_socket.sendall(json.dumps(data).encode())
        logging.info("Sent data: %s", data)
        time.sleep(2)  # Running the script every 2 seconds 
    logging.info("Reached the end date. stopping the script.")
except Exception as e:
    logging.error("An error occurred: %s", str(e))
finally:
    client_socket.close()
    logging.info("Disconnected from server")
