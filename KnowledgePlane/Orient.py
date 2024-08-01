#!/usr/bin/env python3

'''
	Designing the offshore wind farm network topology using the spine-leaf network topology
    Author: Agrippina W. Mwangi
    Created on: July 2024
    ORIENT MODULE: Visualizing the network topology based on the current network state
'''


from Observe import current_network_state  #Loads the current network state from the OBSERVE Module
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

'''
    Visualize the network topology
'''

def create_network_graph(devices, links):
    
    # Formatting the links dataframe to capture source and destination ports
    if not links.empty:
        links['src_device'] = links['src'].apply(lambda x: eval(x)['device'])
        links['dst_device'] = links['dst'].apply(lambda x: eval(x)['device'])
        
        
    G = nx.Graph()

    # Add devices as nodes
    for index, device in devices.iterrows():
        G.add_node(device['id'], label=device['id'])

    # Add links as edges
    for index, link in links.iterrows():
        src = link['src_device']
        dst = link['dst_device']
        G.add_edge(src, dst)

    return G

def draw_network_graph(G):
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=50, edge_color='gray', font_size=8)
    plt.title('Network Topology')
    plt.show()

def create_topology_matrix(G):
    matrix = nx.adjacency_matrix(G).todense()
    return pd.DataFrame(matrix, index=G.nodes(), columns=G.nodes())


if __name__ == "__main__":
    # Get network state variables from file1.py
    devices, links, hosts, flows, port_stats, paths = current_network_state()
    
    # Create and draw network graph
    G = create_network_graph(devices, links)
    draw_network_graph(G)
    topology_matrix = create_topology_matrix(G)
    print("Topology Matrix:")
    print(topology_matrix)
