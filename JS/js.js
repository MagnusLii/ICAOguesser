'use strict';

// Selects buttons used for opening/closing modal.
const spModal = document.querySelector('#modal');
const openModal = document.querySelector('.open-button');
const closeModal = document.querySelector('.close-button');

// Adds event listeners for showing/closing modal(s).
// Mainmenu SP modal.
openModal.addEventListener('click', () => {
  spModal.showModal();
});
closeModal.addEventListener('click', () => {
  spModal.close();
});