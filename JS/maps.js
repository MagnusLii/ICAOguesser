// Gmaps API doesn't work with 'use strict';
// DON'T USE HTTPS, causes errors due to no cert.

// Vars
// For modal manipulation.
const closeModal = document.querySelector('.close-button')
const endOfRoundModal = document.querySelector('#end-of-round-modal');
const scoreboardModal = document.querySelector('#scoreboard-modal');


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
  const json = await response.json();
  document.querySelector('#distance-offset').innerHTML = 'You were ' +
      json.distance + 'KM from the goal.'; // Currently returns float number representing KM diff between airports.
  endOfRoundModal.showModal();
  await fetch('http://127.0.0.1:3000/nextgoal');
  await getNextGoalName(); // Fetches next goal for player.
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
// Ingame scoreboard modal. NOT IMPLEMENTED!
openModal.addEventListener('click', () => {
  scoreboardModal.showModal();
});