# This file contains a bunch of different varables for Prova 210
# Update these values to change the parameters on the prova

CHANNEL = 2 # For non-switching measurements, set the channel

time_delay =100; # "Max": 3000, "Min": 0
sampling_time = 20; #"Max": 99, "Min": 0
scan_current_begin = 0; #"Max": 120.00, "Min": 0
scan_current_end = 5; #"Max": 12.00, "Min": 0.0
cell_area = 1; #"Max": 9999.0, "Min": 0.001
irradiance = 50; # "Max": 1000, "Min": 10
single_test_point = 10; # "Max": 12.00, "Min": 0.0
low_power_alarm = 10; # "Max": 1000, "Min": 10.00

autorun = True; # This determines wheter the program will run automatically
                # (just cycle scan or other stuff too? HERE) in the background