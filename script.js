document.addEventListener("DOMContentLoaded", () => {

    const headers = document.getElementsByClassName("main-header");
    window.addEventListener("scroll", () => {
        Array.from(headers).forEach(header => {
            if (window.scrollY > 0) {
                header.classList.add("scrolled");
            } else {
                header.classList.remove("scrolled");
            }
        });
    });

    // window.addEventListener("scroll", () => {
    //     const hero = document.querySelector(".hero");
    //     const background = document.querySelector(".background");
    //     const textContainer = document.querySelector(".text-container");
    
    //     const bgRect = background.getBoundingClientRect();
    //     const textRect = textContainer.getBoundingClientRect();

    //     const scrollY = window.scrollY;
    //     background.style.top = `-${scrollY}px`;

    //     console.log(bgRect.bottom, textRect.bottom)
    
    //     if (bgRect.bottom <= 50 && textRect.bottom >= 0) {
    //         // Stick background when it reaches 50px from the top
    //         console.log(background.offsetHeight)
    //         const offset = background.offsetHeight - 150
    //         background.style.top = `-${offset}px`;
    //         console.log("Stick background")

    //     } 
    // });
    
    
});

