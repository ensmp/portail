$(function() {
	var geocoder = new google.maps.Geocoder();

	var parisBounds = new google.maps.LatLngBounds(
		new google.maps.LatLng(48.682902,2.052917),
		new google.maps.LatLng(49.003746,2.646179));
	var addrInput = document.getElementById('addressinput');

	var autocomplete = new google.maps.places.Autocomplete(addrInput);
	autocomplete.setBounds(parisBounds);

	google.maps.event.addListener(autocomplete, 'place_changed', function() {
		$('.pac-container').addClass('.chzn-container .chzn-drop .chzn-results');
	});

	$('#addform').submit(function(e) {
		e.preventDefault();
		var noError = true;
		var address = $('input[name="address"]').val();		
		geocoder.geocode({ 'address': address },
			function(results, status) {
				if (status == google.maps.GeocoderStatus.OK) {
					$('input[name="address"]').val(results[0].formatted_address);
					$('input[name="lat"]').val(results[0].geometry.location.lat());
					$('input[name="lng"]').val(results[0].geometry.location.lng());
					var data = $('#addform').serialize();
					$.post('/petitscours/demander/', data, function(res) {
						if (res == 'OK') {
							$('#effectue').show();
							$('input[type="text"], textarea').val('');
						}
						else {
							alert(res);
						}
					});
				} else {
					noError = false;
					alert('Error in geocoding');
				}
			}
		);
	});
});
