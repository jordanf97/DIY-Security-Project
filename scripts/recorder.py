import argparse
from picamera import PiCamera
parser = argparse.ArgumentParser()
parser.add_argument("duration")
args = parser.parse_args()


from datetime import datetime
import time
import subprocess
import os
import random
import string
import sqlite3

camera = PiCamera()

conn = sqlite3.connect(os.path.normpath(os.getcwd() + '/database.db'))

c = conn.cursor()

print("Recording service initiated!")
   
#filename = datetime.now().strftime("%Y-%m-%d_%H.%M.%S.h264")
filename = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
filename = filename + '.h264'
dir = "/var/www/html/project/frontend/inc/videos/"
camera.rotation = 180
camera.resolution = (1920, 1080)
camera.start_recording(dir + 'raw/' + filename)
print("Recording started!")
time.sleep(float(args.duration))
camera.stop_recording()
subprocess.call(["sudo", "MP4Box", "-add", dir + "raw/" + filename, dir + "proc/" + filename + ".mp4"])
filename = filename + '.mp4'
c.execute("INSERT INTO recorded VALUES (NULL, '" + filename + "', '" + str(time.time()) + "')")
conn.commit()
conn.close()

print("Recording finished!")