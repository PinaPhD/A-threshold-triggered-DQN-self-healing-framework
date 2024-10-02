# -*- coding: utf-8 -*-
"""
    Created on Tue Sep 05 14:11:18 2024
    @Main Contributor: León Navarro-Hilfiker and Agrippina Mwangi
"""
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import time
import numpy as np

# Set the threshold for bytes received and temperature limits
THRESHOLD = 190000000
alpha = 0.001  # Heat coefficient
cf = 0.005     # Cooling coefficient
tau_thr_max = 27  # Maximum temperature threshold
tau_thr_min = 18  # Minimum temperature threshold

switch_temp = {}  # Store device temperature values at different timesteps
temp_init = {}    # Store initial temperature for each device
exceeded_devices_set = set()  # Track devices that exceeded the threshold
exceeded_devices_timestamps = []  # Track exceeded device timestamps and temperatures

#Switch sensor readings -- Industrial-grade equipment temperature ranges between (-40 deg.c to 85 deg.c)
inlet_temp_sensor = float(np.random.uniform(-10,35,1))   
outlet_temp_sensor =  float(np.random.uniform(-10,35,1))  
cpu_temp_sensor =  float(np.random.uniform(-10,35,1))  
psu_temp_sensor =  float(np.random.uniform(-10,35,1)) 
ambient_temp_sensor = float(np.random.uniform(15,32,1))

#Assigning weights to these sensors so as to determine their importance in the aggregate temperature value 
w_inlet = 0.10
w_outlet = 0.10
w_cpu = 0.30
w_psu = 0.20
w_asic = 0.30
w_amb = 0.10


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

        # Compute the new temperature based on utilization
        temp_init[device] = (
        (w_inlet * inlet_temp_sensor) +
        (w_outlet * outlet_temp_sensor) +
        (w_cpu * cpu_temp_sensor) +
        (w_psu * psu_temp_sensor) + (w_asic * (utilization * 100)) + (w_amb * ambient_temp_sensor)
    ) / (w_inlet + w_outlet + w_cpu + w_psu + w_asic + w_amb)
         

        # Store the timestamp, device, and updated temperature
        if device not in switch_temp:
            switch_temp[device] = []
        switch_temp[device].append({'timestamp': timestamp, 'temperature': temp_init[device]})

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
    exceeded_devices = [entry['device'] for entry in exceeded_devices_timestamps]

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
    interval = 5  # Interval between checks in seconds

    try:
        while True:
            latest_device_statistics, exceeded_device_stats, temp_values, historical_data = temperature_module()

            # Now apply the cooling/heating logic based on the current temperature
            for device, temp_data in switch_temp.items():
                latest_temp_data = temp_data[-1]  # Get the latest temperature entry for the device
                current_temp = latest_temp_data['temperature']
                timestamp = latest_temp_data['timestamp']

                '''
                    Cooling mechanism
                    Source: https://www.amcoenclosures.com/the-importance-of-cooling-network-switches/
                '''
                if current_temp > tau_thr_max:
                    print(f"Device {device} exceeds max temp: {current_temp}C. Cooling system activated.")
                    # Apply cooling effect
                    latest_temp_data['temperature'] -= cf

                elif current_temp < tau_thr_min:
                    print(f"Device {device} below min temp: {current_temp}C. Heating system activated.")
                    latest_temp_data['temperature'] = tau_thr_min  # Restore to the minimum nominal range

                else:
                    print(f"Device {device} is operating within nominal temperature: {current_temp}C.")

                # DQN traffic actions if temperature is unstable
                if current_temp > tau_thr_max or current_temp < tau_thr_min:
                    print(f"Triggering DQN for traffic rerouting due to temperature instability in device {device}.")

            time.sleep(interval)  # Wait for the specified interval (5 seconds)

    except KeyboardInterrupt:
        # When interrupted, plot the overall time series and overlay exceeding points
        print("KeyboardInterrupt received. Plotting temperature data with exceeded thresholds...")
        
        # Flatten the dictionary into a list of rows
        data = []
        for device, records in switch_temp.items():
            for record in records:
                data.append({
                    'device': device,
                    'timestamp': record['timestamp'],
                    'temperature': record['temperature']
                })

        # Convert the list of rows into a pandas DataFrame
        df = pd.DataFrame(data)
        
        # Write the DataFrame to a CSV file
        df.to_csv('switch_temp.csv', index=False)
        
        print("Data has been written to switch_temp.csv")

        if exceeded_devices_timestamps:
            plot_temperature_with_exceeding_devices(switch_temp, exceeded_devices_timestamps)
        else:
            print("No devices exceeded the threshold during the monitoring period.")
