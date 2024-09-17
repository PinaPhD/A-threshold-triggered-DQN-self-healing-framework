# -*- coding: utf-8 -*-
"""
Created on Tue Sep 05 14:11:18 2024

@author: amwangi254 Based on LNAHI Script 
"""

import numpy as np
import matplotlib.pyplot as plt

# Define constants
NUM_SWITCHES = 40  # Based on the provided switches in your file
HEALTHY_TEMP_RANGE = (18, 27)  # Healthy temperature range in °C
TIME_STEPS = 100  # Number of simulation steps
COOLING_RATE = 0.5  # Rate at which the HVAC unit cools down a switch (°C per time step)
HEATING_RATE = 0.3  # Rate at which the HVAC unit heats up a switch (°C per time step)

# Create a list of switch identifiers from the provided file
switches = [
    'of:000000000000000c', 'of:000000000000000d', 'of:000000000000000a', 'of:000000000000000b',
    'of:000000000000000e', 'of:000000000000000f', 'of:0000000000000010', 'of:0000000000000011',
    'of:0000000000000014', 'of:0000000000000015', 'of:0000000000000012', 'of:0000000000000013',
    'of:0000000000000018', 'of:0000000000000019', 'of:0000000000000016', 'of:0000000000000017',
    'of:000000000000001a', 'of:000000000000001d', 'of:000000000000001e', 'of:000000000000001b',
    'of:000000000000001c', 'of:000000000000001f', 'of:0000000000000021', 'of:0000000000000022',
    'of:0000000000000020', 'of:0000000000000003', 'of:0000000000000025', 'of:0000000000000004',
    'of:0000000000000026', 'of:0000000000000023', 'of:0000000000000001', 'of:0000000000000024',
    'of:0000000000000002', 'of:0000000000000007', 'of:0000000000000008', 'of:0000000000000005',
    'of:0000000000000027', 'of:0000000000000028', 'of:0000000000000006', 'of:0000000000000009'
]

# Initialize temperatures for each switch (randomly between 10 and 35°C)
current_temperatures = np.random.uniform(10, 35, size=NUM_SWITCHES)
temperature_history = np.zeros((NUM_SWITCHES, TIME_STEPS))

# Initialize control signals (1 for cooling, -1 for heating, 0 for no action)
control_signals = np.zeros((NUM_SWITCHES, TIME_STEPS))

# Simulate temperature control over time
for t in range(TIME_STEPS):
    for i in range(NUM_SWITCHES):
        if current_temperatures[i] > HEALTHY_TEMP_RANGE[1]:
            # Switch is overheating, activate cooling
            current_temperatures[i] -= COOLING_RATE
            control_signals[i, t] = 1
        elif current_temperatures[i] < HEALTHY_TEMP_RANGE[0]:
            # Switch is too cold, activate heating
            current_temperatures[i] += HEATING_RATE
            control_signals[i, t] = -1
        # Record the temperature
        temperature_history[i, t] = current_temperatures[i]

# Plot temperature profiles for a few switches
plt.figure(figsize=(10, 6))
for i in range(min(NUM_SWITCHES, 5)):  # Plot 5 random switches
    plt.plot(temperature_history[i], label=f'Switch {switches[i]}')

plt.axhline(y=HEALTHY_TEMP_RANGE[0], color='g', linestyle='--', label='Lower Healthy Limit')
plt.axhline(y=HEALTHY_TEMP_RANGE[1], color='r', linestyle='--', label='Upper Healthy Limit')
plt.title('Temperature Profile of Switches')
plt.xlabel('Time (steps)')
plt.ylabel('Temperature (°C)')
plt.legend(loc='best')
plt.show()

# Plot control signals for the same switches
plt.figure(figsize=(10, 6))
for i in range(min(NUM_SWITCHES, 5)):
    plt.plot(control_signals[i], label=f'Switch {switches[i]}')

plt.title('Control Signals to HVAC (1: Cooling, -1: Heating, 0: No Action)')
plt.xlabel('Time (steps)')
plt.ylabel('Control Signal')
plt.legend(loc='best')
plt.show()
