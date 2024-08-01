
# -*- coding: utf-8 -*-

''' 
        Created on Wed Jul 24 14:13:22 2024
        @Project Title: Implementing self-healing autonomous software-defined OT networks in offshore wind power plants
        @Task: Observe-Orient-Decide-Act Closed Control Loop Self-healing framework
        @author: amwangi254
'''

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
            # Flatten the nested JSON structure for easier CSV writing
            flattened_stats = []
            for device in port_stats:
                device_id = device['device']
                for port in device['ports']:
                    port['device'] = device_id
                    flattened_stats.append(port)
            df = pd.DataFrame(flattened_stats)
            return df
        else:
            print(f"Failed to retrieve Port Statistics: Status code {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching network port statistics: {e}")


#For the paths
def get_devices_fp():
    response = requests.get(f'{onos_base_url}/devices', auth=onos_auth)
    return response.json()

# Function to get links
def get_links_fp():
    response = requests.get(f'{onos_base_url}/links', auth=onos_auth)
    return response.json()

#Determine the source to destination paths
def find_all_paths(graph, start, end, path=[]):
    path = path + [start]
    if start == end:
        return [path]
    if start not in graph:
        return []
    paths = []
    for node in graph[start]:
        if node not in path:
            newpaths = find_all_paths(graph, node, end, path)
            for newpath in newpaths:
                paths.append(newpath)
    return paths

# Generating the links between the source and destination paths
def src_to_dest_paths():
    devices = get_devices_fp()['devices']
    links = get_links_fp()['links']
    
    # Build adjacency list for the graph
    graph = {}
    for link in links:
        src = link['src']['device']
        dst = link['dst']['device']
        if src not in graph:
            graph[src] = []
        if dst not in graph:
            graph[dst] = []
        graph[src].append(dst)
        graph[dst].append(src)
    
    # Iterate over each pair of devices to find all paths
    device_ids = [device['id'] for device in devices]
    paths_list = []
    
    for i in range(len(device_ids)):
        for j in range(i + 1, len(device_ids)):
            source_device = device_ids[i]
            destination_device = device_ids[j]
            
            # Find all paths
            paths = find_all_paths(graph, source_device, destination_device)
            
            # Store paths
            for path in paths:
                paths_list.append({
                    'source': source_device,
                    'destination': destination_device,
                    'path': " -> ".join(path)
                })

    df_paths = pd.DataFrame(paths_list)
    return df_paths

def current_network_state():
    devices = get_devices()
    links = get_links()
    hosts = get_hosts()
    flows = get_flows()
    port_stats = get_port_statistics()
    paths = src_to_dest_paths()
        
    return devices, links, hosts, flows, port_stats, paths

def write_dataframe_to_influx(df, measurement):
    """Writes a DataFrame to InfluxDB with a given measurement name."""
    points = []
    timestamp = strftime("%Y-%m-%dT%H:%M:%SZ")  # ISO 8601 format
    for _, row in df.iterrows():
        fields = {k: v for k, v in row.items() if pd.notnull(v) and not isinstance(v, (list, dict))}
        point = influxdb_client.Point(measurement).time(timestamp)
        for field_key, field_value in fields.items():
            point = point.field(field_key, field_value)
        points.append(point)
    write_api.write(bucket=bucket, org=org, record=points)


if __name__ == "__main__": 
    
    #Reading the current network state
    devices, links, hosts, flows, port_stats, paths = current_network_state()

    #For flows (permanent and temporary flows are identified)
    dp_to_cp = flows[flows['appId'] == 'org.onosproject.core']  #Permanent
    dp_to_dp = flows[flows['appId'] == 'org.onosproject.fwd']   #Renewed periodically/Temporary
    
    try:
        # Save to Excel spreadsheets with different sheets
        while True:
            if not devices.empty and not links.empty and not hosts.empty and not flows.empty and not port_stats.empty:
                # Create a timestamp
                timestamp = strftime("%Y%m%d_%H%M%S")
                file_name = f'Data/network_data_{timestamp}.xlsx'
                with pd.ExcelWriter(file_name) as writer:
                    devices.to_excel(writer, sheet_name='Devices')
                    links.to_excel(writer, sheet_name='Links')
                    hosts.to_excel(writer, sheet_name='Hosts')
                    dp_to_dp.to_excel(writer, sheet_name='FD_to_FD_Flows')
                    dp_to_cp.to_excel(writer, sheet_name='FD_to_SDNC_Flows')
                    paths.to_excel(writer, sheet_name='Paths')
                print(f"Data successfully sent to Knowledge Base and saved to {file_name}")
                # Sleep for a predefined interval before the next iteration
                time.sleep(5)  # Check the state of the topology matrix every 5 seconds
            else:
                error_message = "Network topology is faulty because the following components are empty: "
                if devices.empty:
                    error_message += "devices "
                if links.empty:
                    error_message += "links "
                if hosts.empty:
                    error_message += "hosts "
                if flows.empty:
                    error_message += "flows "
                if port_stats.empty:
                    error_message += "port_stats "
                
                # Raise an alarm with the error message
                raise Exception(error_message)
    
    except KeyboardInterrupt:
        print('\n\nOBSERVE MODULE NOTICE \n\n Network Engineer has interrupted the process ')
