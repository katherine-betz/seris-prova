# System
This repo contains documentaton and code required to perform remote mini module measurments using a Prova 210 measurement device, a Raspberry Pi, and a relay module. Capable of switching between __ modules, performing automated measurements, and automatically hosting data on the cloud, this project (is useful because...?)

# Materials
- Prova 210 PV Analyzer  
- Raspberry Pi 400
- HL-58S V1.2 5V, 8-channel optical isolated relay module

# Workflow
From GitHub:
1. Edit 'prova_params.py':
   - Open the file 'Code/prova_params.py' on this GitHub repo (insert a link??)
   - Edit parameters to your liking and set 'autorun=True' (This makes the pi run the cycle scan software automatically)
   - Wait up to 60 seconds for your changes to take effect. Data will be uploaded to GitHub for you to view

From PC:
1. SSH into Raspberry Pi: (Opens a terminal)
   - Open terminal on your computer
   - Ensure you are connected to the same wifi network as the Pi (in lab, SERIS CTO 1, on roof NAME_HERE)
   - Type `ssh seris@\<local-ip-address\>` (in the lab, this command is `ssh seris@192.168.20.146`, on the roof, it is `ssh seris@10.16.241.117) (if this does not work, check that the Pi is connected to the right wifi network. Then check it's ip address --- the ssh command will be `ssh seris@\<local-ip-address\>`)
   - Enter the password: `solar2941`
   Run startup/connect Pi to PROVA
   - Ensure that the PROVA is turned on and connected to the Pi via USB
   - Run the setup script `setup.py` by typing `python setup.py` --- this should change your directory and connect to the prova
   - You can: run the provided scripts (upload_dat.py, record_measurement.py, etc.) by typing `python \<name of script\>`; run specific functions from the terminal by typing `python import Prova_210_serial_comm; Prova_210_serial_comm.\<function name\>`; or write your own python script, importing `Prova_210_serial_comm` and ensuring that the script is saved in the correct folder

2. VNC to Raspberry Pi: (Gives you virtual access to the Pi desktop)
   - Download RealVNC Viewer: https://www.realvnc.com/en/connect/download/viewer/?lai_sr=5-9&lai_sl=l&lai_p=1&lai_na=611310
   - Open VNC Viewer. If you do not already have an account, you will need to make one. You can get a free account using a lite plan for non-commercial use only. 
   - Type the Pi's local ip address (in lab: `192.168.20.146`, on roof: `10.16.241.117` for wired connection, `10.16.241.117` for wireless) into the search bar. (If this does not work, check that the Pi is connected to the right wifi network. Then check the Pi's local ip address --- this can be done by typing `ping raspberrypi.local -4` into terminal on PC connected to wifi)
   - Enter `seris` as the username and `solar2941` as the password
   - Navigate to Thonny IDE (Raspberry pi icon in top left > Programming > Thonny), and open the script `Prova_210_serial_comm.py` (File > Open > seris/Documents/SERIS-Prova_210_GitHome/Code/Prova_210_serial_comm.py)
   - In the `if __name__ == "__main__"` block, write the commands you want executed. Or, run the script (green run button on top left) and then type your commands one at a time into the terminal at the bottom of the IDE.

# Hosting??
- Currently data is just stored here, in the data folder
- Working on setting up a GitHub pages to try to make this pretty
