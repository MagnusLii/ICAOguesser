const closeModal = document.querySelector('.close-button');
const endOfRoundModal = document.querySelector('#end-of-round-modal');
const endOfGameModal = document.querySelector('#end-of-game-modal');

// Function that handles initialization of the map and creation of airport markers.
async function initMap() {
  const response = await fetch('http://127.0.0.1:3000/fetchAirportData');
  const jsonData = await response.json();
  let trackingnum = 0;
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
      title: jsonData[i].name,
    });

    // Creates an infowindow for the marker.
    const infowindow = new google.maps.InfoWindow({
      content: '<input type="button" value="select this airport" class="marker-button-' +
          trackingnum + '" onclick="getkm(' + trackingnum + ')">',
      ariaLabel: 'Uluru',
    });

    trackingnum += 1; // Updates tracking num for next airport.

    marker.addListener('click', () => {
      infowindow.open(map, marker);
    });
  }
  await getNextGoalName(); // Fetches first goal for player.
}

// Function for getting KM/scorepoints for player after they select an airport and updating roundtracker in the endpoint.
async function getkm(airportIndex) {
  const response = await fetch(
      'http://127.0.0.1:3000/confirmation/' + airportIndex);

  // If the status code === 69.
  if (response.status == 69) {
    const json = await response.json();
    document.querySelector(
        '#end-of-game-distance-offset').innerHTML = 'You were ' +
        json.distance + 'KM from the goal.'; // Currently returns float number representing KM diff between airports.
    endOfGameModal.showModal();
  }

  // Status code will be 69 only if all the goals have been completed.
  else {
    const json = await response.json();
    document.querySelector(
        '#round-end-distance-offset').innerHTML = 'You were ' +
        json.distance + 'KM from the goal.'; // Currently returns float number representing KM diff between airports.
    endOfRoundModal.showModal();
    await fetch('http://127.0.0.1:3000/nextgoal');
    await getNextGoalName(); // Fetches next goal for player.
  }
}

// Provides goals/hints for player.
async function getNextGoalName() {
  const response = await fetch('http://127.0.0.1:3000/nextgoalname');
  const json = await response.json();
  document.querySelector('#current-goal').innerHTML = json.name;
}

// Defining close modal func for ALL modal buttons.
closeModal.addEventListener('click', () => {
  endOfRoundModal.close();
});

const osmMap = document.querySelector('#map2');
const testo = document.createElement('iframe');
testo.id = 'map2';
testo.src = 'http://www.openstreetmap.org/export/embed.html?bbox=-122.480427%2C37.745703%2C-122.472427%2C37.753703&amp;layer=mapnik&amp;marker=37.749703%2C-122.476427';
testo.style = 'border: 1px solid black';
osmMap.append(testo);

map2 = new OpenLayers.Map('mapdiv');
map2.addLayer(new OpenLayers.Layer.OSM());

var lonLat = new OpenLayers.LonLat(-0.1279688, 51.5077286).transform(
    new OpenLayers.Projection('EPSG:4326'), // transform from WGS 1984
    map2.getProjectionObject(), // to Spherical Mercator Projection
);

var zoom = 16;

var markers = new OpenLayers.Layer.Markers('Markers');
map2.addLayer(markers);

markers.addMarker(new OpenLayers.Marker(lonLat));

map2.setCenter(lonLat, zoom);

//osmMap.append(<iframe id="osm" src="http://www.openstreetmap.org/export/embed.html?bbox=-122.480427%2C37.745703%2C-122.472427%2C37.753703&amp;layer=mapnik&amp;marker=37.749703%2C-122.476427" style="border: 1px solid black"></iframe>)