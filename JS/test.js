'use strict';


async function showdata() {
  const response = await fetch('http://127.0.0.1:3000/3');
  const jsonData = await response.json();
  console.log(jsonData)
}

showdata()