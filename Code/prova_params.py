# This file contains a bunch of different varables for Prova 210
# Update these values to change the parameters on the prova

CHANNEL = 1 # For non-switching measurements, set the channel

CYCLE_AUTOSCAN_CHANNELS = [1, 2] # for switching measurements, set the channels to measure

time_delay =100; # "Max": 3000, "Min": 0
sampling_time = 20; #"Max": 99, "Min": 0
scan_current_begin = 0; #"Max": 120.00, "Min": 0
scan_current_end = 5; #"Max": 12.00, "Min": 0.0
cell_area = 1; #"Max": 9999.0, "Min": 0.001
irradiance = 50; # "Max": 1000, "Min": 10
single_test_point = 10; # "Max": 12.00, "Min": 0.0
low_power_alarm = 10; # "Max": 1000, "Min": 10.00

CYCLE_SCAN_PERIOD = 2; # Time, in minutes, between measurements
CYCLE_SCAN_NUM_SCAN = 3; # Number of measurements to be taken total

SESSION_NAME = "default_session_" # this variable can be changed to change the session folder the data goes into
# by default the session name will stay the same with only the session number increasing each time
SESSION_NUMBER = 1 # increases by 1 each time a measurment is taken, to reset it just set this back to 1

autorun = True; # This determines wheter the program will run automatically
                # (just cycle scan or other stuff too? HERE) in the background