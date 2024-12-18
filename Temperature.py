import time
import serial


def send_command(command, port):
    COM_PORT = 'COM' + port  # Replace 'COMX' with the actual COM port on your system
    BAUD_RATE = 9600
    COM = serial.Serial(COM_PORT, BAUD_RATE)
    time.sleep(2)  # Wait for the connection to stabilize
    COM.write(command.encode() + b'\r')
    time.sleep(0.5)  # Wait for the probe to respond
    response = COM.read(COM.inWaiting()).decode().strip()
    return response


def get_temperature(port):
    port = str(port)
    temperature = send_command("R", port)  # Take a reading
    return temperature

def get_status(port):
    port = str(port)
    status = send_command("Status",port)
    return status
def sleep_mode(port):
    port = str(port)
    sleep = send_command("Sleep", port)
    return sleep


#print(get_temperature(8))
