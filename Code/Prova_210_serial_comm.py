import serial
import struct
import time
import sh, os
import subprocess
import csv
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from relay_code import *
from prova_params import *

BAUD = 19200
PORT = '/dev/ttyUSB0'
PARAM_CODES = {"time delay": {"Codes": [b'W00136', b'W00137', b'W00138', b'W00139'], "Max": 3000, "Min": 0 }, # id codes for changing sampling parameters, DO NOT CHANGE
               "sampling time": {"Codes": [b'W00368', b'W00369', b'W00370', b'W00371'], "Max": 99, "Min": 0},
               "scan current begin": {"Codes": [b'W00128', b'W00129', b'W00130', b'W00131'], "Max": 120.00, "Min": 0.0},
               "scan current end": {"Codes": [b'W00132', b'W000133', b'W00134', b'W00135'], "Max": 12.00*10, "Min": 0.0},
               "cell area": {"Codes": [b'W00304', b'W00305', b'W00306', b'W00307'], "Max": 9999.0*1000, "Min": 0.001*1000},
               "irradiance": {"Codes": [b'W00308', b'W00309', b'W00310', b'W00311'], "Max": 1000, "Min": 10},
               "single test point": {"Codes": [b'W00316', b'W00317', b'W00318', b'W00319'], "Max": 12.00*10, "Min": 0.0},
               "low power alarm": {"Codes": [b'W00140', b'W00141', b'W00142', b'W00143'], "Max": 1000*10, "Min": 10.00*10}
    } # HERE -- could potenitally add error checking to check for floats/ints to enforce same things software does but do not have to

SER = serial.Serial(
    PORT,
    baudrate=BAUD,
    bytesize=8,
    parity='N',
    stopbits=1,
    timeout=1
)

# navigating to the repository directory -- ensures that the files are pushed to the correct place
REPO_DIR = r"/home/seris/Documents/SERIS-Prova_210_GitHome"

TODAY= str(datetime.now().year) + "-" + str(datetime.now().month) + "-" + str(datetime.now().day)

# This function takes in a serial object as an argument and attempts to connect through this serial object
# to a Prova 210. HERE also takes in the parameters it supplies and uses the to update vars
def establish_comms(ser = SER):         
    ser.reset_input_buffer()

    ser.dtr = False
    ser.rts = False
    time.sleep(0.5)

    ser.dtr = True
    ser.rts = True
    time.sleep(0.5)
    
    data = b''
    
    while (data != b'\x00\x00\x00'):
        print("Requesting connection...")
        ser.write(b'%')

        time.sleep(0.5)

        data = ser.read(100)
    
    while(len(data) < 10):
        print("Sending setup command...")
        ser.write(b'S0000000400\r')

        time.sleep(1)
        data = ser.read(5000)
        print("Setup successful") # need to actually check for this

def apply_param(param_name, param_value, ser = SER):
    print("Changing", param_name, "to", str(
    
    
    param_value), "...")
    if (param_value < PARAM_CODES[param_name]["Max"] and param_value > PARAM_CODES[param_name]["Min"]):
        val = [(int(param_value) >> 24) &0xff,
            (int(param_value) >> 16) &0xff,
            (int(param_value) >> 8) &0xff,
            int(param_value) &0xff]
        
        for i in range(4):
            ser.write(PARAM_CODES[param_name]["Codes"][i] + bytes([val[i]]) + b'\r')
            time.sleep(0.5)
        ser.write(b'R')
        time.sleep(1)
        data = ser.read(10000)
    else:
        print("ERROR:", param_name, "outside of allowed range. Allowed values are between", PARAM_CODES[param_name]["Min"], "and", PARAM_CODES[param_name]["Max"])
    print(param_name, "changed")

def change_parameters(ser = SER, time_delay=None, sampling_time=None, scan_current_begin=None, scan_current_end=None, cell_area=None, irradiance=None, single_test_point=None, low_power_alarm=None):
    print("Changing parameters...")
    if time_delay is not None:
        apply_param("time delay", time_delay)
    if sampling_time is not None:
        apply_param("sampling time", sampling_time)
    if scan_current_begin is not None:
        scan_current_begin *= 10
        apply_param("scan current begin", scan_current_begin)
    if scan_current_end is not None:
        apply_param("scan current end", scan_current_end*10)
    if cell_area is not None:
        apply_param("cell area", cell_area*1000)
    if irradiance is not None:
        apply_param("irradiance", irradiance)
    if single_test_point is not None:
        apply_param("single test point", single_test_point*10)
    if low_power_alarm is not None:
        apply_param("low power alarm", low_power_alarm*10)
    print("Parameters changed")

