# Workflow
From PC:
1. SSH into Raspberry Pi:
   - open terminal on your computer
   - Ensure you are connected to the same wifi network as the Pi (SERIS CTO 1)
   - type `ssh seris@192.168.20.146` (if this does not work, check that the Pi is connected to the right wifi network. Then check it's ip address -- the ssh command will be `ssh seris@\<ip address\>`)
2. Run startup/connect Pi to PROVA
   - ensure that the PROVA is turned on
   - run the script `Prova_210_serial_comm.py` by typing `python Prova_210_serial_comm.py`
   - import the script's commands: `import Prova_210_serial_comm.py`
   - type the commands you wish to use into the terminal -- for example, `autoscan()` or `upload_data()`. A full list of commands, and their functionality, can be found at (PUT PATH HERE ONCE YOU MAKE THE FILE)
