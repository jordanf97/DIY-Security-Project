function login() {
	username = document.getElementById('username').value
	password = document.getElementById('password').value
	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function() {
		if (this.readyState == 4 && this.status == 200) {
			if(this.responseText == '1') {
				location.reload();
			} else {
				hook = document.getElementById('hook');
				hook.innerHTML = '<div class="uk-alert-danger" uk-alert><a class="uk-alert-close" uk-close></a><p>You have entered an invalid username or password!</p></div>';
			}
		}
	};
	
	params = "username=" + username + "&password=" + password;
	xhttp.open("POST", "/login", true);
	xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
	xhttp.send(params);
	return false;
}