# Loads stored PV data from PROVA 210 solar module
def rec_load(ser = SER):
    print("Attempting to load recorded logs...")
    ser.write(b'S0000000001\r')
    time.sleep(0.5)
    ser.write(b'S0040001029\r')
    time.sleep(0.5)
    ser.write(b'S0103001659\r')
    time.sleep(0.5)
    ser.write(b'S0166002289\r')
    time.sleep(0.5)
    data = ser.read(10000)
    print("Loaded recorded logs:", data)
    return data

# This function clears the memory of the connected Prova 210, deleting the sample files stored on the PROVA
def clear_mem(ser = SER):
    print("Clearing memory...")
    ser.write(b'W00000\0\r')
    time.sleep(0.5)
    ser.write(b'W00007\0\r')
    time.sleep(0.5)    
    ser.write(b'W00008\0\r')
    time.sleep(0.5)
    ser.write(b'W00001\0\r')
    time.sleep(0.5)
    ser.write(b'R')
    print("Memory cleared")
    
# This function takes in a serial object, assumed to be connected to a Prova 210, and attempts to perform an 
# returning the raw binary data recieved in the event of a sucessful scan
# HERE -- maybe add something so that repeated failures or other error messages raise errors and/or get commmunicated
def autoscan(ser = SER):
    errcount = 0
    data = ""
    print("Beginning autoscan...")
    
    while (data != b'\x05\x00' and errcount < 10):
        print("Attempting autoscan command...")
        ser.write(b'A')

        time.sleep(1)
        data = ser.read(10000)
        
        if data == b'\x01': # Error code returned when test leads are not connected properly
            print("Error: Please connect test leads to module")
            time.sleep(10)
            errcount += 1

    time.sleep(10)
    packet = bytearray()
    
    while packet == bytearray(b''):
        while True:
            chunk = ser.read(4096)

            if not chunk:
                break

            packet.extend(chunk)

    print(packet)
    print("Autoscan complete")
    return packet

def scan(ser = SER):
    errcount = 0
    data = ""
    print("Beginning scan...")

    while (data != b'\x05\x00' and errcount < 10):
        print("Attempting scan")
        ser.write(b's')

        time.sleep(1)
        data = ser.read(10000)
        
        if data == b'\x01': # Error code returned when test leads are not connected properly
            print("Error: Please connect test leads to module")
            time.sleep(10)
            errcount += 1

    time.sleep(10)
    packet = bytearray()

    while True:
        chunk = ser.read(4096)

        if not chunk:
            break

        packet.extend(chunk)

    print(packet)
    print("Scan complete")
    return packet
    
# This function takes in binary PV curve data and returns the same data structured as a list of lists,
# with each inner list being one row of a PV table
def decode_curve(dat, channel=None, packet_size=8, sample_num=1, date_time=None):
    if channel is None:
        channel = CHANNEL
    print("Processsing PV curve data...")
    data = dat.hex()
    num_points = len(data)
    if date_time is None:
        date_time = datetime.now()
    
    data_header = [int(data[i:i+packet_size], 16) for i in range(0, packet_size*3, packet_size)]
    measurements = [data[i:i + packet_size] for i in range(packet_size*3, num_points, packet_size)]
        
    V_open = data_header[0]/1000.0
    I_short = data_header[1]/10.0
    P_max_ind = data_header[2]

    V_max_P = float(int(measurements[P_max_ind*2], 16))/1000.0
    I_max_P = float(int(measurements[P_max_ind*2+1], 16))/10.0
    P_max = V_max_P * I_max_P
    
    result = [
        ["Sample Number", sample_num, "Collected with Prova 210"],
        ["Channel Number", channel],
        ["Date & Time", date_time],
        ["Vopen (V)", V_open],
        ["Ishort (mA)", I_short],
        ["Vmaxp (V)", V_max_P],
        ["Imaxp (mA)", I_max_P],
        ["Pmax (mW)", P_max],
        ["V (V)", "I (mA)", "P (mW)"]# header row for the rest of the measurments
    ]
    for i in range(0, len(measurements), 2):
        result.append([float(int(measurements[i], 16))/1000.0, float(int(measurements[i+1], 16))/10.0, float(int(measurements[i], 16)*int(measurements[i+1], 16))/10000])
    result.append(["END OF SAMPLE"])
    result.append([])
    print("Processsing complete")
    return result

