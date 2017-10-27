from gpiozero import MotionSensor
from picamera import PiCamera

import socket
import time
import subprocess
import sqlite3
import os
import random
import string

ipAddress = [l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0]

domain = "http://" + ipAddress

camera = PiCamera()
pir = MotionSensor(4)

conn = sqlite3.connect(os.path.normpath(os.getcwd() + '/database.db'))
print("Security system initiated!")

c = conn.cursor()

while True:
	pir.wait_for_motion()
	print("recording started")
	filename = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
	filename = filename + '.h264'
	#filename = datetime.now().strftime("%Y-%m-%d_%H.%M.%S.h264")
	dir = "/var/www/html/project/frontend/inc/videos/"
	camera.rotation = 180
	camera.resolution = (1920, 1080)
	camera.start_recording(dir + "raw/" + filename)
	pir.wait_for_no_motion()
	print("recording stopped")
	camera.stop_recording()
	subprocess.call(["sudo", "MP4Box", "-add", dir + "raw/" + filename, dir + "proc/" + filename + ".mp4"])
	filename = filename + '.mp4'
	c.execute("INSERT INTO `videos` VALUES (NULL, '" + filename + "', '" + str(time.time()) + "')")
	conn.commit()
	subprocess.call(["python3.6", "scripts/sms.py", "Movement has been Detected in your home! View all system data at: " + domain])

conn.close()