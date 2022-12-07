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