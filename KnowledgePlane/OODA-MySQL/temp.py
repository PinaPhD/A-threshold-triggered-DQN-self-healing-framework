# -*- coding: utf-8 -*-
"""
    Created on Tue Sep 05 14:11:18 2024
    @Main Contributors: León Navarro-Hilfiker and Agrippina Mwangi
"""
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import time
import numpy as np
import csv

# Set the threshold for bytes received and temperature limits
THRESHOLD = 190000000
alpha = 0.001  # Heat coefficient
cf = 0.002     # Cooling coefficient
tau_thr_max = 27  # Maximum temperature threshold
tau_thr_min = 18  # Minimum temperature threshold

switch_temp = {}  # Store device temperature values at different timesteps
temp_init = {}    # Store initial temperature for each device
exceeded_devices_set = set()  # Track devices that exceeded the threshold
exceeded_devices_timestamps = []  # Track exceeded device timestamps and temperatures

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

# Function to compute temperature based on utilization
def manage_temperature_and_traffic(switch_util, switch_temp, temp_init):
    for i, row in switch_util.iterrows():
        device = row['device']
        timestamp = row['timestamp']
        utilization = float(row['utilization_percentage'])

        # Initialize the temperature for the device if not done already
        if device not in temp_init:
            temp_init[device] = 18  # Set the initial temperature for each device
        
        
        # Store the timestamp, device, and updated temperature
        if device not in switch_temp:
            switch_temp[device] = []
        switch_temp[device].append({'timestamp': timestamp, 'temperature': temp_init[device]})
        
        
        # Compute the new temperature based on utilization and sensor weights
        w_asic = 0.02
        temp_init[device] += (w_asic * (utilization * 100)) - 0.7   #0.2 - to stabilize temperature
            

        
        
        #Check for violations
        # Cooling mechanism
        if temp_init[device] > tau_thr_max:
            print(f"Device {device} exceeds max temp: {temp_init[device]}C. Cooling system activated.")
            # Apply cooling effect
            temp_init[device] -= 2

        elif temp_init[device] < tau_thr_min:
            print(f"Device {device} below min temp: {temp_init[device]}C. Heating system activated.")
            temp_init[device] = tau_thr_min  # Restore to the minimum nominal range

        else:
            print(f"Device {device} is operating within nominal temperature: {temp_init[device]}C.")

    return temp_init

# Function to plot overall temperature data and overlay scatter points for exceeded devices
def plot_temperature_with_exceeding_devices(switch_temp, exceeded_devices_timestamps):
    plt.figure(figsize=(12, 8))

    # Plot the time series for all devices
    for device, temp_data in switch_temp.items():
        timestamps = [entry['timestamp'] for entry in temp_data]
        temperatures = [entry['temperature'] for entry in temp_data]
        plt.plot(timestamps, temperatures, label=f'{device} (Time Series)')

    # Overlay the scatter plot for exceeded devices
    exceeded_timestamps = [entry['timestamp'] for entry in exceeded_devices_timestamps]
    exceeded_temperatures = [entry['temperature'] for entry in exceeded_devices_timestamps]
    plt.scatter(exceeded_timestamps, exceeded_temperatures, color='red', label='Threshold Exceeded', zorder=5)

    # Adding labels and title
    plt.xlabel('Timestamp')
    plt.ylabel('Temperature (°C)')
    plt.title('Switch Temperature Over Time with Exceeded Threshold Points')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def temperature_module():
    historical_data = pd.DataFrame()
    latest_device_statistics = fetch_latest_device_statistics()
    exceeded_device_stats = check_switch_utilization(latest_device_statistics)
    #sensor_readings = simulate_temperature_readings()  # Get fresh sensor readings
    temp_values = manage_temperature_and_traffic(latest_device_statistics, switch_temp, temp_init)
    historical_data = pd.concat([historical_data, exceeded_device_stats])

    # Add devices that exceeded thresholds to the set and collect the relevant timestamps
    for i, row in exceeded_device_stats.iterrows():
        device = row['device']
        timestamp = row['timestamp']
        temp = temp_init[device]
        exceeded_devices_set.add(device)
        exceeded_devices_timestamps.append({'device': device, 'timestamp': timestamp, 'temperature': temp})

    return latest_device_statistics, exceeded_device_stats, temp_values, historical_data

# Main execution loop
if __name__ == "__main__":
    interval = 2  # Update interval set to 2 seconds

    # Open the CSV file and write headers at the start
    with open('switch_temp_Wednesday.csv', mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['device', 'timestamp', 'temperature'])
        writer.writeheader()

        try:
            while True:
                latest_device_statistics, exceeded_device_stats, temp_values, historical_data = temperature_module()

                # Now apply the cooling/heating logic based on the current temperature
                #Here --- read the device and its associated temperature value, check for violations and trigger cooling or heating
                for device, temp_data in switch_temp.items():
                    latest_temp_data = temp_data[-1]  # Get the latest temperature entry for the device
                    current_temp = latest_temp_data['temperature']
                    timestamp = latest_temp_data['timestamp']

                   
                    # DQN traffic actions if temperature is unstable
                    if current_temp > tau_thr_max or current_temp < tau_thr_min:
                        print(f"Triggering DQN for traffic rerouting due to temperature instability in device {device}.")

                    # Write the latest data to CSV
                    writer.writerow({
                        'device': device,
                        'timestamp': timestamp,
                        'temperature': current_temp
                    })

                time.sleep(interval)  # Wait for 2 seconds before the next iteration

        except KeyboardInterrupt:
            # When interrupted, plot the overall time series and overlay exceeding points
            print("KeyboardInterrupt received. Plotting temperature data with exceeded thresholds...")
