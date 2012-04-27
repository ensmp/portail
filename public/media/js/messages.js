
	/* ---------------------------- */
/* XMLHTTPRequest Enable */
/* ---------------------------- */
function createObject() {
var request_type;
var browser = navigator.appName;
if(browser == "Microsoft Internet Explorer"){
request_type = new ActiveXObject("Microsoft.XMLHTTP");
}else{
request_type = new XMLHttpRequest();
}
return request_type;
}

var http = createObject();

/* -------------------------- */
/* INSERT */
/* -------------------------- */
/* Required: var nocache is a random number to add to request. This value solve an Internet Explorer cache issue */
var nocache = 0;
function action(page) {
// Optional: Show a waiting message in the layer with ID login_response
//document.getElementById('insert_response').innerHTML = "Just a second..."
// Required: verify that all fileds is not empty. Use encodeURI() to solve some issues about character encoding.
//var site_url= encodeURI(document.getElementById('site_url').value);
//var site_name = encodeURI(document.getElementById('site_name').value);
// Set te random number to add to URL request
nocache = Math.random();
// Pass the login variables like URL variable
http.open('get', page+nocache);
http.onreadystatechange = insertReply;
http.send(null);
}
function insertReply() {
if(http.readyState == 4){
var response = http.responseText;
// else if login is ok show a message: "Site added+ site URL".
//document.getElementById('insert_response').innerHTML = 'Site added:'+response;
}
}
	
$(document).ready(function()
{
    $('a.action_message').click(function(event){
		
        event.preventDefault();
        var link=$(this).attr("href");
		divparent = $(event.target).parent().parent().parent();
        
		document.getElementById("compteur_messages").firstChild.nodeValue--;
		
		divparent.fadeOut(500, function(){
           //  window.location.href =link;
		   action(link);
        });
    });
});