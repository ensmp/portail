function createObject() {
var request_type;
var browser = navigator.appName;
if(browser == "Microsoft Internet Explorer"){
request_type = new ActiveXObject("Microsoft.XMLHTTP");
}else{request_type = new XMLHttpRequest();}
return request_type;
}

var http = createObject();

$(function() {
	//update_ratings();
	$('.unfavourite,.favourite').hover(function() {
		var favourite = $(this).hasClass('favourite') ? 'favourite' : 'unfavourite' ;
		if (!$(this).hasClass('clicked'))
			$(this).attr({'src':'/media/'+favourite+'hover.png'});
	},function() {
		var favourite = $(this).hasClass('favourite') ? 'favourite' : 'unfavourite' ;
		if (!$(this).hasClass('clicked'))
			$(this).attr({'src':'/media/'+favourite+'.png'});
	});
	
	
	
	
	
	/***  CLICK ***/
	$('.favourite,.unfavourite').click(function(event) {
	    event.preventDefault();
		var kind = $(this).parent().parent().attr('id');
		//var favourite = $(this).hasClass('favourite') ? 'favourite' : 'unfavourite' ;
		var csrf = $('input[name="csrfmiddlewaretoken"]').attr('value');
		if ($(this).hasClass('favourite')) {
		
			var lien=$(this).parent().attr("href");				
			http.open('get', lien+'classer_important/');
			//http.onreadystatechange = handleAJAXReturn1;
			http.send(null);
			/**document.getElementById("compteur_messages").firstChild.nodeValue--;
			divparent = $(event.target).parent().parent().parent();
			divparent.fadeOut(500);*/
			
		
		
		
		
			$(this).attr({'src':'/media/unfavourite.png'});
			$(this).addClass('unfavourite');
			$(this).removeClass('favourite');
		}
		else {
		
			var lien=$(this).parent().attr("href");				
			http.open('get', lien+'classer_non_important/');
			//http.onreadystatechange = handleAJAXReturn1;
			http.send(null);
		
			$(this).attr({'src':'/media/favourite.png'});
			$(this).addClass('favourite');
			$(this).removeClass('unfavourite');
		}
		/*if ($(this).hasClass('clicked'))
			$.post('/places/'+placename+'/favourite/',{csrfmiddlewaretoken:csrf,'kind':kind,action:'unlike'},function() {
				update_ratings();
			}).error(function(msg) {
					if (msg.status==403) window.location = '/facebook/login?next=/places/'+placename+'/';
			});
		else
			$.post('/places/'+placename+'/favourite/',{csrfmiddlewaretoken:csrf,'kind':kind,action:favourite},function() {
				
			}).error(function(msg) {
					if (msg.status==403) window.location = '/facebook/login?next=/places/'+placename+'/';
			});*/
		//	update_ratings();
	});
/*
	$('#likebar').hover(function() {
		$('#likecountbox').show();
	}, function() {
		$('#likecountbox').hide();
	});*/
});
/*
function update_ratings() {
	var criteria = new Array('service','value','ambiance','food','favourite');
	var placename = $('#placename').text();
	$.getJSON('/places/'+placename+'/favourite/stats/json',function(data){
		$.each(criteria, function(key, val){
			$('#'+val+' .rating').animate({width:3*data[val]});
		});	
		$('#likecountbox').html(data['favourite'] + ' favourite'
			+ (data['favourite'] == 1? '':'s') + ', ' + data['unfavourite']
			+ ' unfavourite' + (data['unfavourite'] == 1? '':'s'));
		if (data['favourite'] + data['unfavourite'] > 0) {
			likepct = 100 * (data['favourite']) / (data['favourite'] + data['unfavourite']);
			$('#likesbar').css({'background': '#3C2'}).animate({height:likepct+'%'});
			$('#unfavouritesbar').css({'background': '#F33'}).animate({height:(100-likepct)+'%'});
		}
	});
	$.getJSON('/places/'+placename+'/favourite/state/json',function(data) {
		$.each(criteria, function(key, val){
			update_rating_for_place(val,data[val]);
		});
		if (data['favourite'] == 'l'|data['favourite'] == 'd') {
			$('#likedetails .favourite,#likedetails .unfavourite').css({'display':'inline-block'});
		} else {
			$('#likedetails .favourite,#likedetails .unfavourite').css({'display':'none'});
		}
	});
}

function update_rating_for_place(kind,favourite) {
	switch (favourite) {
		case 'l':
			$('#'+kind+' .favourite').attr({'src':'/img/favourite.png'});
			$('#'+kind+' .favourite').addClass('clicked');
			$('#'+kind+' .unfavourite').attr({'src':'/img/defavoriser.png'});
			$('#'+kind+' .unfavourite').removeClass('clicked');
		break;
		case 'd':
			$('#'+kind+' .unfavourite').attr({'src':'/img/unfavourite.png'});
			$('#'+kind+' .unfavourite').addClass('clicked');
			$('#'+kind+' .favourite').attr({'src':'/img/favoriser.png'});
			$('#'+kind+' .favourite').removeClass('clicked');
		break;
		case 'n':
			$('#'+kind+' .unfavourite').attr({'src':'/img/defavoriser.png'});
			$('#'+kind+' .unfavourite').removeClass('clicked');
			$('#'+kind+' .favourite').attr({'src':'/img/favoriser.png'});
			$('#'+kind+' .favourite').removeClass('clicked');
		break;
	};
}*/


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