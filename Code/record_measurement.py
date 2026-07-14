from Prova_210_serial_comm import *
from prova_params import *

if __name__ == "__main__":
    print("Recording measurement...")
    relay_setup()
    data = autoscan()
    decoded = decode_curve(data)
    write_PV_data(decoded)
    graph_PV_data(1, decoded)
    print("Measurement recorded")