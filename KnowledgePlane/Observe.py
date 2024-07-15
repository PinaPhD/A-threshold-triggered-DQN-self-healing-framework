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
from time import strftime

#OODA CCL - OBSERVE MODULE

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


#Retrieving the network devices(L2 switches)
def get_devices():
    try:
        response = requests.get(f'{onos_base_url}/devices', auth=onos_auth)
        if response.status_code == 200:
            devices = response.json().get('devices', [])
            df = pd.DataFrame(devices)
            #save_csv(df, 'devices')
            return df
        else:
            # Handle responses other than 200 OK
            print(f"Failed to retrieve Network devices: Status code {response.status_code} - {response.text}")

    except requests.exceptions.RequestException as e:
            # Handle exceptions that may occur during the request
            print(f"An error occurred while fetching Network devices: {e}")



#Retrieving the network links
def get_links():
    try:
        response = requests.get(f'{onos_base_url}/links', auth=onos_auth)
        if response.status_code == 200:
            links = response.json().get('links', [])
            df = pd.DataFrame(links)
            #save_csv(df, 'links')
            return df
        else:
            # Handle responses other than 200 OK
            print(f"Failed to retrieve Network links: Status code {response.status_code} - {response.text}")

    except requests.exceptions.RequestException as e:
            # Handle exceptions that may occur during the request
            print(f"An error occurred while fetching Network Links: {e}")


# Function to get network hosts
def get_hosts():
    try:
        response = requests.get(f'{onos_base_url}/hosts', auth=onos_auth)
        if response.status_code == 200:
            hosts = response.json().get('hosts', [])
            df = pd.DataFrame(hosts)
            #save_csv(df, 'hosts')
            return df
        else:
            # Handle responses other than 200 OK
            print(f"Failed to retrieve Network hosts: Status code {response.status_code} - {response.text}")

    except requests.exceptions.RequestException as e:
            # Handle exceptions that may occur during the request
            print(f"An error occurred while fetching Network hosts: {e}")


# Function to get flow rules
def get_flows():
    try:
        response = requests.get(f'{onos_base_url}/flows', auth=onos_auth)
        if response.status_code == 200:
            flows = response.json().get('flows', [])
            df = pd.DataFrame(flows)
            #save_csv(df, 'flows')
            return df
        else:
            # Handle responses other than 200 OK
            print(f"Failed to retrieve Network flows: Status code {response.status_code} - {response.text}")

    except requests.exceptions.RequestException as e:
            # Handle exceptions that may occur during the request
            print(f"An error occurred while fetching Network flows: {e}")


#Function to get port statistics
def get_port_statistics():
    """ Fetches port statistics from all devices in the ONOS controller. """
    try:        
        url = f'{onos_base_url}/statistics/ports'
        response = requests.get(url, auth=onos_auth)
        if response.status_code == 200:
            response.raise_for_status()  # will raise an exception for HTTP error responses
            return response.json()
        else:
            # Handle responses other than 200 OK
            print(f"Failed to retrieve Port Statistics: status code {response.status_code} - {response.text}")

    except requests.exceptions.RequestException as e:
            # Handle exceptions that may occur during the request
            print(f"An error occurred while fetching network port statistics: {e}")
            

# Function to save DataFrame to a timestamped CSV file in a timestamped folder
def save_csv(df, filename, folder_path):
    if not df.empty:
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        df.to_csv(os.path.join(folder_path, f"{filename}.csv"), index=False)
        logging.info(f"Data saved to {os.path.join(folder_path, f'{filename}.csv')}")
    else:
        logging.info(f"No data available to save for {filename}")

# Main function to display network details
if __name__ == "__main__":
    devices = get_devices()
    links = get_links()
    hosts = get_hosts()
    flows = get_flows()
    port_stats = get_port_statistics()
   
    
    # Create a timestamped folder to save the CSV files
    timestamp = strftime("%Y%m%d_%H%M%S")
    folder_path = f"network_data_{timestamp}"

    # Save DataFrames to CSV files in the timestamped folder
    save_csv(devices, 'devices', folder_path)
    save_csv(links, 'links', folder_path)
    save_csv(hosts, 'hosts', folder_path)
    save_csv(flows, 'flows', folder_path)


    '''
        Analysing the port statistics and mapping out the link utilization
    '''
    # Fields to extract for the CSV
    fieldnames = [
        'device', 'port', 'packetsReceived', 'packetsSent', 'bytesReceived',
        'bytesSent', 'packetsRxDropped', 'packetsTxDropped', 'packetsRxErrors',
        'packetsTxErrors', 'durationSec'
    ]
    
    # Write port statistics to CSV in the timestamped folder
    with open(os.path.join(folder_path, 'port_stats.csv'), 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        # Loop through each device and its ports
        for stat in port_stats['statistics']:
            device = stat['device']
            for port_info in stat['ports']:
                # Merge device info with port info
                row = {'device': device}
                row.update(port_info)
                writer.writerow(row)
    
    print(f"Data has been written to '{folder_path}'.")
    
    
    '''
       Analysing the flow information to separate data plane to control plane asynchronous
       interactions from data plane switch communication
   '''
    dp_to_cp = flows[flows['appId'] ==  'org.onosproject.core']
    dp_to_dp = flows[flows['appId'] ==  'org.onosproject.fwd']
    
