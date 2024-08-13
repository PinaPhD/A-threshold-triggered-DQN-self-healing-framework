#!/usr/bin/env python3

'''
    Designing the offshore wind farm network topology using the spine-leaf network topology
    Author: Agrippina W. Mwangi
    Created on: July 2024
    ORIENT MODULE: Visualizing the network topology based on the current network state
'''

from Observe import current_network_state  # Loads the current network state from the OBSERVE Module
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

'''
    Visualize the network topology
'''

def visualize_network(devices, links, hosts):
    """Visualizes the network topology using NetworkX and Matplotlib."""
    G = nx.Graph()
    
    # Add device nodes
    for _, device in devices.iterrows():
        G.add_node(device['id'], label=device['id'], color='skyblue')
    
    # Add host nodes and their edges to devices
    for _, host in hosts.iterrows():
        host_id = host['id']
        for location in host['locations']:
            device_id = location['elementId']
            G.add_node(host_id, label=host_id, color='black')
            G.add_edge(host_id, device_id)
    
    # Add device-device edges
    for _, link in links.iterrows():
        src = link['src']['device']
        dst = link['dst']['device']
        G.add_edge(src, dst)
    
    # Get node colors
    node_colors = [G.nodes[node].get('color', 'skyblue') for node in G.nodes()]
    
    # Draw the network
    pos = nx.spring_layout(G)  # Layout for better visualization
    plt.figure(figsize=(15, 15))
    nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=200, font_size=10, font_weight='bold', edge_color='gray')
    plt.title("Network Topology")
    plt.show()

'''
        Capturing the traffic matrix based on link utilization and src-to-dest latency
        Case I: Merging Unit (MU) to virtual Intelligent Electronic Device (vIED) in the vPAC node
        Case II: WTG local data acquisition module to Edge Computing Platform Node 
        Case III: vIED to WTG actuator (bs)
        Case IV: ECP node to WTG actuator (qs)
'''

def network_traffic_state(port_stats_df, links_df):
    '''
        Computes network traffic state including link utilization, throughput, error rates,
        packet drops, and latency values for each link, and stores the results in a DataFrame.
        :param port_stats_df: DataFrame containing port statistics
        :param links_df: DataFrame containing network links
        :return: DataFrame containing computed network metrics for each link
    '''

    metrics_list = []

    for _, link in links_df.iterrows():
        src_device = link['src']['device']
        src_port = link['src']['port']
        dest_device = link['dst']['device']
        dest_port = link['dst']['port']
        link_label = f"{src_device}_{src_port}-{dest_device}_{dest_port}"

        # Get the corresponding port statistics for the source and destination ports
        src_port_stats = port_stats_df[
            (port_stats_df['device'] == src_device) & (port_stats_df['port'] == src_port)
        ]
        dest_port_stats = port_stats_df[
            (port_stats_df['device'] == dest_device) & (port_stats_df['port'] == dest_port)
        ]

        if not src_port_stats.empty and not dest_port_stats.empty:
            # Calculate metrics for the link
            src_rx_bytes = src_port_stats['bytesReceived'].values[0]
            src_tx_bytes = src_port_stats['bytesSent'].values[0]
            dest_rx_bytes = dest_port_stats['bytesReceived'].values[0]
            dest_tx_bytes = dest_port_stats['bytesSent'].values[0]

            # Assuming we have the time interval in seconds between measurements
            interval = 300  # For example, 5 minutes

            # Throughput (in bits per second)
            src_throughput = ((src_tx_bytes * 8) / interval)
            dest_throughput = ((dest_rx_bytes * 8) / interval)

            # Utilization (assuming a link capacity, for example, 1 Gbps)
            link_capacity = 1e9  # 1 Gbps in bits per second
            src_utilization = (src_throughput / link_capacity) * 100  # Percentage
            dest_utilization = (dest_throughput / link_capacity) * 100  # Percentage

            # Error rates (assuming we have error counts)
            src_error_rate = src_port_stats['errors'].values[0] / interval
            dest_error_rate = dest_port_stats['errors'].values[0] / interval

            # Packet drops (assuming we have drop counts)
            src_packet_drops = src_port_stats['packetsDropped'].values[0]
            dest_packet_drops = dest_port_stats['packetsDropped'].values[0]

            # Latency (assuming we have latency measurements in milliseconds)
            src_latency = src_port_stats['latency'].values[0]
            dest_latency = dest_port_stats['latency'].values[0]

            # Store the metrics in a dictionary
            metrics = {
                'link_label': link_label,
                'src_throughput': src_throughput,
                'dest_throughput': dest_throughput,
                'src_utilization': src_utilization,
                'dest_utilization': dest_utilization,
                'src_error_rate': src_error_rate,
                'dest_error_rate': dest_error_rate,
                'src_packet_drops': src_packet_drops,
                'dest_packet_drops': dest_packet_drops,
                'src_latency': src_latency,
                'dest_latency': dest_latency,
            }

            metrics_list.append(metrics)

    # Convert the list of metrics to a DataFrame
    metrics_df = pd.DataFrame(metrics_list)

    # Save the DataFrame to a CSV file
    metrics_df.to_csv('network_traffic_state.csv', index=False)

    return metrics_df


'''
    Network traffic monitoring against system intents 
    (captured as normalized thresholds)
'''

if __name__ == "__main__":
    # Get network state variables from file1.py
    devices, links, hosts, flows, port_stats, paths = current_network_state()
    
    # Visualize the network topology
    visualize_network(devices, links, hosts)
    
    # Example src and dest devices
    src_device = 'MU'
    dest_device = 'vIED'
    
    # Monitor traffic for specific cases
    network_traffic_state_df = network_traffic_state(port_stats,links)
    print(network_traffic_state_df)
