# Workflow
From PC:
1. SSH into Raspberry Pi: (Opens a terminal)
   - Open terminal on your computer
   - Ensure you are connected to the same wifi network as the Pi (SERIS CTO 1)
   - Type `ssh seris@192.168.20.146` (if this does not work, check that the Pi is connected to the right wifi network. Then check it's ip address --- the ssh command will be `ssh seris@\<ip address\>`)
   - Enter the password: `solar2941`
   Run startup/connect Pi to PROVA
   - Ensure that the PROVA is turned on and connected to the Pi via USB
   - Run the setup script `setup.py` by typing `python setup.py` --- this should change your directory and connect to the prova
   - You can: run the provided scripts (upload_dat.py, record_measurement.py, etc.) by typing `python \<name of script\>`; run specific functions from the terminal by typing `python import Prova_210_serial_comm; Prova_210_serial_comm.\<function name\>`; or write your own python script, importing `Prova_210_serial_comm` and ensuring that the script is saved in the correct folder

2. VNC to Raspberry Pi: (Gives you virtual access to the Pi desktop)
   - Download RealVNC Viewer: https://www.realvnc.com/en/connect/download/viewer/?lai_sr=5-9&lai_sl=l&lai_p=1&lai_na=611310
   - Open VNC Viewer. If you do not already have an account, you will need to make one. You can get a free account using a lite plan for non-commercial use only. 
   - Type `192.168.20.146` into the search bar. (if this does not work, check that the Pi is connected to the right wifi network. Then check it's ip address --- your search command should be the Pi's IP address)
   - Enter `seris` as the username and `solar2941` as the password
   - Navigate to Thonny IDE (Raspberry pi icon in top left > Programming > Thonny), and open the script `Prova_210_serial_comm.py` (File > Open > seris/Documents/SERIS-Prova_210_GitHome/Code/Prova_210_serial_comm.py)
   - In the `if __name__ == "__main__"` block, write the commands you want executed. Or, run the script (green run button on top left) and then type your commands one at a time into the terminal at the bottom of the IDE.
