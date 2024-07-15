'''
	Secure self-healing software-defined industrial OT networks for extreme environments.
	@Author: Agrippina W. Mwangi
	@DateCreated: 30-05-2024
	@Task Description: 
				- Observe and Orient modules of the ETSI ZSM framework for the self-healing module
'''

#!pip install requests networkx pyvis

import requests
import json
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
from pyvis.network import Network

# Define the ONOS API base URL and authentication
onos_base_url = 'http://192.168.0.4:8181/onos/v1'
onos_auth = ('onos', 'rocks')

# Function to get network devices
def get_devices():
    response = requests.get(f'{onos_base_url}/devices', auth=onos_auth)
    devices = response.json().get('devices', [])
    return pd.DataFrame(devices)

# Function to get network links
def get_links():
    response = requests.get(f'{onos_base_url}/links', auth=onos_auth)
    links = response.json().get('links', [])
    return pd.DataFrame(links)

# Function to get network hosts
def get_hosts():
    response = requests.get(f'{onos_base_url}/hosts', auth=onos_auth)
    hosts = response.json().get('hosts', [])
    return pd.DataFrame(hosts)

# Function to get flow rules
def get_flows():
    response = requests.get(f'{onos_base_url}/flows', auth=onos_auth)
    flows = response.json().get('flows', [])
    return pd.DataFrame(flows)

# Main function to display network details
devices = get_devices()
links = get_links()
hosts = get_hosts()
flows = get_flows()


#Network Topology Switches
#devices
#links
#hosts
#flows

#Mapping out the network topology using Directed graphs
# Create network graph
G = nx.Graph()

# Add devices as nodes
for index, row in devices.iterrows():
    G.add_node(row['id'], label=row['type'], color='magenta')

# Add hosts as nodes, colored black
for index, row in hosts.iterrows():
    host_id = row['id']
    G.add_node(host_id, label='Host', color='black')

    # Optionally connect hosts to their respective devices
    if 'locations' in row:
        for location in row['locations']:
            device_id = location['elementId']
            G.add_edge(host_id, device_id, color='gray')

# Add links as edges
for index, row in links.iterrows():
    G.add_edge(row['src']['device'], row['dst']['device'], color='blue')

# Node positions using spring layout
pos = nx.spring_layout(G)

# Set up the plot size
plt.figure(figsize=(8, 8))  # Set the figure size in inches (width, height)

# Drawing nodes and edges with labels
node_colors = [G.nodes[n]['color'] for n in G]
edge_colors = [G[u][v]['color'] for u, v in G.edges]
nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=100, edge_color=edge_colors, linewidths=1, font_size=5)

# Show plot
plt.title('AS1 WF1 OSS1 Spine-Leaf Network Topology')
plt.axis('off')  # Hide axes
plt.show()


#Interactive network topology
net = Network(notebook=True, height="800px", width="100%")

# Adding devices, hosts, and links to the network
for _, row in devices.iterrows():
    net.add_node(row['id'], label=row['type'], color='skyblue')

for _, row in hosts.iterrows():
    net.add_node(row['id'], label='Host', color='black')
    if 'locations' in row:
        for location in row['locations']:
            net.add_edge(row['id'], location['elementId'], color='gray')

for _, row in links.iterrows():
    net.add_edge(row['src']['device'], row['dst']['device'], color='blue')

# Setting the physics for the network visualization
net.set_options("""
{
  "physics": {
    "barnesHut": {
      "gravitationalConstant": -8000,
      "centralGravity": 0.3,
      "springLength": 100,
      "springConstant": 0.04,
      "damping": 0.09,
      "avoidOverlap": 0.1
    }
  }
}
""")

# Display the network
net.show("network.html")
