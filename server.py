from aiohttp import web
import subprocess
from time import sleep
import os
import sqlite3
import json
import datetime
import random
import string

security = None
stream = None
database = os.path.normpath(os.getcwd() + '/database.db')
secret = ""

def killServices():
	global security, stream

	if security is not None:
		security.kill()
		security.wait()
		security = None
	
	if stream is not None:
		stream.kill()
		stream.wait()
		stream = None


def controller(request):
	process = request.match_info.get('process', "none")
	duration = request.match_info.get('duration', 5)
	
	global security, stream
	
	if process != "none":
		killServices()
	
		if process == "security":
			security = subprocess.Popen(["python", "/var/www/html/project/scripts/motion-cam.py"])
			return "Security system started!"
		elif process == "stream":
			full_path = "/var/www/html/project/streamer"
			os.chdir(full_path)

			stream = subprocess.Popen(['./mjpg_streamer', '-o', 'output_http.so -w ./www', '-i', 'input_raspicam.so'])
			print("Streaming service started!")
			return "<img src='http://192.168.1.101:8080/?action=stream' />"
		elif process == "record":
			recorder = subprocess.Popen(["python", "scripts/recorder.py", duration])
		else:
			return "All processes killed!"

async def handle(request):	
	return web.Response(text = controller(request))
	
async def homepage(request):
	os.chdir('/var/www/html/project')
	
	if authen(request) is True:
		response = web.FileResponse('frontend/index.html') 
	else:
		response = web.FileResponse('frontend/login.html')
		
	response.headers["Content-Type"] = "text/html"
	response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
	response.headers["Pragma"] = "no-cache"
	response.headers["Expires"] = "0"
	
	return response
	
	

def authen(request):
	global secret
	if 'auth' not in request.cookies:
		return False
	secret = str(secret)
	cookie = str(request.cookies['auth'])

	if secret == cookie:
		return True
	return False


	
async def resource(request):
	type = request.match_info.get("type", "")
	name = request.match_info.get("name", "")
	types = {
		"css": ["text/css", ".css"],
		"js": ["text/javascript", ".js"],
		"mp4": ["video/mp4", '.h264.mp4']
	}
	
	if type in types:
		path = 'frontend/inc/' + type + '/' + name + types[type][1]
		if(type == 'mp4'):
			name = name.split('.')
			name = name[0]
			path = 'frontend/inc/videos/proc/' + name + types[type][1]
		if os.path.isfile(path):
			return web.FileResponse(path)
		else:
			return web.Response(text = "404 not found")

	else:
		return web.Response(text = "404 not found")
	
	
async def deleteVideo(request):
	name = request.match_info.get("name", "")
	type = request.match_info.get("type", "")
	path = '/var/www/html/project/frontend/inc/videos/proc/'
	file = path + name
	if os.path.isfile(file):
		response = "Deleted"
		global database
		conn = sqlite3.connect(database)
		c = conn.cursor()
		os.remove(file)
		if type == '1':
			table = 'videos'
		else:
			table = 'recorded'
		param = (name,)
		c.execute("DELETE FROM " + table + " WHERE name = ?", param)
		conn.commit()
		conn.close()
	else:
		response = "File not found"
		
	return web.Response(text = response)
	
async def listVids(request):
	global database
	conn = sqlite3.connect(database)
	c = conn.cursor()
	
	videos = []
	for row in c.execute("SELECT name, date FROM videos"):
		video = []
		video.append(row[0])
		video.append(datetime.datetime.fromtimestamp(int(row[1].split('.')[0])))
		video[1] = video[1].strftime('%A %d. %B %Y %H:%M:%S')
		videos.append(video)
	conn.close()
	
	return web.Response(text = json.dumps(videos))
	
async def listRecorded(request):
	global database
	conn = sqlite3.connect(database)
	c = conn.cursor()
	
	videos = []
	
	for row in c.execute("SELECT name, date FROM recorded"):
		video = []
		video.append(row[0])
		video.append(datetime.datetime.fromtimestamp(int(row[1].split('.')[0])))
		video[1] = video[1].strftime('%A %d. %B %Y %H:%M:%S')
		videos.append(video)
	conn.close()
	
	return web.Response(text = json.dumps(videos))
	
	
async def statcheck(request):
	global security, stream
	services = []
	if stream is not None:
		services.append('stream')
	if security is not None:
		services.append('security')
		

	return web.Response(text = json.dumps(services))

async def login(request):
	global secret
	
	data = await request.post()
	username = data['username']
	password = data['password']
	
	#insecure as meant to be used locally
	if username == 'admin' and password == 'admin':
		secret = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))

		response = web.Response(text = '1')
		response.set_cookie(name = 'auth', value = secret)
	else:
		response = web.Response(text = '0')
	return response
	
app = web.Application()
app.router.add_get('/', homepage)
app.router.add_get('/run/{process}', handle)
app.router.add_get('/run/{process}/{duration}', handle)
app.router.add_get('/resource/{type}/{name}', resource)
app.router.add_get('/api/listvideos', listVids)
app.router.add_get('/api/listrecordedvideos', listRecorded)
app.router.add_get('/status', statcheck)
app.router.add_get('/deletevideo/{name}/{type}', deleteVideo)
app.router.add_post('/login', login)

web.run_app(app, host = "0.0.0.0", port=80)
