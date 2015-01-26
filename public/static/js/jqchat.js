// Chat client code.

// Keep track of the last message received (to avoid receiving the same message several times).
// This global variable is updated every time a new message is received.
var timestamp = 0;

// URL to contact to get updates.
var url = null;

// How often to call updates (in milliseconds)
var CallInterval = 8000;
// ID of the function called at regular intervals.
var IntervalID = 0;

// A callback function to be called to further process each response.
var prCallback = null;

var loadedOnce = false;

var unreadMessages = 0;

var origTitle = document.title;

var importantWords = ["philippe", "hitman", "piche"];

function callServer(){
	// At each call to the server we pass data.
	/**$.get(url, // the url to call.
			{time: timestamp}, // the data to send in the GET request.
			function(payload) { // callback function to be called after the GET is completed.
							alert('get ');
							processResponse(payload);
							},
			'json');*/
	$.getJSON(url, {time: timestamp}, function(data) {processResponse(data);});
	};

function processResponse(payload) {

	//If window active, reset unreadMessages counter and window title
	if (!document.hidden){
		unreadMessages = 0;
		document.title = origTitle;
	}

	// if no new messages, return.
	if(payload.status == 0) return;
	// Get the timestamp, store it in global variable to be passed to the server on next call.
	timestamp = payload.time;


	
	for(message in payload.messages) {
		messageText = payload.messages[message].text;
		$("#chatwindow").append(messageText);
		if (loadedOnce){
			pattern = "@" + myPseudo();
			if (messageText.search(pattern) > -1){
				if (document.hidden){
					unreadMessages++;
					document.title = "[" + unreadMessages + "] " + origTitle;
				}
				document.getElementById("notifSoundPlayer").play();
			}
			for (importantWord in importantWords){
				if (messageText.toLowerCase().search(importantWords[importantWord]) > -1){
					document.getElementById("importantSoundPlayer").play();
				}
			}
		}
	}
	loadedOnce = true;
	// Scroll down if messages fill up the div.
	var objDiv = document.getElementById("chatwindow");
	objDiv.scrollTop = objDiv.scrollHeight;

	// Handle custom data (data other than messages).
	// This is only called if a callback function has been specified.
	if(prCallback != null) prCallback(payload);
}

function InitChatWindow(ChatMessagesUrl, ProcessResponseCallback){
/**   The args to provide are:
	- the URL to call for AJAX calls.
	- A callback function that handles any data in the JSON payload other than the basic messages.
	  For example, it is used in the example below to handle changes to the room's description. */	
	$("#loading").remove(); // Remove the dummy 'loading' message.

	// Push the calling args into global variables so that they can be accessed from any function.
	url = ChatMessagesUrl;
	prCallback = ProcessResponseCallback;

	// Read new messages from the server every X milliseconds.
	IntervalID = setInterval(callServer, CallInterval);

	// The above will trigger the first call only after X milliseconds; so we
	// manually trigger an immediate call.
	callServer();

	// Process messages input by the user & send them to the server.
	$("form#chatform").submit(function(){
		// If user clicks to send a message on a empty message box, then don't do anything.
		if($("#msg").val() == "") return false;

		// We don't want to post a call at the same time as the regular message update call,
		// so cancel that first.
		clearInterval(IntervalID);
		
		$.ajaxSetup({ 
			 beforeSend: function(xhr, settings) {
				 function getCookie(name) {
					 var cookieValue = null;
					 if (document.cookie && document.cookie != '') {
						 var cookies = document.cookie.split(';');
						 for (var i = 0; i < cookies.length; i++) {
							 var cookie = jQuery.trim(cookies[i]);
							 // Does this cookie string begin with the name we want?
						 if (cookie.substring(0, name.length + 1) == (name + '=')) {
							 cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
							 break;
						 }
					 }
				 }
				 return cookieValue;
				 }
				 if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
					 // Only send the token to relative URLs i.e. locally.
					 xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
				 }
			 } 
		});

		var msg_post = $("#msg").val();
		$("#msg").val(""); // clean out contents of input field.
		
		$.post(url,
				{
				time: timestamp,
				action: "postmsg",
				message: msg_post
           		},
           		function(payload) {         						
         						// Calls to the server always return the latest messages, so display them.
         						processResponse(payload);
       							},
       			'json'
       	);
		msg_post = "";
       	
       	// Start calling the server again at regular intervals.
       	IntervalID = setInterval(callServer, CallInterval);
       	
		return false;
	});


} // End InitChatWindow

/**	This code below is an example of how to extend the chat system.
 * It's used in the second example chat window and allows us to manage a user-updatable
 * description field.
 *  */

// Callback function, processes extra data sent in server responses.
function HandleRoomDescription(payload) {
	$("#chatroom_description").text(payload.description);
}

function InitChatDescription(){

	$("form#chatroom_description_form").submit(function(){
		// If user clicks to send a message on a empty message box, then don't do anything.
		if($("#id_description").val() == "") return false;
		// We don't want to post a call at the same time as the regular message update call,
		// so cancel that first.
		clearInterval(IntervalID);
		$.post(url,
				{
				time: timestamp,
				action: "change_description",
				description: $("#id_description").val()
           		},
           		function(payload) {
         						$("#id_description").val(""); // clean out contents of input field.
         						// Calls to the server always return the latest messages, so display them.
         						processResponse(payload);
       							},
       			'json'
       	);
       	// Start calling the server again at regular intervals.
       	IntervalID = setInterval(callServer, CallInterval);
		return false;
	});

}