def decode_log_curve(dat, channel=None, packet_size = 4, header_length = 4, footer_length = 12):
    if channel is None:
        channel = CHANNEL
    data = dat.hex()
    num_points = len(data)
    print("Processsing logged curve...") # need to test with multiple curves
    
    measurements = [data[i:i + packet_size] for i in range(packet_size*header_length, num_points, packet_size)]
    data_footer = measurements[(len(measurements)-footer_length):len(measurements)]
    sample_num = int(data[0:4], 16)
    year = int(data[4:6], 16)
    month = int(data[6:8], 16)
    day = int(data[8:10], 16)
    hour = int(data[10:12], 16)
    minute = int(data[12:14], 16)
    second = int(data[14:16], 16)
    
    date_time = str(year) + "-" + str(month) + "-" + str(day) + " " + str(hour) + ":" + str(minute) + ":" + str(second)
    V_open = int(data_footer[1], 16)/1000.0 # figure out where this stuff is stored
    I_short = int(data_footer[0], 16)/5.0
    
    V_max_P = 0
    I_max_P = 0
    P_max = V_max_P * I_max_P
    
    result = [
        ["Sample Number (Logged Sample)", sample_num],
        ["Channel Number", channel],
        ["Date & Time", date_time],
        ["Vopen (V)", V_open],
        ["Ishort (mA)", I_short],
        ["Vmaxp (V)", V_max_P],
        ["Imaxp (mA)", I_max_P],
        ["Pmax (mW)", P_max],
        ["V (V)", "I (mA)", "P (mW)"] # header row for the rest of the measurments
    ]
    for i in range(0, len(measurements)-footer_length, 2):
        result.append([float(int(measurements[i], 16))/1000.0, float(int(measurements[i+1], 16))/5.0, float(int(measurements[i], 16)*int(measurements[i+1], 16))/10000])
        if result[i+9][2] > P_max:
            P_max = result[i+9][2]
            V_max_P = result[i+9][0]
            I_max_P = result[i+9][1]
    result[5][1] = V_max_P
    result[6][1] = I_max_P
    result[7][1] = P_max
    result.append(["END OF LOGGED SAMPLE"])
    result.append([])
    print("Processsing complete")
    return result
    
# This function adds a file to the next git commit
def add_file(filename):
    os.chdir(REPO_DIR)
    print(filename)
    subprocess.run(["git", "add", filename])


# Creates the automatic folder structure:
# Data / YEAR / MONTH / YYYY-MM-DD / Channel_X / Data
# Data / YEAR / MONTH / YYYY-MM-DD / Channel_X / Graphs
def get_output_folders(channel, date_time=None):
    if date_time is None:
        date_time = datetime.now()

    year = date_time.strftime("%Y")
    month = date_time.strftime("%m")
    day = date_time.strftime("%Y-%m-%d")

    channel_folder = os.path.join(
        REPO_DIR,
        "Data",
        year,
        month,
        day,
        f"Channel_{channel}"
    )

    data_folder = os.path.join(channel_folder, "Data")
    graph_folder = os.path.join(channel_folder, "Graphs")

    # os.makedirs creates every missing folder level automatically.
    os.makedirs(data_folder, exist_ok=True)
    os.makedirs(graph_folder, exist_ok=True)

    return data_folder, graph_folder


