console.log('hello');
/* ************************** Background Animation ************************** */

window.addEventListener('DOMContentLoaded', (event) => {
    let bg = document.querySelector(".bg")
    const glassContainer = document.querySelector('.glass');

    const containerWidth = window.innerWidth;

    function createGlassElement() {
        const glassElement = document.createElement('li');
        const randomSize = Math.floor(Math.random() * (15 - 10 + 1)) + 10; // Random size between 10vh and 15vh
        const randomLeft = Math.floor(Math.random() * containerWidth);
        const delay = Math.random() * 5; // Random delay between 0 and 5 seconds

        glassElement.style.width = randomSize + 'vh';
        glassElement.style.height = randomSize + 'vh';
        glassElement.style.background = 'rgba(255, 255, 255, 0.1)';
        glassElement.style.border = '1px solid rgba(255, 255, 255, 0.18)';
        glassElement.style.animation = 'rise 5s linear infinite, spin 5s linear infinite';
        glassElement.style.position = 'absolute';
        glassElement.style.bottom = '-30px'; // Adjusted initial position below the viewport
        glassElement.style.left = randomLeft + 'px';
        glassElement.style.transition = 'all 5s linear';
        glassElement.style.animationDelay = `${delay}s`;
        glassContainer.appendChild(glassElement);

        // Trigger reflow to enable the animation
        glassElement.style.animationPlayState = 'running';
    }

    function createGlassElements() {
        const totalElements = 10; // Total number of elements
        for (let i = 0; i < totalElements; i++) {
            createGlassElement();
        }
    }

    createGlassElements();
});
/* ************************** Pop Up Form ************************** */
const wrapper = document.querySelector('.login-form-wrapper');
const loginlink = document.querySelector('.login-link');
const registerlink = document.querySelector('.register-link');
const btnPopup = document.querySelector('.btnLogin-popup');
const btnClose = document.querySelector('.icon-close');

registerlink.addEventListener('click', () => {
    wrapper.classList.add('active')
});
loginlink.addEventListener('click', () => {
    wrapper.classList.remove('active')
});
btnPopup.addEventListener('click', () => {
    wrapper.classList.add('active-popup')
});
btnClose.addEventListener('click', () => {
    wrapper.classList.remove('active-popup')
})

/* ************************** TYPING ANIMATION EFFECT************************** */

const dynamicText = document.querySelector('.hero-content h1 span');
const words = ["سی شارپ", "پایتون", "جاوا", "جنگو"];

// Variables to track the position and deletion status of the word
let wordIndex = 0;
let charIndex = 0;
let isDeleting = false;

const typeEffect = () => {
    const currentWord = words[wordIndex];
    const currentChar = currentWord.substring(0, charIndex);
    dynamicText.textContent = currentChar;
    dynamicText.classList.add("stop-blinking");

    if (!isDeleting && charIndex < currentWord.length) {
        // If condition is true, type the next character
        charIndex++;
        setTimeout(typeEffect, 200);
    } else if (isDeleting && charIndex > 0) {
        // If condition is true, remove the previous character
        charIndex--;
        setTimeout(typeEffect, 100);
    } else {
        // If word is deleted then switch to the next word
        isDeleting = !isDeleting;
        dynamicText.classList.remove("stop-blinking");
        wordIndex = !isDeleting ? (wordIndex + 1) % words.length : wordIndex;
        setTimeout(typeEffect, 1200);
    }
}

typeEffect();

