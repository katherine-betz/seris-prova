# This file is the file run by the automatic background process of the pi (this is the program that runs when autorun=True in prova_params.py)
#

from Prova_210_serial_comm import *
from prova_params import *

if __name__ == "__main__":
    print("Starting automatic measurement...")
    establish_comms()
    relay_setup()
    cycle_autoscan(loop_indef = True)
    print("Measurement recorded")