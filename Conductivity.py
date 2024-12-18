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


def get_conductivity(port):
    port = str(port)
    con = send_command("R", port)  # Take a reading
    return con


#print(get_conductivity(7))

def set_probe(port):
    port = str(port)
    type = send_command("*OK,0", port)  # Take a reading
    return type

def get_status(port):
    port = str(port)
    status = send_command("Status",port)
    return status
def sleep_mode(port):
    port = str(port)
    sleep = send_command("Sleep", port)
    return sleep

#print(set_probe(7))
#print(get_status(7))