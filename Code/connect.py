from Prova_210_serial_comm import *

if __name__ == "__main__":
    ser = serial.Serial(
        PORT,
        baudrate=BAUD,
        bytesize=8,
        parity='N',
        stopbits=1,
        timeout=1
    )
    
    establish_comms(ser)