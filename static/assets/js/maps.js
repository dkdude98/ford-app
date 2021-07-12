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
  infowindow = new google.maps.InfoWindow({
    content: "<button type='button' data-bs-toggle='modal' class='btn btn-outline-tertiary' data-bs-target='#modal-myq'>Save Location</button>"
  });
  infowindow.open(map, marker);
}