import os
import subprocess

full_path = "/var/www/html/test/mjpg-streamer-master/mjpg-streamer-experimental"
os.chdir(full_path)

subprocess.call(['./mjpg_streamer', '-o', 'output_http.so -w ./www', '-i', 'input_raspicam.so'])



