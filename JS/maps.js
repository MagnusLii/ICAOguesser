// Gmaps API doesn't work with 'use strict';
// DON'T USE HTTPS, causes errors due to no cert.

// Vars
// For modal manipulation.
const openModal = document.querySelector('#open-modal');
const closeModal = document.querySelector('.close-button');
const endOfRoundModal = document.querySelector('#end-of-round-modal');
const endOfGameModal = document.querySelector('#end-of-game-modal');

// Function that handles initialization of the map and creation of airport markers.
async function initMap() {

  // API call stuff.
  const response = await fetch('http://127.0.0.1:3000/fetchAirportData');
  const jsonData = await response.json();

  // To synch markers with ID's used in endpoint.
  let trackingnum = 0;

  map = new google.maps.Map(document.getElementById('map'), {
    mapId: 'eedb0a8713ca32aa',
    center: {lat: 48.85, lng: 2.35},
    zoom: 4,
    disableDefaultUI: true,
  });

  // This needs to be done cause Gmaps has no way to clear makers from secondary maps, Other than outright deleting all markers from all maps and recreating them...............
  // Thus the maps need to be recreated between rounds.
  nonCoreMaps = function nonCoreMaps() {
    endOfRoundMap = new google.maps.Map(document.getElementById('map2'), {
      mapId: 'eedb0a8713ca32aa',
      center: {lat: 48.85, lng: 2.35},
      zoom: 3,
      disableDefaultUI: true,
    });
    endOfGameMap = new google.maps.Map(document.getElementById('map3'), {
      mapId: 'eedb0a8713ca32aa',
      center: {lat: 48.85, lng: 2.35},
      zoom: 3,
    });
  };
  nonCoreMaps();

  // Another thing that needs to happen like this cause reasons.....
  zoomChange = function zoomChange(mapId, latlong, zoom) {
    mapId.setCenter(latlong);
    mapId.setZoom(zoom);
  };

  for (let i = 0; i < jsonData.length; i++) {

    // Creates markers on the map.
    let marker = new google.maps.Marker({
      position: {lat: jsonData[i].latitude, lng: jsonData[i].longitude},
      map,
    });

    // Creates an infowindow for the marker.
    const infowindow = new google.maps.InfoWindow({
      content: '<input type="button" value="select this airport" class="select-airport marker-button-' +
          trackingnum + '" onclick=" getkm(' + trackingnum + ');">',
      ariaLabel: 'Uluru',
    });

    trackingnum += 1; // Updates tracking num for next airport.

    marker.addListener('click', () => {
      infowindow.open(map, marker);
    });
  }

  await getNextGoalName(); // Fetches first goal for player.
};

// Function for getting KM/scorepoints for player after they select an airport and updating roundtracker in the endpoint.
async function getkm(airportIndex) {
  const response = await fetch(
      'http://127.0.0.1:3000/confirmation/' + airportIndex);
  const json = await response.json();

  // Adding player choice markers to end of round/game maps.
  let playerChoiceMarker = new google.maps.Marker({
    position: {lat: json.choicelat, lng: json.choicelon},
    icon: {
      url: '../ICONS/playerchoice.png',
      scaledSize: new google.maps.Size(40, 40),
    },
  });
  playerChoiceMarker.setMap(endOfRoundMap);

  // New markers need to be created cause Gmaps doesn't like the same marker being show on multiple maps ?!?"?!"?"!?#??#"!¤=)%?!#%(%=)#()=..-...........
  playerChoiceMarker = new google.maps.Marker({
    position: {lat: json.choicelat, lng: json.choicelon},
    icon: {
      url: '../ICONS/playerchoice.png',
      scaledSize: new google.maps.Size(40, 40),
    },
  });
  playerChoiceMarker.setMap(endOfGameMap);

  // Adding goal markers to end of round/game maps.
  let goalMarker = new google.maps.Marker({
    position: {lat: json.goallat, lng: json.goallon},
    icon: {
      url: '../ICONS/target.png',
      scaledSize: new google.maps.Size(40, 40),
    },
  });
  goalMarker.setMap(endOfRoundMap);

  goalMarker = new google.maps.Marker({
    position: {lat: json.goallat, lng: json.goallon},
    icon: {
      url: '../ICONS/target.png',
      scaledSize: new google.maps.Size(40, 40),
    },
  });
  goalMarker.setMap(endOfGameMap);

  // Centering end of round/game map in the middle of markers.
  // Zoom changle needs to happen before pan otherwise the pan gets overwritten.
  if (json.distance < 1000) {
    zoomChange(endOfRoundMap,
        {lat: json.middlepointlat, lng: json.middlepointlon}, 5);
    zoomChange(endOfGameMap,
        {lat: json.middlepointlat, lng: json.middlepointlon}, 5);
  } else if (json.distance < 2000) {
    zoomChange(endOfRoundMap,
        {lat: json.middlepointlat, lng: json.middlepointlon}, 4);
    zoomChange(endOfGameMap,
        {lat: json.middlepointlat, lng: json.middlepointlon}, 4);
  } else if (json.distance < 4000) {
    zoomChange(endOfRoundMap,
        {lat: json.middlepointlat, lng: json.middlepointlon}, 3);
    zoomChange(endOfGameMap,
        {lat: json.middlepointlat, lng: json.middlepointlon}, 3);
  } else if (json.distance > 6000) {
    zoomChange(endOfRoundMap,
        {lat: json.middlepointlat, lng: json.middlepointlon}, 2);
    zoomChange(endOfGameMap,
        {lat: json.middlepointlat, lng: json.middlepointlon}, 2);
  } else if (json.distance > 9000) {
    zoomChange(endOfRoundMap,
        {lat: json.middlepointlat, lng: json.middlepointlon}, 0);
    zoomChange(endOfGameMap,
        {lat: json.middlepointlat, lng: json.middlepointlon}, 0);
  }

  endOfRoundMap.panTo({lat: json.middlepointlat, lng: json.middlepointlon});

  // If the status code === 69.
  if (response.status == 69) {
    document.querySelector(
        '#end-of-game-distance-offset').innerHTML = 'You were ' +
        json.distance + 'KM from the goal.';// Currently returns float number representing KM diff between airports.
    document.querySelector(
        '#last-current-points').innerHTML = 'You get ' + json.points +
        ' points.';
    document.querySelector(
        '#final-score').innerHTML = 'Final score: ' + json.finalpoints +
        ' points.';
    endOfGameModal.showModal();
  }

  // Status code will be 69 only if all the goals have been completed.
  else {
    document.querySelector(
        '#round-end-distance-offset').innerHTML = 'You were ' +
        json.distance + 'KM from the goal.'; // Currently returns float number representing KM diff between airports.
    document.querySelector(
        '#current-points').innerHTML = 'You get ' + json.points + ' points.';
    document.querySelector(
        '#total-points').innerHTML = 'Total: ' + json.totalpoints +
        ' points.';
    endOfRoundModal.showModal();
    await fetch('http://127.0.0.1:3000/nextgoal');
    await getNextGoalName(); // Fetches next goal for player.
  }
}

// Provides goals/hints for player.
async function getNextGoalName() {
  const response = await fetch('http://127.0.0.1:3000/nextgoalname');
  const json = await response.json();
  document.querySelector('#current-goal').innerHTML ='Find ' + json.name;
}

// Defining close modal func for ALL modal buttons.
closeModal.addEventListener('click', () => {
  nonCoreMaps();
  endOfRoundModal.close();
});


