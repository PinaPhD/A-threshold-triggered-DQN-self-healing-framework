# -*- coding: utf-8 -*-
"""
Created on Wed Jul 24 16:08:47 2024

@author: amwangi254
"""

# -*- coding: utf-8 -*-
"""
    Created on Wed Jul 24 14:13:22 2024
    @Project Title: Implementing self-healing autonomous software-defined OT networks in offshore wind power plants
    @Task: Observe-Orient-Decide-Act Closed Control Loop Self-healing framework
    @author: amwangi254
"""

import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
import requests
import logging
import time
import pandas as pd
from time import strftime

'''
    Interact with the ONOS and InfluxDB:
    Connecting to the primary SDN controller using a 8181 RESTful API based url and 
    BASE24 Authentication (Plain user/password credentials)
'''

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Prompting user for ONOS controller details
print("OBSERVE MODULE AS* OT Network Topology \n   Disclaimer: Press Enter if you wish to use the default configurations\n\n")
controller_ip = input("Enter the IP address of the ONOS controller (default is 192.168.0.6: )")
controller_ip = controller_ip if controller_ip else '192.168.0.6'
onos_base_url = f'http://{controller_ip}:8181/onos/v1'

username = input("Enter the username for ONOS controller (default is 'onos'): ")
username = username if username else 'onos'
password = input("Enter the password for ONOS controller (default is 'rocks'): ")
password = password if password else 'rocks'
onos_auth = (username, password)


'''
    Setting up the InfluxDB Connection
    Connection via TCP/8086 with API Token Authentication
    Bucket name: onos_metrics
    Organization: Knowledge_Base
'''

# InfluxDB configuration
url = "http://192.168.0.7:8086"  #InfluxDB URL (Host Server)
token = "qkc2ZrwHen0ZzaPyBisN9E5bZYGNmhwO9R-ATu077_ieVy9ZqrhxqvHlzmn8zS2A5iCiBTGmSUM4hz9flPX6yg=="  # InfluxDB API Token
org = "Knowledge_Base"  # InfluxDB Organization
bucket = "onos_metrics"   #Influx Bucket Name

# Initialize InfluxDB client
client = influxdb_client.InfluxDBClient(
    url=url,
    token=token,
    org=org
)

write_api = client.write_api(write_options=SYNCHRONOUS)

def get_devices():
    """ Fetches network devices from the ONOS controller. """
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

def get_links():
    """ Fetches network links from the ONOS controller. """
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

def get_hosts():
    """ Fetches network hosts from the ONOS controller. """
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

def get_flows():
    """ Fetches flow rules from the ONOS controller. """
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

def get_port_statistics():
    """ Fetches port statistics from all devices in the ONOS controller. """
    try:
        response = requests.get(f'{onos_base_url}/statistics/ports', auth=onos_auth)
        if response.status_code == 200:
            port_stats = response.json().get('statistics', [])
            df = pd.DataFrame(port_stats)
            return df
        else:
            print(f"Failed to retrieve Port Statistics: Status code {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching network port statistics: {e}")


#Determine the source to destination paths
def get_path(src,dst):
    response = requests.get(f'http://{onos_base_url}:8181/onos/v1/paths/{src}/{dst}', auth=onos_auth)
    return response.json()


def write_dataframe_to_influx(df, measurement):
    """ Writes a DataFrame to InfluxDB with a given measurement name. """
    points = []
    for _, row in df.iterrows():
        fields = {k: (str(v) if isinstance(v, dict) else v) for k, v in row.items() if pd.notnull(v)}  # Convert dicts to strings
        point = influxdb_client.Point(measurement).tag("timestamp", timestamp)
        for field_key, field_value in fields.items():
            if isinstance(field_value, (int, float, str, bool)):  # Only allow supported types
                point = point.field(field_key, field_value)
        points.append(point)
    write_api.write(bucket=bucket, org=org, record=points)
    
if __name__ == "__main__":
    
        '''
            OBSERVE MODULE
        '''
        
        devices = get_devices()
        links = get_links()
        hosts = get_hosts()
        flows = get_flows()        
       
        # Create a timestamp
        timestamp = strftime("%Y%m%d_%H%M%S")
        
        # Writing dataframes to InfluxDB
        if not devices.empty:
            write_dataframe_to_influx(devices, 'devices')
        if not links.empty:
            write_dataframe_to_influx(links, 'links')
        if not hosts.empty:
            write_dataframe_to_influx(hosts, 'hosts')
        if not flows.empty:
            # Analysing the flow information
            dp_to_cp = flows[flows['appId'] == 'org.onosproject.core']
            dp_to_dp = flows[flows['appId'] == 'org.onosproject.fwd']
            write_dataframe_to_influx(dp_to_cp, 'Switch-to-Controller-flows')
            write_dataframe_to_influx(dp_to_dp, 'Switch-to-Switch-flows')
            
        '''
            ORIENT MODULE
        '''
        port_stats = get_port_statistics()
        
        #Interpreting the port statistics to determine the current network state
        
        '''
            KNOWLEDGE BASE
        '''
        
            
       #while True:
        #   try:     
      #  time.sleep(10)  # Collect the network state every 10 seconds
