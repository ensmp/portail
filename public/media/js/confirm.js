function createObject() {
var request_type;
var browser = navigator.appName;
if(browser == "Microsoft Internet Explorer"){
request_type = new ActiveXObject("Microsoft.XMLHTTP");
}else{request_type = new XMLHttpRequest();}
return request_type;
}

var http = createObject();

jQuery.fn.fadeThenSlideToggle = function(speed, easing, callback) {
  if (this.is(":hidden")) {
    return this.slideDown(speed, easing).fadeTo(speed, 1, easing, callback).delay(5000);
  } else {
    return this.fadeTo(speed, 0, easing).slideUp(speed, easing, callback);
  }
};


$(function() {
	//update_ratings();
	
	
	
	/***  CLICK ***/
	$('.action_confirmer').click(function(event) {
	    event.preventDefault();
		var kind = $(this).parent().parent().attr('id');
		//var favourite = $(this).hasClass('favourite') ? 'favourite' : 'unfavourite' ;
		var csrf = $('input[name="csrfmiddlewaretoken"]').attr('value');
		
			var lien=$(this).parent().attr("href");				
			http.open('get', lien);
			//http.onreadystatechange = handleAJAXReturn1;
			http.send(null);
			
			if ($(this).hasClass('disparait')) {
			divparent = $(event.target).parent().parent();
			divparent.fadeThenSlideToggle();
			}
			setTimeout(function() {
			window.open('/billetterie','_self');}, 500);


		

	});
	
	
	
	
	
	
	
	/**READ**/
	$('.unread,.read').hover(function() {
		var read = $(this).hasClass('read') ? 'read' : 'unread' ;
		if (!$(this).hasClass('clicked'))
			$(this).attr({'src':'/media/'+read+'hover.png'});
	},function() {
		var read = $(this).hasClass('read') ? 'read' : 'unread' ;
		if (!$(this).hasClass('clicked'))
			$(this).attr({'src':'/media/'+read+'.png'});
	});
	
	
	
	
	
	/***  CLICK ***/
	$('.read,.unread').click(function(event) {
	    event.preventDefault();
		var kind = $(this).parent().parent().attr('id');
		//var read = $(this).hasClass('read') ? 'read' : 'unread' ;
		var csrf = $('input[name="csrfmiddlewaretoken"]').attr('value');
		if ($(this).hasClass('read')) {
		
			var lien=$(this).parent().attr("href");				
			http.open('get', lien+'lire/');
			//http.onreadystatechange = handleAJAXReturn1;
			http.send(null);
			
			document.getElementById("compteur_messages").firstChild.nodeValue--;
			if ($(this).hasClass('disparait')) {			
			
			divparent = $(event.target).parent().parent().parent().parent().parent().parent().parent();
			divparent.fadeThenSlideToggle();
			}

		
			$(this).attr({'src':'/media/unread.png'});
			$(this).addClass('unread');
			$(this).removeClass('read');
		}
		else {
		
			var lien=$(this).parent().attr("href");				
			http.open('get', lien+'classer_non_lu/');
			
			
			
			document.getElementById("compteur_messages").firstChild.nodeValue++;

			//http.onreadystatechange = handleAJAXReturn1;
			http.send(null);
		
			$(this).attr({'src':'/media/read.png'});
			$(this).addClass('read');
			$(this).removeClass('unread');
		}

	});

});


function handleAJAXReturn1()
{
    alert(http.readyState);
    if(http.readyState == 4)
    {
        if(http.status == 200)
        {
      //     alert(http.responseText);
        }
        else
        {
      //      alert("<strong>N/A</strong>");
        }
    }
}