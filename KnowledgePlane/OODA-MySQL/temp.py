# -*- coding: utf-8 -*-
"""
    Created on Tue Sep 05 14:11:18 2024
    @Main Contributor:  León Navarro-Hilfiker
    @Contributor: Agrippina Mwangi
"""
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import time

# Set the threshold for bytes received
THRESHOLD = 190000000
alpha =0.001   #Heat coefficient

# Function to fetch the latest values from the view
def fetch_latest_device_statistics():
    # Connect to the database
    conn = mysql.connector.connect(
        host="localhost",        # e.g. "localhost" or IP address
        user="root",    # e.g. "root"
        password="50acresIsinya",# e.g. "password"
        database="Orsted" # Name of the database containing the view
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
    data = pd.DataFrame(rows)

    # Close the connection
    cursor.close()
    conn.close()

    return data

# Function to check switch utilization against the threshold
def check_switch_utilization(data):
    # Check which devices have exceeded the threshold
    data['exceeds_threshold'] = data['total_bytesReceived'] > THRESHOLD

    # Calculate the percentage of utilization against the threshold
    data['utilization_percentage'] = (data['total_bytesReceived'] / THRESHOLD) * 100

    # Filter the devices that exceeded the threshold
    exceeded_devices = data[data['exceeds_threshold']]

    return exceeded_devices[['timestamp', 'device', 'total_bytesReceived', 'utilization_percentage']]

# Function to plot the time series
def plot_exceeded_threshold(df):
    plt.figure(figsize=(10, 6))

    for device in df['device'].unique():
        device_data = df[df['device'] == device]
        plt.plot(device_data['timestamp'], device_data['utilization_percentage'], label=device)

    plt.xlabel('Timestamp')
    plt.ylabel('Utilization Percentage (%)')
    plt.title('Switch Utilization Exceeding Threshold Over Time')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Main execution
if __name__ == "__main__":
    # List to store data for plotting
    historical_data = pd.DataFrame()

    # Set the number of iterations (e.g., how many times to fetch data, 1 fetch per minute)
    num_iterations = 10
    interval = 10  # Interval between checks in seconds

    for i in range(num_iterations):
        # Fetch the latest statistics from the view
        latest_device_statistics = fetch_latest_device_statistics()

        # Check for devices that exceed the threshold and calculate utilization
        exceeded_device_stats = check_switch_utilization(latest_device_statistics)

        # Append the exceeded stats to the historical data DataFrame
        historical_data = pd.concat([historical_data, exceeded_device_stats])

        # Wait for the specified interval before fetching again
        time.sleep(interval)

    # Plot the time series of devices that exceeded the threshold
    if not historical_data.empty:
        plot_exceeded_threshold(historical_data)
    else:
        print("No devices exceeded the threshold during the monitored period.")
