#!/usr/bin/env python3

'''
    Designing the offshore wind farm network topology using the spine-leaf network topology
    Author: Agrippina W. Mwangi
    Created on: April 2024
    OBSERVE: NETWORK MONITORING MODULE
'''

import requests
import logging
import pandas as pd
from time import strftime
from influxdb import InfluxDBClient

# OODA CCL - OBSERVE MODULE

'''
    READING THE NETWORK STATE:
    Connecting to the primary SDN controller using a 8181 RESTful API based url and 
    BASE24 Authentication (Plain user/password credentials)
'''

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Prompting user for ONOS controller details
controller_ip = input("Enter the IP address of the ONOS controller (default is 192.168.0.6: ")
controller_ip = controller_ip if controller_ip else '192.168.0.6'
onos_base_url = f'http://{controller_ip}:8181/onos/v1'

username = input("Enter the username for ONOS controller (default is 'onos'): ")
username = username if username else 'onos'
password = input("Enter the password for ONOS controller (default is 'rocks'): ")
password = password if password else 'rocks'
onos_auth = (username, password)

#InfluxdB connection settings
influx_client = InfluxDBClient(host='192.168.0.10', port=8086, username='admin', password='50acresIsinya', database='onos_metrics')


# Retrieving the network devices(L2 switches)
def get_devices():
    try:
        response = requests.get(f'{onos_base_url}/devices', auth=onos_auth)
        if response.status_code == 200:
            devices = response.json().get('devices', [])
            df = pd.DataFrame(devices)
            return df
        else:
            print(f"Failed to retrieve Network devices: Status code {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching Network devices: {e}")

# Retrieving the network links
def get_links():
    try:
        response = requests.get(f'{onos_base_url}/links', auth=onos_auth)
        if response.status_code == 200:
            links = response.json().get('links', [])
            df = pd.DataFrame(links)
            return df
        else:
            print(f"Failed to retrieve Network links: Status code {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching Network Links: {e}")

# Function to get network hosts
def get_hosts():
    try:
        response = requests.get(f'{onos_base_url}/hosts', auth=onos_auth)
        if response.status_code == 200:
            hosts = response.json().get('hosts', [])
            df = pd.DataFrame(hosts)
            return df
        else:
            print(f"Failed to retrieve Network hosts: Status code {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching Network hosts: {e}")

# Function to get flow rules
def get_flows():
    try:
        response = requests.get(f'{onos_base_url}/flows', auth=onos_auth)
        if response.status_code == 200:
            flows = response.json().get('flows', [])
            df = pd.DataFrame(flows)
            return df
        else:
            print(f"Failed to retrieve Network flows: Status code {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching Network flows: {e}")

# Function to get port statistics
def get_port_statistics():
    """ Fetches port statistics from all devices in the ONOS controller. """
    try:        
        url = f'{onos_base_url}/statistics/ports'
        response = requests.get(url, auth=onos_auth)
        if response.status_code == 200:
            response.raise_for_status()  # will raise an exception for HTTP error responses
            return response.json()
        else:
            print(f"Failed to retrieve Port Statistics: status code {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching network port statistics: {e}")


def write_to_influx(dataframe, measurement_name):
    json_body = [
        {
            "measurement": measurement_name,
            "time": strftime("%Y-%m-%dT%H:%M:%SZ"),  # ISO8601 format
            "fields": row.to_dict()
        }
        for index, row in dataframe.iterrows()
    ]
    influx_client.write_points(json_body)


# Main function to display network details
if __name__ == "__main__":
    devices = get_devices()
    links = get_links()
    hosts = get_hosts()
    flows = get_flows()
    port_stats = get_port_statistics()
   
    # Create a timestamp
    timestamp = strftime("%Y%m%d_%H%M%S")
    
    # Analysing the flow information
    dp_to_cp = flows[flows['appId'] == 'org.onosproject.core']
    dp_to_dp = flows[flows['appId'] == 'org.onosproject.fwd']

    # Write data to InfluxDB
    write_to_influx(devices, "devices")
    write_to_influx(links, "links")
    write_to_influx(hosts, "hosts")
    write_to_influx(flows, "flows")
    write_to_influx(pd.DataFrame(port_stats), "port_stats")
