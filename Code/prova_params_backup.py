# This file contains the user-adjustable settings for the Prova 210 system.

# For non-switching measurements, set the channel here.
CHANNEL = 1

# For switching measurements, channels are scanned in this order.
# [1, 2] means PV1 is measured first, followed by PV2.
CYCLE_AUTOSCAN_CHANNELS = [1, 2]

# Prova 210 scan parameters
time_delay = 100             # Max: 3000, Min: 0
sampling_time = 20           # Max: 99, Min: 0
scan_current_begin = 0       # Max: 120.00, Min: 0
scan_current_end = 5         # Max: 12.00, Min: 0.0
cell_area = 1                # Max: 9999.0, Min: 0.001
irradiance = 50              # Max: 1000, Min: 10
single_test_point = 10       # Max: 12.00, Min: 0.0
low_power_alarm = 10         # Max: 1000, Min: 10.00

# Automatic PV1 -> PV2 cycling settings
CYCLE_SCAN_PERIOD = 5        # Minutes between the START of each PV1 -> PV2 cycle
CYCLE_START_HOUR = 7         # Begin measuring each day at 07:00
CYCLE_END_HOUR = 20          # Stop measuring each day at 20:00

# Legacy settings retained for compatibility with other project scripts.
SESSION_NAME = "default_session_"
SESSION_NUMBER = 1

# Automatically run cycle_autoscan when Prova_210_serial_comm.py is executed.
autorun = True
