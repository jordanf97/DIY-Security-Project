window.onload = function() {
	setTimeout(function() {
		$('#overlay').fadeOut();
	}, 1000);
	init();}

serviceList = {
	"stream": false,
	"security": false,
	"record": false
};

function init() {
	fetchVideos();
	fetchRecordedVideos();
	fetchServiceStats();
}
function fetchServiceStats() {
	resetServices();
	fetch('status', function(response) {
		services = JSON.parse(response);
		for(var i = 0; i < services.length; i++) {
			buttonCtrl(services[i], 'Deactivate');
			serviceList[services[i]] = true;
		}
		displayStream(serviceList['stream']);
	});
}

function resetServices() {
	for (var service in serviceList) {
		serviceList[service] = false;
		resetBtn(service);
	}
}
function resetBtn(service) {
	if(service != 'record') {
		btn = document.getElementById(service + '_service');
		btn.setAttribute('class', 'uk-button uk-button-primary');
		btn.innerHTML = 'Activate';
	}
}

function startRecordtime(duration) {
	hook = document.getElementById('hook');
	hook.innerHTML = '<h3 class="uk-heading-bullet">Recording</h3>';
	var progress = document.createElement('progress');
	progress.setAttribute('id', 'progressbar');
	progress.setAttribute('class', 'uk-progress');
	progress.setAttribute('value', '0');
	duration = (parseInt(duration) + 3);
	progress.setAttribute('max', duration);
	
	hook.appendChild(progress);
	var animate = setInterval(function () {
		progress.value += 0.125;
		if(progress.value >= progress.max) {
			clearInterval(animate);
			hook.innerHTML = '';
			location.reload();
		}
	}, 125);
}

function buttonCtrl(service, type) {
	
	resetBtn('stream');
	resetBtn('security');
	
	if(type == 'Activate') {
		typeC = 'primary';
	} else {
		typeC = 'danger';
	}
	btn = document.getElementById(services + "_service");
	btn.setAttribute('class', 'uk-button uk-button-' + typeC);
	btn.innerHTML = type;
}

function activateService(service) {
	if(serviceList[service] == true) {
		service = 'kill';
	}
	if(service == 'record') {
		duration = document.getElementById('duration').value;
		service = service + '/' + duration;
		startRecordtime(duration);
	}
	fetch('run/' + service, function(response) {
		fetchServiceStats();
	});
}

function displayStream(display) {
	if(display == true) {
		document.getElementById('streamFeed').src = window.location.href.slice(0, -1) + ":8080/?action=stream";
		document.getElementById('streamCont').style.display = "block";
	} else {
		document.getElementById('streamFeed').src = "";
		document.getElementById('streamCont').style.display = "none";
	}
}

function fetchVideos() {
	fetch('api/listvideos', function(response) {
		response = JSON.parse(response);
		for(var i = 0; i < response.length; i++) {
			addVideo(response[i][0], response[i][1]);
		}
	});
}

function fetchRecordedVideos() {
	fetch('api/listrecordedvideos', function(response) {
		response = JSON.parse(response);
		for(var i = 0; i < response.length; i++) {
			addVideo(response[i][0], response[i][1], 'recorded');
		}
	});
}

function deleteVideo(video) {
	fetch(video, function(response) {
		location.reload()
	});
}

function addVideo(path, date, type = null) {
	deletePath = 'deletevideo/' + path;
	if(type != null) {
		prnt = 'recordedVideoBox';
		deletePath = deletePath + '/0'
	} else {
		prnt = 'videoBox';
		deletePath = deletePath + '/1'
	}
	path = '/resource/mp4/' + path;
	video = document.createElement('li');
	videoContent = document.createTextNode(date);
	video.appendChild(videoContent);
	
	playButton = document.createElement('span');
	playButton.setAttribute("class", "uk-align-right");
	
	playButtonText = document.createElement('span');
	playButtonText.setAttribute("onclick", "deleteVideo('" + deletePath + "')");
	playButtonText.setAttribute("uk-icon", "icon: trash");
	playButton.appendChild(playButtonText);
	video.appendChild(playButton);
	
	deleteButton = document.createElement('span');
	deleteButton.setAttribute("class", "uk-align-right");
	
	deleteButtonText = document.createElement('a');
	deleteButtonText.setAttribute("href", path);
	deleteButtonText.setAttribute("uk-icon", "icon: play-circle");
	deleteButton.appendChild(deleteButtonText);
	video.appendChild(deleteButton);
	
	document.getElementById(prnt).appendChild(video);
}

function fetch(url, callback) {
	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function() {
		if (this.readyState == 4 && this.status == 200) {
		   callback(this.responseText);
		}
	};
	xhttp.open("GET", window.location.href + url, true);
	xhttp.send();
}