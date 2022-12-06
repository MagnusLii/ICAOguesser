function initMap() {
  map = new google.maps.Map(document.getElementById('map'), {
    mapId: 'eedb0a8713ca32aa',
    center: {lat: 48.85, lng: 2.35},
    zoom: 4,
  });
  const markers = [{"name": "Nassen airport", "latitude": 10.123, "longitude": 124.42},
      {"name": "Jasperin airport","latitude": 50,"longitude": 30,},
      {"name": "Miston Airport","latitude": 12.341,"longitude": 1.1},
      {"name": "Danielin Airport","latitude": -8,"longitude": -56.3}]
  for (let i = 0; i < markers.length; i++) {
    let marker = new google.maps.Marker({
    position: {lat: markers[i].latitude, lng: markers[i].longitude},
    map,
    title: 'Olet täällä Nasse!',
  });
  }
  // Creates markers on the map.
  let marker = new google.maps.Marker({
    position: {lat: 60.3172, lng: 24.963301},
    map,
    title: 'Olet täällä Nasse!',
  });

  // Creates an infowindow for the marker.
  let trackingnum = 0
  const infowindow = new google.maps.InfoWindow({
    content: '<a class="marker-button-' + trackingnum + '"><button>Lock in this airport</button></a>',
    ariaLabel: 'Uluru',
  });
  marker.addListener('click', () => {
    infowindow.open(map, marker);
  });
}