# Writes one Prova scan to a CSV file in the correct year/month/day/channel folder.
def write_PV_data(data=None, channel=None, filename=None, date_time=None):
    if data is None:
        data = []

    if channel is None:
        channel = CHANNEL

    if date_time is None:
        date_time = datetime.now()

    print("Writing PV data...")

    data_folder, _ = get_output_folders(channel, date_time)
    timestamp = date_time.strftime("%H-%M-%S")

    if filename is None:
        filepath = os.path.join(data_folder, f"{timestamp}.csv")
    else:
        filepath = os.path.join(data_folder, f"{timestamp}_{filename}.csv")

    with open(filepath, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(data)

    add_file(filepath)
    print(f"Data saved to: {filepath}")


# Saves the I-V / power graph for one Prova scan in the matching Graphs folder.
def graph_PV_data(sample_num, data=None, channel=None, filename=None, date_time=None):
    if data is None:
        data = []

    if channel is None:
        channel = CHANNEL

    if date_time is None:
        date_time = datetime.now()

    print("Graphing PV data...")

    _, graph_folder = get_output_folders(channel, date_time)
    timestamp = date_time.strftime("%H-%M-%S")

    if filename is None:
        filepath = os.path.join(graph_folder, f"{timestamp}.png")
    else:
        filepath = os.path.join(graph_folder, f"{timestamp}_{filename}.png")

    voltage = []
    current = []
    power = []

    for i in range(9, len(data) - 2):
        voltage.append(data[i][0])
        current.append(data[i][1])
        power.append(data[i][2])

    current_col = 'tab:red'
    pwr_col = 'tab:blue'

    fig, ax1 = plt.subplots()
    ax1.set_ylabel('Current (mA)')
    ax1.set_xlabel('Voltage (V)')
    ax1.plot(voltage, current, color=current_col, linewidth=2, label='Current (mA)')
    ax1.tick_params(axis='y', labelcolor=current_col)

    ax2 = ax1.twinx()
    ax2.set_ylabel('Power (mW)', color=pwr_col)
    ax2.plot(voltage, power, color=pwr_col, linewidth=2, label='Power (mW)')
    ax2.tick_params(axis='y', labelcolor=pwr_col)

    fig.tight_layout()
    plt.savefig(filepath)
    plt.close(fig)

    add_file(filepath)
    print(f"Graph saved to: {filepath}")


# Uploads files already staged with git add.
def upload_data(today=None, files_to_add=None):
    if today is None:
        today = datetime.now().strftime("%Y-%m-%d")

    print("Uploading data...")

    if files_to_add is not None:
        for filename in files_to_add:
            add_file(filename)

    os.chdir(f"{REPO_DIR}/Data")
    sh.git("pull")
    sh.git("commit", "-m", f"Add data from {today}")
    sh.git("push")
    print("Upload complete")


# Returns the start and end times for the calendar day containing 'now'.
def get_daily_window(now, start_hour, end_hour):
    start_time = now.replace(
        hour=start_hour,
        minute=0,
        second=0,
        microsecond=0
    )

    end_time = now.replace(
        hour=end_hour,
        minute=0,
        second=0,
        microsecond=0
    )

    return start_time, end_time


# Continuously runs the PV measurement system every day.
# During each day it scans PV1 -> PV2 every <period> minutes from 07:00 to 20:00.
# After 20:00 it turns all relays off, waits overnight, and automatically resumes at 07:00.
def cycle_autoscan(ser=SER, period=CYCLE_SCAN_PERIOD, channels=None,
                   start_hour=CYCLE_START_HOUR, end_hour=CYCLE_END_HOUR):

    if channels is None:
        channels = CYCLE_AUTOSCAN_CHANNELS

    # Existing estimate: one Prova scan takes about 30 seconds.
    # For two channels this gives a theoretical minimum cycle period of 1 minute.
    minimum_period = len(channels) / 2

    if period < minimum_period:
        print(
            f"ERROR: Period too short. "
            f"Setting period to {minimum_period} min"
        )
        period = minimum_period

    print("Beginning continuous daily cycle autoscan...")
    print(f"Channels: {channels}")
    print(f"Measurement period: {period} minutes")
    print(f"Daily operating hours: {start_hour:02d}:00 to {end_hour:02d}:00")

    # Keep every PV module disconnected whenever no measurement is being taken.
    turn_off()

    try:
        while True:
            now = datetime.now()
            start_time_today, end_time_today = get_daily_window(
                now,
                start_hour,
                end_hour
            )

            # ----------------------------------------------------------
            # BEFORE 7 AM: wait until today's 7 AM
            # ----------------------------------------------------------
            if now < start_time_today:
                wait_seconds = (start_time_today - now).total_seconds()

                print(
                    f"Waiting until {start_time_today.strftime('%Y-%m-%d %H:%M:%S')} "
                    f"to begin measurements."
                )

                turn_off()
                time.sleep(wait_seconds)
                continue

            # ----------------------------------------------------------
            # AT/AFTER 8 PM: wait until 7 AM the next day
            # ----------------------------------------------------------
            if now >= end_time_today:
                next_start = (now + timedelta(days=1)).replace(
                    hour=start_hour,
                    minute=0,
                    second=0,
                    microsecond=0
                )

                wait_seconds = (next_start - now).total_seconds()

                print(
                    f"Daily measurement window finished. "
                    f"Waiting until {next_start.strftime('%Y-%m-%d %H:%M:%S')}."
                )

                turn_off()
                time.sleep(wait_seconds)
                continue

            # ----------------------------------------------------------
            # BETWEEN 7 AM AND 8 PM: perform today's measurements
            # ----------------------------------------------------------
            measurement_day = now.strftime("%Y-%m-%d")
            scan_num = 1
            last_uploaded_scan = 0

            print("\n=====================================")
            print(f"Starting measurements for {measurement_day}")
            print("=====================================")

            while datetime.now() < end_time_today:
                cycle_start_time = time.time()

                print("\n-------------------------------------")
                print(f"Starting scan cycle {scan_num}")
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                print("-------------------------------------")

                # With CYCLE_AUTOSCAN_CHANNELS = [1, 2], this scans PV1 then PV2.
                for channel in channels:
                    # Do not start another module if the daily end time was reached
                    # while the previous module was being measured.
                    if datetime.now() >= end_time_today:
                        break

                    print(f"Switching to PV module {channel}")
                    switch_relay(channel)

                    # Allow relay contacts to settle before starting the Prova scan.
                    time.sleep(1)

                    print(f"Scanning PV module {channel}")
                    data = autoscan(ser)

                    # Use one timestamp for decoding, CSV naming and graph naming
                    # so the CSV and PNG from one measurement match exactly.
                    measurement_time = datetime.now()

                    decoded_data = decode_curve(
                        data,
                        channel=channel,
                        sample_num=scan_num,
                        date_time=measurement_time
                    )

                    write_PV_data(
                        data=decoded_data,
                        channel=channel,
                        date_time=measurement_time
                    )

                    graph_PV_data(
                        sample_num=scan_num,
                        data=decoded_data,
                        channel=channel,
                        date_time=measurement_time
                    )

                print(f"Scan cycle {scan_num} complete.")

                # Upload after every 10 completed cycles.
                if scan_num % 10 == 0:
                    upload_data(today=measurement_day)
                    last_uploaded_scan = scan_num

                scan_num += 1

                # Keep cycle START times approximately <period> minutes apart.
                elapsed_time = time.time() - cycle_start_time
                remaining_time = period * 60 - elapsed_time

                if remaining_time <= 0:
                    print(
                        "WARNING: Measurement cycle took longer "
                        "than the requested period. Starting the next cycle immediately."
                    )
                    continue

                # Never sleep past 8 PM.
                seconds_until_end = (
                    end_time_today - datetime.now()
                ).total_seconds()

                if seconds_until_end <= 0:
                    break

                sleep_time = min(remaining_time, seconds_until_end)

                print(
                    f"Waiting {sleep_time:.1f} seconds "
                    "until the next measurement cycle."
                )

                time.sleep(sleep_time)

            # ----------------------------------------------------------
            # 8 PM: finish today's run, upload remaining files, then
            # return to the outer loop which waits for tomorrow at 7 AM.
            # ----------------------------------------------------------
            turn_off()

            completed_scans = scan_num - 1

            if completed_scans > last_uploaded_scan:
                upload_data(today=measurement_day)

            print(
                f"Measurements for {measurement_day} complete. "
                f"All relays are off."
            )

    except KeyboardInterrupt:
        print("\nProgram stopped by user.")

    finally:
        # Always disconnect PV modules when the program ends for any reason.
        turn_off()
        print("All PV relays are off.")


if __name__ == "__main__":
    if autorun:
        relay_setup()
        cycle_autoscan()
