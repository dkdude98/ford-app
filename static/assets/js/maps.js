var map;
var marker;
var infowindow;

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
  } else {
    marker.setPosition(location);
  }
  if (!!infowindow && !!infowindow.close) {
    infowindow.close();
  }

  document.getElementById('lat').value= location.lat()
  document.getElementById('lng').value= location.lng()
  console.log(location.lng() + " " + location.lat())
}