import serial
import struct
import time
import sh, os
import subprocess
import csv
from datetime import datetime
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
GIT_TOKEN = "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"

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
    print("Changing", param_name, "to", str(param_value), "...")
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

# Loads stored PV data from PROVA 210 solar module (does with the software installed, without it idk)
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
    print("Loaded recorded logs:", data) # HERE -- need to decode
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
    
def load_LCD(ser = SER): # not sure what this will do on the pi
    ser.write(b'*')
    
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
def decode_curve(dat, channel=CHANNEL, packet_size=8, sample_num=1, date_time=None):
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
        ["Ishort (A)", I_short],
        ["Vmaxp (V)", V_max_P],
        ["Imaxp (A)", I_max_P],
        ["Pmax (W)", P_max],
        ["V (V)", "I (A)", "P (W)"]# header row for the rest of the measurments
    ]
    for i in range(0, len(measurements), 2):
        result.append([float(int(measurements[i], 16))/1000.0, float(int(measurements[i+1], 16))/10.0, float(int(measurements[i], 16)*int(measurements[i+1], 16))/10000])
    result.append(["END OF SAMPLE"])
    result.append([])
    print("Processsing complete")
    return result

def decode_log_curve(dat, channel=CHANNEL, packet_size = 4, header_length = 4, footer_length = 12):
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
        ["Ishort (A)", I_short],
        ["Vmaxp (V)", V_max_P],
        ["Imaxp (A)", I_max_P],
        ["Pmax (W)", P_max],
        ["V (V)", "I (A)", "P (W)"] # header row for the rest of the measurments
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
    
# This function takes in data formatted as a list of lists, and writes it to a csv file, making each sublist its own row
# This function also adds the created file to the next git commit (this is easier than having to keep track of all the files but maybe bad practice so I might change)
# HERE -- return something to indicate success/failure???
def write_PV_data(data=[], channel=CHANNEL, today=TODAY, filename=None):
    print("Writing PV data...")

    if not os.path.isdir(f"{REPO_DIR}/Data/Channel_{channel}"):
        os.mkdir(f"{REPO_DIR}/Data/Channel_{channel}")
    if filename is None:
        filename = f"{REPO_DIR}/Data/Channel_{channel}/data_{today}.csv"
    else:
        filename = f"{REPO_DIR}/Data/Channel_{channel}/{filename}.csv"
        
    with open(filename, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(data)
    add_file(filename)
    print("Write complete")
    
# This function uploads data to git, using already added files and adding files if needed
def upload_data(today=TODAY, channel=CHANNEL, files_to_add=None):
    print("Uploading data...")

    if files_to_add is not None:
        for filename in files_to_add:
            add_file(filename)
    
    os.chdir(f"{REPO_DIR}/Data/Channel_{channel}") # assert correct directory
    sh.git("pull")
    sh.git("commit", "-m", f"\"Add data from {today}\"")
    sh.git("push")
    print("Upload complete")

# Takes an autoscan of each of the channels listed every <period> minutes
def cycle_autoscan(ser=SER, period=1, num_scans=100, channels=[1], today=TODAY):
    # Minimum scan time is around 30 sec for one scan
    if period > len(channels)/2:
        print(f"ERROR: Period too short. Setting period to {len(channels)/2} min")
    scan_num = 1
    data = None
    decoded_data = None
    print("Beginning cycle autoscan...")

    
    while (scan_num <= num_scans):
        start_time = time.time()
        for channel in channels:
            select_channel(channel)
            data = autoscan()
            decoded_data = decode_curve(data, channel=channel, sample_num=scan_num, date_time=datetime.now())
            write_PV_data(data=decoded_data, today=today, channel=channel)
        scan_num += 1
        end_time = time.time()
        time.sleep(period*60-(end_time-start_time))
    print("Autoscan complete")
    upload_data(today=today)
    
if __name__ == "__main__":
    if autorun == True:
        relay_setup()
        switch_relay(1)
        data = autoscan()
        decoded = decode_curve(data, sample_num=1)
        write_PV_data(decoded, filename = "PRELIMINARY_module_A_relay_wires_two_wire_measurement")
        print(CHANNEL)
        switch_relay(2)
        print(CHANNEL)
        data = autoscan()
        decoded = decode_curve(data, sample_num=1)
        write_PV_data(decoded, filename = "PRELIMINARY_module_B_relay_wires_two_wire_measurement")
        upload_data()
        print(CHANNEL)