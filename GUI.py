import sys
from pathlib import Path
from tkinter import messagebox

import pyvisa
import xlsxwriter
from pyvisa import VisaIOError
from pyvisa.constants import VI_ERROR_RSRC_NFOUND

import Siglent
import BKPrescion
import PH
import threading
import time
import tkinter as tk
import threading
from openpyxl import Workbook
from openpyxl import Workbook, load_workbook
import os
import pandas as pd
import Peristaltic_Pump


class GUI:

    def __init__(self):
        self.rpm_voltage = 0  # The voltage that will be sent to the peristaltic pump
        self.rpm = 0  # User inputs wanted RPM for peristaltic pump
        self.minutes = 0  # The amount of minutes user will choose
        self.ph_threshold = 0  # The user inputs what ph they want electrolysis to start
        self.instrument_input = ""  # User chooses which power supply they are using
        self.channel_input = ""  # User enters which channel they will be using on the power supply
        self.voltage_input = 0  # User enters the voltage they will send to the power supply
        self.current_input = 0  # User enters the current they will send to the power supply
        self.monitor_variables_input = 0  # User chooses if they want to monitor the variables
        self.stop_ph = 0  # User chooses what ph they want the ph to stop
        self.total_volume = 0  # User enters the amount of volume in the system
        self.duration = 0  # User enters the amount of time they will wait to collect data
        self.instrument = None  # self.instrument is set to the power supply the user chose
        self.channel = 0  # self.channel is set to the channel the user chose
        self.current = 0  # self.current is set to the current the user chose
        self.is_running = True  # Shared flag to control the thread execution

    def create_window(self):
        self.window = tk.Tk()  # Set the Initial window

        self.label = tk.Label(  # creates Label
            self.window,
            text="Communicate with devices"
        )
        self.label.pack()

        self.instrument_label = tk.Label(  # creates Label
            self.window,
            text="Select an instrument:"
        )
        self.instrument_label.pack()  # .pack() makes the windows, buttons, user entry appear on screen

        self.bk_button = tk.Button(  # Creates the "BK Precision" button on screen
            self.window,
            text="BK Precision",
            command=lambda: self.handle_instrument_selection("1")
            # When user chooses BK Precision the handle_instrument_selection method  runs with 1 as its argument
        )
        self.bk_button.pack()  # .pack() makes the windows, buttons, user entry appear on screen

        self.siglent_button = tk.Button(  # Creates the "Siglent" button on screen
            self.window,
            text="Siglent",
            command=lambda: self.handle_instrument_selection("2")
            # When user chooses Siglent the handle_instrument_selection method runs with 2 as its argument

        )
        self.siglent_button.pack()  # .pack() makes the windows, buttons, user entry appear on screen

        self.channel_label = tk.Label(  # Creates channel  label
            self.window,
            text="Select a channel:"
        )

        self.channel1_button = tk.Button(  # Creates channel 1 button
            self.window,
            text="Channel 1",
            command=lambda: self.handle_channel_selection("1")
            # When user chooses channel 1 the handle_channel_selection method runs with 1 as its argument
        )

        self.channel2_button = tk.Button(  # Creates channel 2 button
            self.window,
            text="Channel 2",
            command=lambda: self.handle_channel_selection("2")
            # When user chooses channel 2 the handle_channel_selection method runs with 2 as its argument

        )

        self.channel3_button = tk.Button(  # Creates channel 3 button
            self.window,
            text="Channel 3",
            command=lambda: self.handle_channel_selection("3")
            # When user chooses channel 3 the handle_channel_selection method runs with 3 as its argument

        )

        self.voltage_label = tk.Label(  # Creates voltage label
            self.window,
            text="Enter voltage:"
        )

        self.voltage_entry = tk.Entry(self.window)  # Creates user input box
        self.submit_voltage_button = tk.Button(  # Creates Submit button
            self.window,
            text="Submit",
            command=self.handle_voltage_submission
            # When user enters voltage the handle_voltage_submission method runs
        )

        self.total_volume_label = tk.Label(  # creates volume label
            self.window,
            text="How much volume total volume do you have? :"

        )
        self.total_volume_entry = tk.Entry(self.window)  # Creates user input box
        self.submit_total_volume_button = tk.Button(  # Creates Submit button
            self.window,
            text="Submit",
            command=lambda: self.handle_total_volume_selection()
            # When user enters volume the handle_total_volume_selection method runs
        )

        self.current_label = tk.Label(  # Creates current label
            self.window,
            text="Enter Current:"
        )

        self.current_entry = tk.Entry(self.window)  # Creates user input box
        self.submit_current_button = tk.Button(  # Creates Submit button
            self.window,
            text="Submit",
            command=self.handle_current_submission
            # When user enters current the handle_current_submission method runs

        )
        self.rpm_label = tk.Label(  # Creates RPM Label
            self.window,
            text="Enter the RPM for the Peristaltic Pump: "
        )

        self.rpm_entry = tk.Entry(self.window)  # Creates user input box
        self.submit_rpm_button = tk.Button(  # Creates  submit button
            self.window,
            text="Submit",
            command=self.handle_rpm_submission
            # When user enters rpm the handle_rpm_submission method runs
        )

        self.monitor_variables_label = tk.Label(  # Creates monitor variables label
            self.window,
            text="Do you want to monitor variables?:"
        )

        self.monitor_variables_yes_button = tk.Button(  # Creates yes button
            self.window,
            text="YES",
            command=lambda: self.handle_monitor_variables_selection(True)
            # When user chooses to monitor variables handle_monitor_variables_selection method with True
        )

        self.monitor_variables_no_button = tk.Button(  # Creates no button
            self.window,
            text="NO",
            command=lambda: self.handle_monitor_variables_selection(False)
            # When user chooses to monitor variables handle_monitor_variables_selection method with False

        )

        self.duration_minutes_label = tk.Label(  # Creates minutes label
            self.window,
            text="How often do you want to collect data in minutes? :"

        )
        self.duration_minute_entry = tk.Entry(self.window)  # Creates minute entry box
        self.submit_duration_minute_button = tk.Button(  # Creates  Submit Minutes button
            self.window,
            text="Submit Minutes",
            command=lambda: self.handle_duration_minute_selection()
            # When user enters minutes the handle_duration_minute_selection method runs

        )
        self.duration_second_label = tk.Label(  # Creates seconds label
            self.window,
            text="How often do you want to collect data in seconds? :"

        )
        self.duration_second_entry = tk.Entry(self.window)  # Creates seconds entry box
        self.submit_duration_second_button = tk.Button(  # Creates seconds  submit button
            self.window,
            text="Submit Seconds",
            command=lambda: self.handle_duration_seconds_selection()
            # When user enters seconds the handle_duration_seconds_selection method runs

        )

        self.ph_label = tk.Label(  # Creates ph label
            self.window,
            text="At what PH do you want to start electrodialysis? :"

        )
        self.ph_entry = tk.Entry(self.window)  # Creates ph entry box
        self.submit_ph_button = tk.Button(  # Creates ph submit button
            self.window,
            text="Submit",
            command=lambda: self.handle_ph_selection()
            # When user enters ph the handle_ph_selection method runs

        )

        self.stop_ph_label = tk.Label(  # Creates stop ph label
            self.window,
            text="At what PH do you want the electrodialysis to stop? :"

        )
        self.stop_ph_entry = tk.Entry(self.window)  # Creates stop ph entry box
        self.submit_stop_ph_button = tk.Button(  # Creates ph submit button
            self.window,
            text="Submit",
            command=lambda: self.handle_stop_ph_selection()
            # When user enters stop ph the handle_stop_ph_selection  method runs

        )
        self.excel_label = tk.Label(  # Creates excel label
            self.window,
            text="Do you have an execl file already?:"
        )

        self.excel_yes_button = tk.Button(  # Creates yes excel label
            self.window,
            text="YES",
            command=lambda: self.handle_excel_selection(True)
            # When user chooses yes the handle excel selection method runs with True

        )

        self.excel_no_button = tk.Button(  # Creates excel no button
            self.window,
            text="NO",
            command=lambda: self.handle_excel_selection(False)
            # When user chooses no the handle excel selection method runs with False

        )

        self.do_more_label = tk.Label(  # Creates do more label
            self.window,
            text="Do you want to do anything else ?"
        )

        self.do_more_yes_button = tk.Button(  # Creates do more yes button
            self.window,
            text="YES",
            command=lambda: self.handle_do_more_selection(True)
            # When user chooses no the handle do more method runs with True

        )

        self.do_more_no_button = tk.Button(  # Creates do more no button
            self.window,
            text="NO",
            command=lambda: self.handle_do_more_selection(False)
            # When user chooses no the handle do more method runs with False

        )

        self.home_label = tk.Label(  # Creates home label
            self.window,
            text=" Running commands! "
        )

        self.home_stop = tk.Button(  # Creates home stop button
            self.window,
            text="Stop commands",
            command=lambda: self.handle_home_selection(1)
            # When user chooses stop commands the handle home selection runs with False

        )

        self.home_commands = tk.Button(  # Creates home commands button
            self.window,
            text="Enter in new commands",
            command=lambda: self.handle_home_selection(2)
            # When user chooses Enter in new commands the handle home selection runs with True

        )

        self.home_sample = tk.Button(  # Creates home sample button
            self.window,
            text="Take sample",
            command=lambda: self.handle_home_selection(3)
            # When user chooses Take sample the handle home selection runs with 1

        )

        self.sample_label = tk.Label(  # Creates sample label
            self.window,
            text="How much are you sampling ? :"

        )
        self.sample_entry = tk.Entry(self.window)  # Creates sample entry box
        self.sample_button = tk.Button(  # Creates sample submit button
            self.window,
            text="Submit",
            command=lambda: self.handle_sample_selection()
            # When user enters sample amount  handle sample selection method runs

        )

        self.window.mainloop()  # Starts the window to start up

    def handle_stop_ph_selection(self):
        self.stop_ph = self.stop_ph_entry.get()  # gets user entry for stop ph
        if self.stop_ph:
            try:
                ph_float = float(self.stop_ph)  # converts stop_ph from string to float
                if ph_float <= -1.6 or ph_float >= 15.6:
                    # Show an error message if the pH value is outside the valid range
                    messagebox.showerror("Invalid pH Value", "Please enter a pH value between -1.6 and 15.6.")
                elif ph_float < self.ph_threshold:
                    # Show an error message if the pH value is less than the threshold
                    messagebox.showerror("Invalid Input", "Please enter a pH value greater than when you start "
                                                          "electrodialysis.")
                else:
                    # Set the stop_ph value and update the GUI elements
                    self.stop_ph = ph_float
                    self.stop_ph_entry.pack_forget()
                    self.stop_ph_label.pack_forget()
                    self.submit_stop_ph_button.pack_forget()
                    self.excel_label.pack()
                    self.excel_yes_button.pack()
                    self.excel_no_button.pack()
            except ValueError:
                # Show an error message if the input is not a valid numeric value
                messagebox.showerror("Invalid Input", "Please enter a valid numeric value for the pH.")

    def handle_ph_selection(self):
        # Get the pH value from the entry widget
        ph_value = self.ph_entry.get()
        if ph_value:
            try:
                # Convert the pH value to a float
                ph_float = float(ph_value)
                if -1.6 <= ph_float <= 15.6:
                    # Set the ph_threshold and update the GUI elements
                    self.ph_threshold = ph_float
                    self.ph_entry.pack_forget()
                    self.ph_label.pack_forget()
                    self.submit_ph_button.pack_forget()
                    self.stop_ph_label.pack()
                    self.stop_ph_entry.pack()
                    self.submit_stop_ph_button.pack()
                else:
                    # Show an error message if the pH value is outside the valid range
                    messagebox.showerror("Invalid pH Value", "Please enter a pH value between -1.6 and 15.6.")
            except ValueError:
                # Show an error message if the input is not a valid numeric value
                messagebox.showerror("Invalid Input", "Please enter a valid numeric value for the pH.")

    def handle_duration_minute_selection(self):
        # Get the input minutes from the entry widget
        minutes = self.duration_minute_entry.get()
        if minutes:
            try:
                # Convert the input minutes to an integer
                minutes = int(minutes)

                if minutes < 0 or minutes > 60:
                    # Show an error message if the input minutes are outside the valid range
                    messagebox.showerror("Invalid Value", "Please enter a number between 0 and 60 Minutes")
                else:
                    # Convert minutes to seconds and set the 'minutes' attribute
                    minutes = 60 * minutes
                    self.minutes = minutes

                    # Hide the current GUI elements and show the next set of elements
                    self.duration_minutes_label.pack_forget()
                    self.duration_minute_entry.pack_forget()
                    self.submit_duration_minute_button.pack_forget()
                    self.duration_second_label.pack()
                    self.duration_second_entry.pack()
                    self.submit_duration_second_button.pack()

            except ValueError:
                # Show an error message if the input is not a valid integer
                messagebox.showerror("Invalid Input", "Please enter a valid numeric value for the Duration.")

    def handle_home_selection(self, selection):
        # If selection is 1, show the instrument options (bk_button and siglent_button)
        if selection == 1:
            self.home_label.pack_forget()
            self.home_commands.pack_forget()
            self.home_stop.pack_forget()
            self.home_sample.pack_forget()
            self.instrument_label.pack()
            self.bk_button.pack()
            self.siglent_button.pack()

        # If selection is 2, stop the running code and show the instrument options
        elif selection == 2:
            self.instrument.is_running = False
            self.home_label.pack_forget()
            self.home_commands.pack_forget()
            self.home_stop.pack_forget()
            self.home_sample.pack_forget()
            self.instrument_label.pack()
            self.bk_button.pack()
            self.siglent_button.pack()
            print("Stopping code")

        # If selection is 3, show the sample entry options
        elif selection == 3:
            self.home_label.pack_forget()
            self.home_commands.pack_forget()
            self.home_stop.pack_forget()
            self.home_sample.pack_forget()
            self.sample_label.pack()
            self.sample_entry.pack()
            self.sample_button.pack()

    def open_excel_file(self):
        # Get the current working directory
        directory = os.getcwd()

        # Create a file name based on the instrument and channel
        file_name = f"{self.instrument}_CH{self.channel}"

        # Remove any characters from the file name that are not alphanumeric or spaces
        file_name = "".join([c for c in file_name if c.isalpha() or c.isdigit() or c == ' ']).rstrip()

        # Add the file format if missing
        if not file_name.endswith(".xlsx"):
            file_name += ".xlsx"

        # Get the full file path
        file_path = os.path.join(directory, file_name)

        # Start threads to monitor variables and active devices
        threading.Thread(target=self.instrument.monitor_variables,
                         args=(str(file_path), self.duration, self.channel,)).start()

        threading.Thread(target=self.instrument.active_devices,
                         args=(self.ph_threshold, self.stop_ph, self.channel, self.rpm_voltage,)).start()

        print("Opening " + file_path)

    def create_excel_file(self):
        # Get the current working directory
        directory = os.getcwd()

        # Create a file name based on the instrument and channel
        file_name = f"{self.instrument}_CH{self.channel}"

        # Remove any characters from the file name that are not alphanumeric or spaces
        file_name = "".join([c for c in file_name if c.isalpha() or c.isdigit() or c == ' ']).rstrip()

        # Add the file format if missing
        if not file_name.endswith(".xlsx"):
            file_name += ".xlsx"

        # Get the full file path
        file_path = os.path.join(directory, file_name)

        print("Saving to " + file_path)

        try:
            # Create an Excel workbook and sheet
            wb = Workbook()
            sheet = wb.active

            # Add column headers
            sheet['A1'] = 'Time Stamp'
            sheet['B1'] = 'Voltage'
            sheet['C1'] = 'Current'
            sheet['D1'] = 'Power'

            # Save the workbook to the file
            wb.save(file_path)
        except Exception as e:
            print(f"Error creating Excel file: {e}")

        # Start threads to monitor variables and active devices
        threading.Thread(target=self.instrument.monitor_variables,
                         args=(str(file_path), self.duration, self.channel,)).start()

        threading.Thread(target=self.instrument.active_devices,
                         args=(self.ph_threshold, self.stop_ph, self.channel, self.rpm_voltage,)).start()

    def handle_do_more_selection(self, selection):
        # If the user selects "True," go back to the home screen
        if selection is True:
            print("returning home")
            self.do_more_label.pack_forget()
            self.do_more_yes_button.pack_forget()
            self.do_more_no_button.pack_forget()
            self.instrument_label.pack()
            self.bk_button.pack()
            self.siglent_button.pack()

        # If the user selects "False," execute the request
        elif selection is False:
            print("Executing request")
            self.do_more_label.pack_forget()
            self.do_more_yes_button.pack_forget()
            self.do_more_no_button.pack_forget()
            self.home_label.pack()
            self.home_commands.pack()
            self.home_stop.pack()
            self.home_sample.pack()

    def handle_excel_selection(self, selection):
        # If the user selects "True," find the file and go back to the home screen
        if selection is True:
            print("finding file")
            self.open_excel_file()
            self.excel_label.pack_forget()
            self.excel_yes_button.pack_forget()
            self.excel_no_button.pack_forget()
            self.home_label.pack()
            self.home_commands.pack()
            self.home_stop.pack()
            self.home_sample.pack()

        # If the user selects "False," create the file and go back to the home screen
        elif selection is False:
            print("Creating file")
            self.excel_label.pack_forget()
            self.excel_yes_button.pack_forget()
            self.excel_no_button.pack_forget()
            self.home_label.pack()
            self.home_commands.pack()
            self.home_stop.pack()
            self.home_sample.pack()
            self.create_excel_file()

    def handle_monitor_variables_selection(self, selection):
        self.monitor_variables_input = selection
        # If the user selects "True," show the duration entry options
        if selection is True:
            print("User wants to save data")
            self.monitor_variables_label.pack_forget()
            self.monitor_variables_yes_button.pack_forget()
            self.monitor_variables_no_button.pack_forget()
            self.duration_minutes_label.pack()
            self.duration_minute_entry.pack()
            self.submit_duration_minute_button.pack()

        # If the user selects "False," go back to the do_more options
        elif selection is False:
            print("User is not saving data")
            self.monitor_variables_label.pack_forget()
            self.monitor_variables_yes_button.pack_forget()
            self.monitor_variables_no_button.pack_forget()
            self.do_more_label.pack()
            self.do_more_yes_button.pack()
            self.do_more_no_button.pack()

    def handle_instrument_selection(self, instrument):
        self.instrument_input = instrument
        # Start a new thread to handle the instrument selection
        threading.Thread(target=self.chose_instrument).start()

    def handle_channel_selection(self, channel):
        self.channel_input = channel
        # Start a new thread to handle the channel selection
        threading.Thread(target=self.chose_channel).start()

        # Hide the current channel options
        self.channel_label.pack_forget()
        self.channel1_button.pack_forget()
        self.channel2_button.pack_forget()
        self.channel3_button.pack_forget()

        # Show the voltage entry options
        self.show_voltage_entry()

    def chose_instrument(self):
        print("Entering chose_instrument()")

        # Check if the user selected BK Precision instrument
        if self.instrument_input == "1":
            self.instrument = BKPrescion

            try:
                print("Initializing BK Precision connection...")
                connection = self.instrument.initialize_connection()
                print("Starting BK Precision...")
                self.instrument.startup(connection)
                print("BK Precision started successfully.")

                # Hide the current instrument options
                self.instrument_label.pack_forget()
                self.bk_button.pack_forget()
                self.siglent_button.pack_forget()

                # Show the channel options
                self.channel_label.pack()
                self.channel1_button.pack()
                self.channel2_button.pack()
                self.channel3_button.pack()

            except pyvisa.errors.VisaIOError:
                # Show an error message if the device is not found or not properly connected
                messagebox.showerror("Can not find device",
                                     "Make sure the device is turned on and the USB is properly connected.")

        # Check if the user selected Siglent instrument
        if self.instrument_input == "2":
            self.instrument = Siglent
            try:
                print("Initializing Siglent connection...")
                connection = self.instrument.initialize_connection()
                print("Communicating with Siglent...")
                self.instrument.communicate_with_instrument(connection)
                print("Siglent communication successful.")

                # Hide the current instrument options
                self.instrument_label.pack_forget()
                self.bk_button.pack_forget()
                self.siglent_button.pack_forget()

                # Show the channel options
                self.channel_label.pack()
                self.channel1_button.pack()
                self.channel2_button.pack()
                self.channel3_button.pack()

            except pyvisa.errors.VisaIOError:
                # Show an error message if the device is not found or not properly connected
                messagebox.showerror("Can not find device",
                                     "Make sure the device is turned on and the USB is properly connected.")

    def chose_channel(self):
        # Set the channel based on the user's input
        if self.channel_input == "1":
            self.channel = 1
        elif self.channel_input == "2":
            self.channel = 2
        elif self.channel_input == "3":
            self.channel = 3
        print("Channel input:", self.channel_input)

    def show_voltage_entry(self):
        # Show the voltage entry options
        self.voltage_label.pack()
        self.voltage_entry.pack()
        self.submit_voltage_button.pack()

    def handle_voltage_submission(self):
        # Get the voltage value from the entry widget
        voltage = self.voltage_entry.get()
        if voltage:
            try:
                # Convert the voltage value to a float
                voltage_value = float(voltage)
                if voltage_value <= 0:
                    # Show an error message for negative or zero voltage value
                    messagebox.showerror("Invalid Input", "Please enter a positive or zero value for the voltage.")

                # Check voltage limits based on the instrument and channel
                elif voltage_value > 32 and self.instrument == Siglent and self.channel != 3:
                    messagebox.showerror("Invalid Input", "Please enter a value less than 32 for the voltage.")
                elif voltage_value > 5 and self.instrument == Siglent and self.channel == 3:
                    messagebox.showerror("Invalid Input", "Please enter a value less than 5 for the voltage.")
                elif voltage_value > 30 and self.instrument == BKPrescion and self.channel != 3:
                    messagebox.showerror("Invalid Input", "Please enter a value less than 32 for the voltage.")
                elif voltage_value > 5 and self.instrument == BKPrescion and self.channel == 3:
                    messagebox.showerror("Invalid Input", "Please enter a value less than 5 for the voltage.")

                else:
                    # Store the voltage input and start a thread to set the voltage
                    self.voltage_input = voltage_value
                    threading.Thread(target=self.set_voltage).start()

                    # Hide the current voltage entry options and show the current entry options
                    self.voltage_label.pack_forget()
                    self.voltage_entry.pack_forget()
                    self.submit_voltage_button.pack_forget()
                    self.show_current_entry()

            except ValueError:
                # Show an error message for invalid numeric value for voltage
                messagebox.showerror("Invalid Input", "Please enter a valid numeric value for the voltage.")

    def set_voltage(self):
        # Convert the voltage input to float
        voltage = float(self.voltage_input)

        # Set the voltage using the instrument and channel
        self.instrument.set_voltage(self.instrument.initialize_connection(), voltage, self.channel)
        print("Running set_voltage...")

        # Add your code logic for command 1 here

    def show_current_entry(self):
        # Show the current entry options
        self.current_label.pack()
        self.current_entry.pack()
        self.submit_current_button.pack()

    def handle_current_submission(self):
        # Get the current value from the entry widget
        current = self.current_entry.get()
        if current:
            try:
                # Convert the current value to float
                self.current_input = float(current)
                if self.current_input <= 0:
                    # Show an error message for non-positive current value
                    messagebox.showerror("Invalid Input", "Please enter a positive numeric value for the current.")
                elif self.current_input > 3.2 and self.instrument == Siglent:
                    # Show an error message for current value exceeding the limit for Siglent
                    messagebox.showerror("Invalid Input", "Please enter a value less than 3.2 for the current.")
                elif self.current_input > 6 and self.instrument == BKPrescion and self.channel != 3:
                    # Show an error message for current value exceeding the limit for BK Precision on non-channel 3
                    messagebox.showerror("Invalid Input", "Please enter a value less than 6 for the current.")
                elif self.current_input > 3 and self.instrument == BKPrescion and self.channel == 3:
                    # Show an error message for current value exceeding the limit for BK Precision on channel 3
                    messagebox.showerror("Invalid Input", "Please enter a value less than 3 for the current.")
                else:
                    # Start a thread to set the current
                    threading.Thread(target=self.set_current).start()

                    # Hide the current entry options and show the total volume entry options
                    self.current_label.pack_forget()
                    self.current_entry.pack_forget()
                    self.submit_current_button.pack_forget()
                    self.total_volume_label.pack()
                    self.total_volume_entry.pack()
                    self.submit_total_volume_button.pack()

            except ValueError:
                # Show an error message for invalid numeric value for current
                messagebox.showerror("Invalid Input", "Please enter a valid numeric value for the current.")

    def set_current(self):
        # Convert the current input to float
        current = float(self.current_input)

        # Set the current using the instrument and channel
        self.instrument.set_current(self.instrument.initialize_connection(), current, self.channel)
        print("Running set_current...")

    def handle_sample_selection(self):
        self.sample_size = self.sample_entry.get()
        if self.sample_size:
            try:
                self.sample_size = float(self.sample_size)
                if self.sample_size > 0:
                    self.total_volume -= self.sample_size
                    self.sample_label.pack_forget()
                    self.sample_entry.pack_forget()
                    self.sample_button.pack_forget()
                    self.home_label.pack()
                    self.home_commands.pack()
                    self.home_stop.pack()
                    self.home_sample.pack()

                else:
                    messagebox.showerror("Invalid Input", "Please enter a positive numeric value for the sample size.")
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter a valid numeric value for the sample size")

    def handle_total_volume_selection(self):
        self.total_volume = self.total_volume_entry.get()

        if self.total_volume:
            try:
                self.total_volume = float(self.total_volume)
                if self.total_volume > 0:
                    self.total_volume_entry.pack_forget()
                    self.total_volume_label.pack_forget()
                    self.submit_total_volume_button.pack_forget()
                    self.rpm_label.pack()
                    self.rpm_entry.pack()
                    self.submit_rpm_button.pack()



                else:
                    messagebox.showerror("Invalid Input", "Please enter a positive numeric value for the sample size.")
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter a valid numeric value for the sample size")

    def handle_duration_seconds_selection(self):
        seconds = self.duration_second_entry.get()
        if seconds:
            try:
                seconds = int(seconds)
                if seconds < 0 or seconds > 60:
                    messagebox.showerror("Invalid Input", "Please enter a value between 0 and 60 seconds")

                else:
                    self.duration = self.minutes + seconds
                    self.duration_second_entry.pack_forget()
                    self.duration_second_label.pack_forget()
                    self.submit_duration_second_button.pack_forget()
                    self.ph_label.pack()
                    self.ph_entry.pack()
                    self.submit_ph_button.pack()
                    print('Taking data every ' + str(self.minutes) + ' minutes and ' + str(seconds) + " seconds. ")
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter a valid numeric value for the seconds")

    def handle_rpm_submission(self):
        rpm = self.rpm_entry.get()
        if rpm:
            try:
                rpm = float(rpm)
                if rpm < 5 or rpm > 48:
                    messagebox.showerror("Invalid Input", "Please enter a value between 5 and 48 RPM")

                else:
                    self.rpm_voltage = Peristaltic_Pump.set_rpm(rpm)
                    self.rpm_label.pack_forget()
                    self.rpm_entry.pack_forget()
                    self.submit_rpm_button.pack_forget()
                    self.monitor_variables_label.pack()
                    self.monitor_variables_yes_button.pack()
                    self.monitor_variables_no_button.pack()
                    print("The rpm is set to " + str(rpm))
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter a valid numeric value for the RPM")


# Create an instance of the GUI class
gui = GUI()
gui.create_window()
