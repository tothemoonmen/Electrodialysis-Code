import time
import serial
import pyftdi

"USB needs to be in UART mode for code to work. If the led is bilking green it is in the correct mode. "


# formats so that the code will send to the ph reader, returns response from the reader, param are the command and port
def send_command(command, port):
    COM_PORT = 'COM' + port  # Replace 'COMX' with the actual COM port on your system
    BAUD_RATE = 9600
    COM = serial.Serial(COM_PORT, BAUD_RATE)
    time.sleep(2)  # Wait for the connection to stabilize
    COM.write(command.encode() + b'\r')
    time.sleep(0.5)  # Wait for the probe to respond
    response = COM.read(COM.inWaiting()).decode().strip()
    return response


# Get ph and returns it as a string. Param is port
def get_ph(port):
    ph = send_command("R", "5")  # Take a reading
    if ph == "OK":
        print('PH said OK')
    else:
        ph_float = float(ph.split()[0])
        # print(ph)
        return ph_float

