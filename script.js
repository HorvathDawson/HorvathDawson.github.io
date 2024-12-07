document.addEventListener("DOMContentLoaded", () => {
    const header = document.getElementById("main-header");

    window.addEventListener("scroll", () => {
        if (window.scrollY > 0) {
            header.classList.add("scrolled");
        } else {
            header.classList.remove("scrolled");
        }

        const heroScrollOver = document.querySelector(".hero .scroll-over");
        if (heroScrollOver.getBoundingClientRect().top < header.offsetHeight) {
            header.classList.add("white-section");
        } else {
            header.classList.remove("white-section");
        }
    });



    
});

