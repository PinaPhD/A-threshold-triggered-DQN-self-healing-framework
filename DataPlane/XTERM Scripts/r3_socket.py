#!/usr/bin/env python3

'''
    Designing the IIoT to Edge Computing Nodes data acquisition system
    Author: Agrippina W. Mwangi
    Created on: July 2024
    DATA PLANE: IIoT-Edge Computing Nodes 
'''


import socket
import time
import random
import json

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

def send_sensor_data():
    server_address = ('10.0.1.32', 10200)  # IP address and port of E3

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        while True:
            data = generate_sensor_data()
            message = json.dumps(data)
            print(f'Sending: {message}')
            sock.sendto(message.encode(), server_address)
            time.sleep(1)
    except KeyboardInterrupt:
        print('Interrupted!')
    finally:
        sock.close()

if __name__ == '__main__':
    send_sensor_data()
