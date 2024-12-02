document.addEventListener("DOMContentLoaded", () => {
    const header = document.getElementById("main-header");

    window.addEventListener("scroll", () => {
        if (window.scrollY > 0) {
            header.classList.add("scrolled");
        } else {
            header.classList.remove("scrolled");
        }
    });
    // const ticker = document.querySelector('.ticker');
    // const phrases = [
    //   'Engineering Physicist',
    //   'Mechatronic Engineer',
    //   'Problem Solver',
    //   'Innovator',
    //   'Hands-On Builder',
    //   'Robotics Enthusiast',
    //   'Creative Thinker',
    //   'Data Explorer',
    //   'Outdoor Adventurer',
    //   'Curiosity-Driven'
    // ];
    
    // phrases.forEach(phrase => {
    //   const span = document.createElement('span');
    //   span.textContent = phrase;
    //   ticker.appendChild(span);
    // });

    
});

