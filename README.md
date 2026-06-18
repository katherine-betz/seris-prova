# Workflow
From PC:
1. SSH into Raspberry Pi: (Opens a terminal)
   - Open terminal on your computer
   - Ensure you are connected to the same wifi network as the Pi (SERIS CTO 1)
   - Type `ssh seris@192.168.20.146` (if this does not work, check that the Pi is connected to the right wifi network. Then check it's ip address --- the ssh command will be `ssh seris@\<ip address\>`)
   - Enter the password: `solar2941`
   Run startup/connect Pi to PROVA
   - Ensure that the PROVA is turned on and connected to the Pi via USB
   - Run the setup script `setup.py` by typing `python setup.py` --- this should change your directory
   - Import the script's commands: `import Prova_210_serial_comm.py`
   - Type the commands you wish to use into the terminal --- for example, `autoscan()` or `upload_data()`. A full list of commands, and their functionality, can be found at (PUT PATH HERE ONCE YOU MAKE THE FILE)

2. VNC to Raspberry Pi: (Gives you virtual access to the Pi desktop)
   - Download RealVNC Viewer: https://www.realvnc.com/en/connect/download/viewer/?lai_sr=5-9&lai_sl=l&lai_p=1&lai_na=611310
   - Open VNC Viewer
   - Type 192.168.20.146 into the search bar. (if this does not work, check that the Pi is connected to the right wifi network. Then check it's ip address --- your search command should be the Pi's IP address)
   - Navigate to Thonny IDE, and open the script `Prova_210_serial_comm.py`
   - In the `if __name__ == "__main__"` block, write the commands you want executed. Or, run the script (green run button on top left) and then type your commands one at a time into the terminal at the bottom of the IDE. 
