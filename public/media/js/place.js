$(function() {
	update_ratings();
	$('.unfavorite,.favorite').hover(function() {
		var favorite = $(this).hasClass('favorite') ? 'favorite' : 'unfavorite' ;
		if (!$(this).hasClass('clicked'))
			$(this).attr({'src':'/img/'+favorite+'hover.png'});
	},function() {
		var favorite = $(this).hasClass('favorite') ? 'favorite' : 'unfavorite' ;
		if (!$(this).hasClass('clicked'))
			$(this).attr({'src':'/img/'+favorite+'ns.png'});
	});
	$('.favorite,.unfavorite').click(function() {
		var placename = $('#placename').text();
		var kind = $(this).parent().parent().attr('id');
		var favorite = $(this).hasClass('favorite') ? 'favorite' : 'unfavorite' ;
		var csrf = $('input[name="csrfmiddlewaretoken"]').attr('value');
		if ($(this).hasClass('clicked'))
			$.post('/places/'+placename+'/favorite/',{csrfmiddlewaretoken:csrf,'kind':kind,action:'unlike'},function() {
				update_ratings();
			}).error(function(msg) {
					if (msg.status==403) window.location = '/facebook/login?next=/places/'+placename+'/';
			});
		else
			$.post('/places/'+placename+'/favorite/',{csrfmiddlewaretoken:csrf,'kind':kind,action:favorite},function() {
				update_ratings();
			}).error(function(msg) {
					if (msg.status==403) window.location = '/facebook/login?next=/places/'+placename+'/';
			});
	});

	$('#likebar').hover(function() {
		$('#likecountbox').show();
	}, function() {
		$('#likecountbox').hide();
	});
});

function update_ratings() {
	var criteria = new Array('service','value','ambiance','food','favorite');
	var placename = $('#placename').text();
	$.getJSON('/places/'+placename+'/favorite/stats/json',function(data){
		$.each(criteria, function(key, val){
			$('#'+val+' .rating').animate({width:3*data[val]});
		});	
		$('#likecountbox').html(data['favorite'] + ' favorite'
			+ (data['favorite'] == 1? '':'s') + ', ' + data['unfavorite']
			+ ' unfavorite' + (data['unfavorite'] == 1? '':'s'));
		if (data['favorite'] + data['unfavorite'] > 0) {
			likepct = 100 * (data['favorite']) / (data['favorite'] + data['unfavorite']);
			$('#likesbar').css({'background': '#3C2'}).animate({height:likepct+'%'});
			$('#unfavoritesbar').css({'background': '#F33'}).animate({height:(100-likepct)+'%'});
		}
	});
	$.getJSON('/places/'+placename+'/favorite/state/json',function(data) {
		$.each(criteria, function(key, val){
			update_rating_for_place(val,data[val]);
		});
		if (data['favorite'] == 'l'|data['favorite'] == 'd') {
			$('#likedetails .favorite,#likedetails .unfavorite').css({'display':'inline-block'});
		} else {
			$('#likedetails .favorite,#likedetails .unfavorite').css({'display':'none'});
		}
	});
}
function update_rating_for_place(kind,favorite) {
	switch (favorite) {
		case 'l':
			$('#'+kind+' .favorite').attr({'src':'/img/favorite.png'});
			$('#'+kind+' .favorite').addClass('clicked');
			$('#'+kind+' .unfavorite').attr({'src':'/img/defavoriser.png'});
			$('#'+kind+' .unfavorite').removeClass('clicked');
		break;
		case 'd':
			$('#'+kind+' .unfavorite').attr({'src':'/img/unfavorite.png'});
			$('#'+kind+' .unfavorite').addClass('clicked');
			$('#'+kind+' .favorite').attr({'src':'/img/favoriser.png'});
			$('#'+kind+' .favorite').removeClass('clicked');
		break;
		case 'n':
			$('#'+kind+' .unfavorite').attr({'src':'/img/defavoriser.png'});
			$('#'+kind+' .unfavorite').removeClass('clicked');
			$('#'+kind+' .favorite').attr({'src':'/img/favoriser.png'});
			$('#'+kind+' .favorite').removeClass('clicked');
		break;
	};
}