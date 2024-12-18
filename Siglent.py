import pyvisa
import pandas as pd
import openpyxl
from datetime import datetime
import xlrd
import time
from openpyxl import load_workbook
from openpyxl import Workbook, load_workbook

import Conductivity
import Graph
import PH
import Machine_learning
import Temperature
from Graph import LivePlotter

ph = 0  # Global PH variable so that it can be used in multiple methods simultaneously
voltage = 0  # Global voltage variable so that it can be used in multiple methods simultaneously
current = 0  # Global current variable so that it can be used in multiple methods simultaneously
power = 0  # Global power variable so that it can be used in multiple methods simultaneously
temperature = 0  # Global temperature variable so that it can be used in multiple methods simultaneously
conductivity = 0  # Global conductivity variable so that it can be used in multiple methods simultaneously

is_running = True  # Shared flag variable that tell when to start and stop code


# initialize_connection is how the computer connects to the power supply. The power supply is returned
def initialize_connection():
    # Define the individual components of the resource address
    vendor_id = '0xf4ec'
    product_id = '0x1430'
    serial_number = 'SPD3XIDX5R2849'

    # Create the resource address using the components
    resource_address = f'USB0::{vendor_id}::{product_id}::{serial_number}::0::INSTR'

    # Create a PyVISA resource manager
    rm = pyvisa.ResourceManager()

    # Open the connection to the device
    power_supply = rm.open_resource(resource_address, timeout=10000)  # Set timeout to 10000 milliseconds (10 seconds)

    return power_supply


# Gets power supply identification
def communicate_with_instrument(power_supply):
    # Send the '*IDN?' command
    power_supply.write('*IDN?')

    # Read the response from the instrument
    print('Reading the response')
    response = power_supply.read()

    # Print the response
    print(f"Instrument identification: {response}")


# Get power supply current reading and returns current, param are the power supply and channel
def get_current_reading(power_supply, channel: int):
    power_supply.write('INST CH' + str(channel))
    current = power_supply.query(":MEAS:CURR?")
    power_supply.close()
    # print('The current is: ' + str(current))
    return current


# sets the voltage,param are power supply, voltage, and channel
def set_voltage(power_supply, voltage: float, channel: int):
    #print("Sending " + str(voltage) + " Volts to channel " + str(channel))
    voltage += .002  # .002 is needed because the power supply will be off by .002

    power_supply.write('INST CH' + str(channel))
    time.sleep(3)
    power_supply.write('VOLT ' + str(voltage))
    power_supply.close()


# sets the current,param are power supply, voltage, and channel
def set_current(power_supply, current: float, channel: int):
    print("Sending " + str(current) + " Amps to channel " + str(channel))
    current += .001  # .001 is needed because the power supply will be off by .001

    power_supply.write('INST CH' + str(channel))
    time.sleep(3)
    power_supply.write('CURRent ' + str(current))
    power_supply.close()


# gets power reading. param are the powersupply and channel
def get_power_reading(power_supply, channel):
    # Send the command to retrieve the power reading
    power_supply.write('INST CH' + str(channel))
    power_reading = power_supply.query('MEAS:POWE?')

    # Return the power reading as a float value
    return float(power_reading)


# Turns the channel on the power supply on. param are the power supply and channel
def turn_on(power_supply, channel):
    power_supply.write('OUTP CH' + str(channel) + ',ON')


# Turns the channel on the power supply off. param are the power supply and channel
def turn_off(power_supply, channel):
    power_supply.write('OUTP CH' + str(channel) + ',OFF')


# Sets timer on power supply. param is the power supply
def timer(power_supply):
    power_supply.write('TIMEr CH1,ON')


# Gets voltage reading and returns voltage. Param are power supply and channel
def get_voltage_reading(power_supply, channel: int):
    time.sleep(2)
    power_supply.write('INST CH' + str(channel))
    voltage = power_supply.query("MEAS:VOLT?")
    power_supply.close()
    print('The Voltage is: ' + str(voltage))
    return voltage



# closes connection on power supply, param is power supply
def close_connection(power_supply):
    # Close the connection
    power_supply.close()
