// Gmaps API doesn't work with 'use strict';

async function initMap() {
  const response = await fetch('http://127.0.0.1:3000/fetchAirportData');
  const jsonData = await response.json();
  let trackingnum = 0
  map = new google.maps.Map(document.getElementById('map'), {
    mapId: 'eedb0a8713ca32aa',
    center: {lat: 48.85, lng: 2.35},
    zoom: 4,
  });


  for (let i = 0; i < jsonData.length; i++) {

    // Creates markers on the map.
  let marker = new google.maps.Marker({
    position: {lat: jsonData[i].latitude, lng: jsonData[i].longitude},
    map,
    title: 'Airport',
  });

  // Creates an infowindow for the marker.
  const infowindow = new google.maps.InfoWindow({
    content: '<a class="marker-button-' + trackingnum + '"><button>Lock in this airport</button></a>',
    ariaLabel: 'Uluru',
  });

  trackingnum += 1; // Updates tracking num for next airport.

  marker.addListener('click', () => {
    infowindow.open(map, marker);
  });

  }

}