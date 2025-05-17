// Typing Effect
const text = "I Love You, Akriti ❤️";
let index = 0;

function typeEffect() {
    if (index < text.length) {
        document.getElementById("love-text").innerHTML += text.charAt(index);
        index++;
        setTimeout(typeEffect, 100);
    }
}

window.onload = function () {
    typeEffect();
    generateHearts();
};

// Floating Hearts Animation
function generateHearts() {
    const heartsContainer = document.querySelector('.hearts');

    setInterval(() => {
        const heart = document.createElement('div');
        heart.classList.add('heart');
        heart.style.left = `${Math.random() * 100}vw`;
        heart.style.animationDuration = `${2 + Math.random() * 3}s`;
        heartsContainer.appendChild(heart);

        setTimeout(() => {
            heart.remove();
        }, 4000);
    }, 500);
}
