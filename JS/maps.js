function initMap() {
  map = new google.maps.Map(document.getElementById('map'), {
    mapId: 'eedb0a8713ca32aa',
    center: {lat: 48.85, lng: 2.35},
    zoom: 4,
  });
  // Creates markers on the map.
  const marker = new google.maps.Marker({
    position: {lat: 60.3172, lng: 24.963301},
    map,
    title: 'Hello World!',

  });
  // Creates an infowindow for the marker.
  const infowindow = new google.maps.InfoWindow({
    content: 'HELSINKI-VANTAAN LENTOKENTTÄ',
    ariaLabel: 'Uluru',
  });
  marker.addListener('click', () => {
    infowindow.open(map, marker);
  });
}