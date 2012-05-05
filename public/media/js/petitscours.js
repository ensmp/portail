$(function() {


var map;
var markers = [];
var infowins = [];


	alert('function');

function addMarker(title, descr, lat, lng) {
  var marker = new google.maps.Marker({
    position: new google.maps.LatLng(lat, lng),
    map: map,
    title: title
  })
  markers.push(marker);
  var infowin = new google.maps.InfoWindow({
    content: '<p><b><a href=/places/' + encodeURI(title) + '/>' + title + '</a></b></p>' +
      '<p>' + descr + '</p>'
  });
  infowins.push(infowin);
  google.maps.event.addListener(marker, 'click', function() {
    for (var i=0; i<infowins.length; i++) {
      infowins[i].close();
    }
    infowin.open(map,marker);
  });
}




/*
  $('#map').hide()
  {% if loc %}
  var loc = new google.maps.LatLng({{loc.lat}}, {{loc.lng}})
  {% else %}
  var loc = new google.maps.LatLng(48.846596,2.34448);
  {% endif %}
  var myOptions = {
    zoom: 14,
    center: loc,
    mapTypeId: google.maps.MapTypeId.ROADMAP
	map = new google.maps.Map(document.getElementById("map"),
          myOptions);
  };


	$('#showmap').click(function(e) {
	alert('click');
    e.preventDefault();
    if (this.shown === undefined) {
      $('#map').show();
      this.shown = true;
      $(this).html('Masquer la carte');
    //  map = new google.maps.Map(document.getElementById("map"),
    //      myOptions);
      {% if loc %}addMarker('Ici', {{loc.lat}}, {{loc.lng}});{% endif %}{% for cours in cours_list %}{% if cours.latitude %}
      addMarker("{{cours.title}}", "{{cours.address}}", {{cours.latitude}}, {{cours.longitude}});{% endif %}{% endfor %}
    }
    else if (this.shown) {
      $('#map').hide();
      this.shown = false;
      $(this).html('Afficher la carte');
    } else {
      $('#map').show();
      this.shown = true;
      $(this).html('Masquer la carte');
    }
  });*/
});

 
  