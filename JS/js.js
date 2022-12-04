'use strict';

// Selects buttons used for opening/closing modal.
const modal = document.querySelector('#modal');
const openModal = document.querySelector('.open-button');
const closeModal = document.querySelector('.close-button');

// Adds event listeners for showing/closing modal.
openModal.addEventListener('click', () => {
  modal.showModal();
});
closeModal.addEventListener('click', () => {
  modal.close();
});