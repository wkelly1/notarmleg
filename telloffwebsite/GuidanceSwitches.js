function runOnLoad() {
	var mailURL = decodeURIComponent(window.location.href);
	mailURL = mailURL.substring(mailURL.indexOf("?")+1, mailURL.length);
	console.log(mailURL);
	var request = new XMLHttpRequest();
	request.open('GET', mailURL+"features.json");
	request.responseType = 'text';
	request.onload = function() {
		appendFeatures(request.response);
	};
	request.send();
	document.body.append("test");
}


function appendFeatures(featuresJSON) {
	document.body.append(featuresJSON);
}
