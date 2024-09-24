#!/usr/bin/env python3

'''
	Designing the offshore wind farm network topology using the spine-leaf network topology
    Author: Agrippina W. Mwangi
    Created on: July 2024
    ACT MODULE: Enters flows into the network
'''


import requests
import json

# ONOS Controller information
ONOS_IP = "192.168.0.6"
ONOS_PORT = 8181
USERNAME = "onos"
PASSWORD = "rocks"

# Headers for the REST API
HEADERS = {
    "Content-Type": "application/json"
}

# Function to add a flow entry
def add_flow(device_id, output_port, src_mac, dst_mac):
    url = f"http://{ONOS_IP}:{ONOS_PORT}/onos/v1/flows"
    flow = {
        "priority": 40000,
        "timeout": 0,
        "isPermanent": True,
        "deviceId": device_id,
        "treatment": {
            "instructions": [
                {
                    "type": "OUTPUT",
                    "port": output_port
                }
            ]
        },
        "selector": {
            "criteria": [
                {
                    "type": "ETH_DST",
                    "mac": dst_mac
                },
                {
                    "type": "ETH_SRC",
                    "mac": src_mac
                }
            ]
        }
    }
    response = requests.post(url, data=json.dumps(flow), headers=HEADERS, auth=(USERNAME, PASSWORD))
    if response.status_code == 201:
        print(f"Flow added to {device_id} successfully.")
    else:
        print(f"Failed to add flow to {device_id}: {response.text}")










# Example scenario: Host A to Host B via S1 -> S2 -> S3
# Host A MAC: 00:00:00:00:00:01
# Host B MAC: 00:00:00:00:00:02

# Switch S1
device_id_s1 = "of:0000000000000001"
output_port_s1 = "2"
add_flow(device_id_s1, output_port_s1, "00:00:00:00:00:01", "00:00:00:00:00:02")

# Switch S2
device_id_s2 = "of:0000000000000002"
output_port_s2 = "3"
add_flow(device_id_s2, output_port_s2, "00:00:00:00:00:01", "00:00:00:00:00:02")

# Switch S3
device_id_s3 = "of:0000000000000003"
output_port_s3 = "1"
add_flow(device_id_s3, output_port_s3, "00:00:00:00:00:01", "00:00:00:00:00:02")

# Function to retrieve and print all flows
def get_flows():
    url = f"http://{ONOS_IP}:{ONOS_PORT}/onos/v1/flows"
    response = requests.get(url, headers=HEADERS, auth=(USERNAME, PASSWORD))
    if response.status_code == 200:
        flows = response.json()
        print(json.dumps(flows, indent=4))
    else:
        print(f"Failed to retrieve flows: {response.text}")

# Retrieve and print all flows
get_flows()
