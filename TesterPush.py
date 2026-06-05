import sh, os
import subprocess
from datetime import datetime
GIT_TOKEN = "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"

#Hi! This is a python script where I will be attempting to push data to github!

# initializing random data just to practice pushing, will need to figure out
# how we want data fromatted (CSV files?) as we push -- potential is CSV files that are uploaded to a specific folder, folder indicates the session that they were recorded in, naming convention just basic PV_test_date or smth
data = {'00', '01', '02', '03', '04', '05'}

# navigating to the repository directory -- ensures that the files are pushed to the correct place
repo_dir = r"/home/seris/Documents/Random Git Stuff"

def add_file(filename):
    os.chdir(repo_dir)
    sh.git(f"add .")

def log_data(data):
    today = datetime.today()
    print(today)
    for dat in data: # change this to be for csv files in a folder and push the files, maybe rename?
        print(dat)
        date = datetime.now() # don't do this in the final because you are using the time at time of logging and not the time of recording
        file = open(f"data_{date}.txt", 'w')
        print("open")
        file.write(dat)
        file.close()
        print("close")
        #add_file(f"data_{date}.txt") # push all the files from a given day to the same folder,
                                    # could change to make it so that the folders are named after sessions or smth, to allow for changing panels etc.
    subprocess.run(["git", "add", "."])
    sh.git("commit", "-m", f"\"Add data from {today}\"")
    sh.git("push")

if __name__ == "__main__":
    log_data(data)
