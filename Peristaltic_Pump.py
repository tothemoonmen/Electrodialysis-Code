import serial
import time
import math


"""
# Open a connection to the serial device
port = 'COM6'  # Replace with the correct COM port for your device
baud_rate = 19200  # Replace with the correct baud rate for your device
ser = serial.Serial(port, baud_rate)

# Send the disconnect code (255 - FF hexadecimal)
disconnect_code = b'
ser.write(disconnect_code)

# Wait for 20 milliseconds
time.sleep(0.5)

# Send the pump unit ID with the addition of 128
unit_id = 30
unit_id_with_flag = unit_id + 128
ser.write(bytes([unit_id_with_flag]))
print("unit_id_with_flag" + str(unit_id_with_flag))
# Read the echo response from the serial device
response = ser.read(1)  # Read 1 byte from the serial device
echoed_unit_id = int.from_bytes(response, byteorder='big')
print("echoed_unit_id" + str(echoed_unit_id))
# Check if the echoed unit ID matches the sent unit ID
if echoed_unit_id == unit_id:
    print("Echo successful! Received echoed unit ID:", echoed_unit_id)
else:
    print("Echo unsuccessful!")

# Close the serial connection
ser.close()
"""""
"I got the equation by recording the voltage at what rpm i wanted. then just solved for the line of best fit with " \
"these points: (48,4.984), (47,4.9), (46.1,4.8), (45.1,4.7),(44,4.6), (43.1,4.474)(42.1,4.38),(41, 4.268),(40,4.168), " \
"(39.1,4.064), (38, 3.963),(37,3.863),(36.1,3.751),(35,3.651),(34,3.551),(33.1,3.455),(32,3.336),(31, 3.236), (30," \
"3.125),(29.1, 3.026), (28, 2.926), (27.1, 2.811),(26.1,2.711), (25, 2.611),(24, 2.511), (23.1,  2.411),(22, 2.298)," \
"(21, 2.198), (20.1,2.098),(19,1.98),(18,1.80), (17.1,1.78),(16,1.67),(15,1.57),(14,1.460),(13.1,1.360),(12,1.260)," \
"(11.1,1.146),(10.1, 1.05),(9.04,9.35),(8.09,.835),(.6.96,6.02),(6.02,.620),(5.08,.53) "

def set_rpm(rpm):

    return round((rpm - 0.0356106) / 9.5912, 3)

#print(set_rpm(22.5))