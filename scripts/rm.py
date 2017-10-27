from glob import glob
import os
import sqlite3

dir = "/var/www/html/project/frontend/inc/videos/"

conn = sqlite3.connect(os.path.normpath(os.getcwd() + '/database.db'))
c = conn.cursor()

c.execute("DELETE FROM videos")
c.execute("DELETE FROM recorded")
conn.commit()

conn.close()

for file in glob(dir + "raw/*"):
	if os.path.isfile(file):
		os.remove(file)
		print(file, "has been deleted")
for file in glob(dir + "proc/*"):
	if os.path.isfile(file):
		os.remove(file)
		print(file, "has been deleted")
		
for file in glob(dir + "proc/recorded/*"):
	if os.path.isfile(file):
		os.remove(file)
		print(file, "has been deleted")
print("emptied")

