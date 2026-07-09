from Prova_210_serial_comm import *

if __name__ == "__main__":
    data = autoscan()
    decoded = decode_curve(data)
    write_PV_data(decoded)