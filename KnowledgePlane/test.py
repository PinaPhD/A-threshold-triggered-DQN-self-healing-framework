#!/usr/bin/env python3

'''
    Designing the offshore wind farm network topology using the spine-leaf network topology
    Author: Agrippina W. Mwangi
    Created on: April 2024
    OBSERVE: NETWORK MONITORING MODULE
'''

import requests
import logging
import csv
import os
import pandas as pd
import redis
from time import strftime

# OODA CCL - OBSERVE MODULE

'''
    READING THE NETWORK STATE:
    Connecting to the primary SDN controller using a 8181 RESTful API based url and 
    BASE24 Authentication (Plain user/password credentials)
'''

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Prompting user for ONOS controller details
controller_ip = input("Enter the IP address of the ONOS controller (default is 192.168.0.7): ")
controller_ip = controller_ip if controller_ip else '192.168.0.7'
onos_base_url = f'http://{controller_ip}:8181/onos/v1'

username = input("Enter the username for ONOS controller (default is 'onos'): ")
username = username if username else 'onos'
password = input("Enter the password for ONOS controller (default is 'rocks'): ")
password = password if password else 'rocks'
onos_auth = (username, password)

# Redis configuration
redis_host = input("Enter the Redis host (default is 'localhost'): ")
redis_host = redis_host if redis_host else 'localhost'
redis_port = input("Enter the Redis port (default is 6379): ")
redis_port = int(redis_port) if redis_port else 6379
redis_db = input("Enter the Redis database number (default is 0): ")
redis_db = int(redis_db) if redis_db else 0

# Connect to Redis
r = redis.StrictRedis(host=redis_host, port=redis_port, db=redis_db)

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

# Function to save DataFrame to Redis
def save_to_redis(df, key):
    if not df.empty:
        df_json = df.to_json(orient='records')
        r.set(key, df_json)
        logging.info(f"Data saved to Redis under key '{key}'")
    else:
        logging.info(f"No data available to save for key '{key}'")

# Main function to display network details
if __name__ == "__main__":
    devices = get_devices()
    links = get_links()
    hosts = get_hosts()
    flows = get_flows()
    port_stats = get_port_statistics()
   
    # Create a timestamp
    timestamp = strftime("%Y%m%d_%H%M%S")

    # Save DataFrames to Redis with timestamped keys
    save_to_redis(devices, f'devices_{timestamp}')
    save_to_redis(links, f'links_{timestamp}')
    save_to_redis(hosts, f'hosts_{timestamp}')
    save_to_redis(flows, f'flows_{timestamp}')

    # Fields to extract for the CSV
    fieldnames = [
        'device', 'port', 'packetsReceived', 'packetsSent', 'bytesReceived',
        'bytesSent', 'packetsRxDropped', 'packetsTxDropped', 'packetsRxErrors',
        'packetsTxErrors', 'durationSec'
    ]
    
    # Write port statistics to Redis
    port_stats_key = f'port_stats_{timestamp}'
    for stat in port_stats['statistics']:
        device = stat['device']
        for port_info in stat['ports']:
            row = {'device': device}
            row.update(port_info)
            r.rpush(port_stats_key, row)

    print(f"Data has been saved to Redis with keys '{timestamp}'.")

    # Analysing the flow information
    dp_to_cp = flows[flows['appId'] == 'org.onosproject.core']
    dp_to_dp = flows[flows['appId'] == 'org.onosproject.fwd']
