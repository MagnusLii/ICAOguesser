'use strict';

async function showdata() {
  fetch('http://127.0.0.1:3000/3')
  .then(function(response) {
    response.text().then(function(responseString) {
        return responseString
    });
  });
}

const jsonn =  showdata()

document.querySelector('p').innerText = jsonn

async function getkm(airportIndex) {
  const response = await fetch('http://127.0.0.1:3000/confirmation/' + airportIndex);
  const json = await response.json();
  console.log(response)
  console.log(json)
  document.querySelector('#distance-offset').innerHTML = json.distance // Currently returns float number representing KM diff between airports.
}

async function getNextGoalName() {
  const response = await fetch('http://127.0.0.1:3000/nextgoalname');
  const json = await response.json();
  document.querySelector('#current-goal').innerHTML = json.name
}