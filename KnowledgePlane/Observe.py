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
import time
import logging
import pandas as pd
from time import strftime
from datetime import datetime
import os


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
org = "Knowledge_Base"   #InfluxDB Organization
bucket = "Observe_Module_KB"   #Influx Bucket Name

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
    timestamp = strftime("%Y%m%d_%H%M%S")  # ISO 8601 format
    for _, row in df.iterrows():
        fields = {k: v for k, v in row.items() if pd.notnull(v) and not isinstance(v, (list, dict))}
        point = influxdb_client.Point(measurement).time(timestamp)
        for field_key, field_value in fields.items():
            point = point.field(field_key, field_value)
        points.append(point)
    write_api.write(bucket=bucket, org=org, record=points)


if __name__ == "__main__":
    try:
        # Reading the current network state
        devices, links, hosts, flows, port_stats, paths = current_network_state()

        # For flows (permanent and temporary flows are identified)
        dp_to_cp = flows[flows['appId'] == 'org.onosproject.core']  # Permanent
        dp_to_dp = flows[flows['appId'] == 'org.onosproject.fwd']   # Renewed periodically/Temporary

        # Create Port DataFrame
        ports = []
        for index, row in links.iterrows():
            src_device, src_port = row['src']['device'], row['src']['port']
            dest_device, dest_port = row['dst']['device'], row['dst']['port']
            ports.append({'port_identifier': f'{src_device}_{src_port}', 'device_name': src_device, 'port_number': src_port})
            ports.append({'port_identifier': f'{dest_device}_{dest_port}', 'device_name': dest_device, 'port_number': dest_port})
        
        port_df = pd.DataFrame(ports).drop_duplicates().reset_index(drop=True)

        # Create Network Links DataFrame
        network_links = []
        for index, row in links.iterrows():
            src_device, src_port = row['src']['device'], row['src']['port']
            dest_device, dest_port = row['dst']['device'], row['dst']['port']
            link_id = f'{src_device}_{src_port}_to_{dest_device}_{dest_port}'
            src_port_identifier = f'{src_device}_{src_port}'
            dest_port_identifier = f'{dest_device}_{dest_port}'
            network_links.append({'link_id': link_id, 'src_port_identifier': src_port_identifier, 'dest_port_identifier': dest_port_identifier})
        
        network_links_df = pd.DataFrame(network_links)

        # Write initial data to InfluxDB
        write_dataframe_to_influx(port_df, 'ports')
        write_dataframe_to_influx(network_links_df, 'network_links')

        # Initialize DataFrame to store link port statistics
        link_port_stats_df = pd.DataFrame(columns=['link_stats_id', 'link_id', 'timestamp', 'PacketsReceived', 'PacketsSent', 'BytesReceived', 'BytesSent', 'PacketsRxDropped', 'PacketsTxDropped', 'PacketsRxErrors', 'PacketsTxErrors'])
        
        #Writing to csv file
        # Define the file path for storing port stats
        csv_file = 'Data/port_stats.csv'
         
        # Initialize the CSV file with headers if it doesn't exist
        if not os.path.isfile(csv_file):
           with open(csv_file, 'w') as f:
               f.write('link_stats_id, link_id, timestamp, PacketsReceived, PacketsSent, BytesReceived, BytesSent, PacketsRxDropped, PacketsTxDropped, PacketsRxErrors, PacketsTxErrors\n')


        while True:
            # Update link_port_stats_df with new data
            port_stats = get_port_statistics()
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # ISO 8601 format
            #timestamp = pd.Timestamp.now()   #Captures the time when the record is being stored
            new_rows = []
            for index, row in port_stats.iterrows():
                new_rows.append({
                    'link_stats_id': f'{row["device"]}_{row["port"]}_{timestamp}',
                    'link_id': f'{row["device"]}_{row["port"]}',
                    'timestamp': timestamp,
                    'PacketsReceived': float(row.get('packetsReceived', 0)),
                    'PacketsSent': float(row.get('packetsSent', 0)),
                    'BytesReceived': float(row.get('bytesReceived', 0)),
                    'BytesSent': float(row.get('bytesSent', 0)),
                    'PacketsRxDropped': float(row.get('packetsRxDropped', 0)),
                    'PacketsTxDropped': float(row.get('packetsTxDropped', 0)),
                    'PacketsRxErrors': float(row.get('packetsRxErrors', 0)),
                    'PacketsTxErrors': float(row.get('packetsTxErrors', 0))
                })
            
            new_df = pd.DataFrame(new_rows)
            #link_port_stats_df = pd.concat([link_port_stats_df, new_df], ignore_index=True)
        
            # Write updated link_port_stats_df to InfluxDB
            print(f'\nWriting port statistics to influxdB bucket:{bucket} at: {timestamp}')
            write_dataframe_to_influx(new_df, 'link_port_stats')
            
            #Write to a csv file (Backup)
            
            new_df.to_csv(csv_file, mode='a', header=False, index=False)
            
            # Wait for 1 minute before the next iteration
            time.sleep(60)

    
    except KeyboardInterrupt:
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
            port_stats.to_excel(writer, sheet_name='Port_stats')
            port_df.to_excel(writer, sheet_name='Port')
            network_links_df.to_excel(writer, sheet_name='Network_Links')
            link_port_stats_df.to_excel(writer, sheet_name='Link_Port_Stats')
            
        print(f"\nData successfully sent to Knowledge Base and saved to {file_name}")
        print('\n\nOBSERVE MODULE NOTICE \n\n Network Engineer has interrupted the process!')
