from Prova_210_serial_comm import *

if __name__ == "__main__":
    os.chdir(Prova_210_serial_comm.REPO_DIR)
    establish_comms()
    relay_setup()