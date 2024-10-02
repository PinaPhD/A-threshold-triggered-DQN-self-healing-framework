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
alpha = 0.001  # Heat coefficient
temp_init = np.full(40, 18)  # Initial temperature value for each switch
tau_thr_max = 27  # Maximum temperature threshold
tau_thr_min = 18  # Minimum temperature threshold

switch_temp = {}  # Store device temperature values at different timesteps


# Function to fetch the latest values from the view
def fetch_latest_device_statistics():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="50acresIsinya",
        database="Orsted"
    )
    cursor = conn.cursor(dictionary=True)
    query = """
    SELECT *
    FROM port_statistics_device_agg
    WHERE timestamp = (SELECT MAX(timestamp) FROM port_statistics_device_agg)
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    switch_util = pd.DataFrame(rows)
    cursor.close()
    conn.close()
    return switch_util


# Function to check switch utilization against the threshold
def check_switch_utilization(switch_util):
    switch_util['exceeds_threshold'] = switch_util['total_bytesReceived'] > THRESHOLD
    switch_util['utilization_percentage'] = (switch_util['total_bytesReceived'] / THRESHOLD) * 100
    exceeded_devices = switch_util[switch_util['exceeds_threshold']]
    return exceeded_devices[['timestamp', 'device', 'total_bytesReceived', 'utilization_percentage']]


# Function to manage cooling/heating systems
def manage_temperature_and_traffic(switch_util, temp_init, switch_temp):
    temperature = np.array(temp_init)  # Initializes the switch temperature

    for i, row in switch_util.iterrows():
        device = row['device']
        timestamp = row['timestamp']
        utilization = float(row['utilization_percentage'])

        # Compute temperature based on utilization
        temperature[i] += alpha * (utilization) / 100

        # Store the timestamp, device, and temperature
        if device not in switch_temp:
            switch_temp[device] = []
        switch_temp[device].append({'timestamp': timestamp, 'temperature': temperature[i]})

        # Cooling system logic
        if temperature[i] > tau_thr_max:
            print(f"Device {device} exceeds max temp: {temperature[i]}C. Cooling system activated.")
            # Example: cooling effect applied, decrease temperature by 5 degrees
            temperature[i] -= 5
        elif temperature[i] < tau_thr_min:
            print(f"Device {device} below min temp: {temperature[i]}C. Heating system activated.")
            temperature[i] = tau_thr_min  # Restore to the minimum nominal range
        else:
            print(f"Device {device} is operating within nominal temperature: {temperature[i]}C.")

        # DQN traffic actions if temperature is unstable
        if temperature[i] > tau_thr_max or temperature[i] < tau_thr_min:
            print(f"Triggering DQN for traffic rerouting due to temperature instability in device {device}.")

    return temperature


# Function to plot temperature data
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
    historical_data = pd.DataFrame()
    latest_device_statistics = fetch_latest_device_statistics()
    exceeded_device_stats = check_switch_utilization(latest_device_statistics)
    temp_values = manage_temperature_and_traffic(latest_device_statistics, temp_init, switch_temp)
    historical_data = pd.concat([historical_data, exceeded_device_stats])
    return latest_device_statistics, exceeded_device_stats, temp_values, historical_data


# Main execution loop
if __name__ == "__main__":
    num_iterations = 10  # Number of iterations
    interval = 5  # Interval between checks in seconds

    for _ in range(num_iterations):
        latest_device_statistics, exceeded_device_stats, temp_values, historical_data = temperature_module()

        # Uncomment below if you want to plot the temperature data after each iteration
        # if switch_temp:
        #     plot_temperature_data(switch_temp)
        # else:
        #     print("No temperature data recorded during the monitored period.")

        time.sleep(interval)  # Wait for the specified interval (5 seconds)
