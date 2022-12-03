'use strict';

document.getElementById('SP-button').
    addEventListener('click',
        async function start() {await fetch('localhost:3000/1');});