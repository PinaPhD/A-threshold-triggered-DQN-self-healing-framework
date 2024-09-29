# -*- coding: utf-8 -*-
"""
    Created on Tue Sep 05 14:11:18 2024
    @Main Contributor: León Navarro-Hilfiker
    @Contributor: Agrippina Mwangi
"""
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import time
import numpy as np

# Set the threshold for bytes received and temperature limits
THRESHOLD = 190000000
alpha = 0.001                       # Heat coefficient
temp_init = np.full(40, 18)         # Initial temperature value for each switch
tau_thr_max = 27                    # Maximum temperature threshold
tau_thr_min = 18                    # Minimum temperature threshold

switch_temp = {}                    # Store device temperature values at different timesteps

# Function to fetch the latest values from the view
def fetch_latest_device_statistics():
    # Connect to the database
    conn = mysql.connector.connect(
        host="localhost",               # e.g. "localhost" or IP address
        user="root",                    # e.g. "root"
        password="50acresIsinya",       # e.g. "password"
        database="Orsted"               # Name of the database containing the view
    )
    
    # Create a cursor to execute queries
    cursor = conn.cursor(dictionary=True)

    # SQL query to fetch the latest values (most recent timestamp)
    query = """
    SELECT *
    FROM port_statistics_device_agg
    WHERE timestamp = (SELECT MAX(timestamp) FROM port_statistics_device_agg)
    """
    
    cursor.execute(query)
    
    # Fetch all rows and load them into a Pandas DataFrame
    rows = cursor.fetchall()
    switch_util = pd.DataFrame(rows)

    # Close the connection
    cursor.close()
    conn.close()

    return switch_util

# Function to check switch utilization against the threshold
def check_switch_utilization(switch_util):
    # Check which devices have exceeded the threshold
    switch_util['exceeds_threshold'] = switch_util['total_bytesReceived'] > THRESHOLD

    # Calculate the percentage of utilization against the threshold
    switch_util['utilization_percentage'] = (switch_util['total_bytesReceived'] / THRESHOLD) * 100

    # Filter the devices that exceeded the threshold
    exceeded_devices = switch_util[switch_util['exceeds_threshold']]

    return exceeded_devices[['timestamp', 'device', 'total_bytesReceived', 'utilization_percentage']]

# Function to check switch temperature and manage cooling/heating systems
def manage_temperature_and_traffic(switch_util, temp_init, switch_temp):
    temperature = np.array(temp_init)

    for i, row in switch_util.iterrows():
        device = row['device']
        timestamp = row['timestamp']
        utilization = float(row['utilization_percentage'])
        
        # Compute the temperature based on utilization
        temperature[i] += temp_init[i] + alpha * (utilization - 100) / 100

        # Store the timestamp, device, and temperature in the switch_temp dictionary
        if device not in switch_temp:
            switch_temp[device] = []
        switch_temp[device].append({'timestamp': timestamp, 'temperature': temperature[i]})

        # Check if temperature exceeds thresholds
        if temperature[i] > tau_thr_max:
            print(f"Device {device} exceeds max temp: {temperature[i]}C.\nTriggering cooling system.")
            # Insert logic for cooling system here, e.g., HVAC system adjustments

        elif temperature[i] < tau_thr_min:
            print(f"Device {device} below min temp: {temperature[i]}C.\nTriggering heating system.")
            # Insert logic for heating system here, e.g., turning on heaters

        else:
            print(f"Device {device} is operating within nominal temperature: {temperature[i]}C. No action needed.")

        # Trigger DQN actions for traffic engineering if temperature is unstable
        if temperature[i] > tau_thr_max or temperature[i] < tau_thr_min:
            print(f"Triggering DQN to choose optimal paths away from paths with device {device} due to temperature instability.")

    return temperature

# Function to plot the temperature data from switch_temp
def plot_temperature_data(switch_temp):
    plt.figure(figsize=(10, 6))

    for device, temp_data in switch_temp.items():
        timestamps = [entry['timestamp'] for entry in temp_data]
        temperatures = [entry['temperature'] for entry in temp_data]
        plt.plot(timestamps, temperatures, label=device)

    plt.xlabel('Timestamp')
    plt.ylabel('Temperature (°C)')
    plt.title('Switch Temperature Over Time')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def temperature_module():    
    # List to store data for plotting
    historical_data = pd.DataFrame()
        
    # Fetch the latest statistics from the view
    latest_device_statistics = fetch_latest_device_statistics()

    # Check for devices that exceed the threshold and calculate utilization
    exceeded_device_stats = check_switch_utilization(latest_device_statistics)
    
    # Manage temperature and traffic engineering actions based on switch utilization
    temp_values = manage_temperature_and_traffic(latest_device_statistics, temp_init, switch_temp)

    # Append the exceeded stats to the historical data DataFrame
    historical_data = pd.concat([historical_data, exceeded_device_stats])
    
    return latest_device_statistics, exceeded_device_stats, temp_values, historical_data

# Main execution
if __name__ == "__main__":
    

    # Set the number of iterations (e.g., how many times to fetch data, 1 fetch per minute)
    num_iterations = 10
    interval = 10  # Interval between checks in seconds
    
    #Calling the temperature module function
    latest_device_statistics, exceeded_device_stats, temp_values, historical_data = temperature_module()
    
    # Plot the temperature data from the switch_temp dictionary
    if switch_temp:
        plot_temperature_data(switch_temp)
    else:
        print("No temperature data recorded during the monitored period.")
