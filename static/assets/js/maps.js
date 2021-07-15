var map;
var marker;
var cityCircle;

function initMap() {
  var myCenter = new google.maps.LatLng(37.0902, 263.7129);
  var mapProp = {
    center: myCenter,
    zoom: 3.65,
    mapTypeId: google.maps.MapTypeId.HYBRID
  };

  map = new google.maps.Map(document.getElementById("map"), mapProp);

  google.maps.event.addListener(map, 'click', function(event) {
    placeMarker(event.latLng);
  });
}

function placeMarker(location) {
  if (!marker || !marker.setPosition) {
    marker = new google.maps.Marker({
      position: location,
      map: map,
    });

    cityCircle = new google.maps.Circle({
      strokeColor: "#FF0000",
      strokeOpacity: 0.8,
      strokeWeight: 2,
      fillColor: "#FF0000",
      fillOpacity: 0.35,
      map: map,
      center: location,
      radius: 100,
    });
  } else {
    marker.setPosition(location);
    cityCircle.setMap(null);
    cityCircle = new google.maps.Circle({
      strokeColor: "#FF0000",
      strokeOpacity: 0.8,
      strokeWeight: 2,
      fillColor: "#FF0000",
      fillOpacity: 0.35,
      map: map,
      center: location,
      radius: 100,
    });
  }

  
  document.getElementById('lat').value= location.lat()
  document.getElementById('lng').value= location.lng()
}