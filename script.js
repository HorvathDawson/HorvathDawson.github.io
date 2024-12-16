// JavaScript for Parallax Effect
document.addEventListener('DOMContentLoaded', () => {


  document.addEventListener('scroll', () => {
    const scrollTop = window.scrollY; // Get current scroll position
    console.log(scrollTop);
    // const layers = document.querySelectorAll('.parallax__layer');
    // layers.forEach((layer, index) => {
    //   console.log(layer, index);
    //   const speed = (index + 1) * 0.3; // Define layer-specific speed
    //   const yOffset = scrollTop * speed;
    //   layer.style.transform = `translateY(${yOffset}px)`;
    // });
  });

  const items = document.querySelectorAll('.project-portfolio__item');

  items.forEach((item) => {
    item.addEventListener('mouseenter', () => {
      const backgrounds = item.querySelectorAll('.background');
      const foregrounds = item.querySelectorAll('.foreground');
      const splashes = item.querySelectorAll('.splash');

      backgrounds.forEach(background => {
      background.style.willChange = 'opacity';
      background.style.transition = 'opacity 0.5s ease-in-out';
      background.style.opacity = '0';
      });

      foregrounds.forEach(foreground => {
      foreground.style.willChange = 'opacity';
      foreground.style.transition = 'opacity 0.5s ease-in-out, transform 0.5s ease-in-out';
      foreground.style.opacity = '1';
      });

      splashes.forEach(splash => {
      splash.style.willChange = 'opacity';
      splash.style.transition = 'opacity 0.5s ease-in-out';
      splash.style.opacity = '1';
      });
    });

    item.addEventListener('mouseleave', () => {
      const backgrounds = item.querySelectorAll('.background');
      const foregrounds = item.querySelectorAll('.foreground');
      const splashes = item.querySelectorAll('.splash');

      backgrounds.forEach(background => {
      background.style.willChange = 'opacity';
      background.style.transition = 'opacity 0.5s ease-in-out';
      background.style.opacity = '1';
      });

      foregrounds.forEach(foreground => {
      foreground.style.willChange = 'opacity';
      foreground.style.transition = 'opacity 0.5s ease-in-out, transform 0.5s ease-in-out';
      foreground.style.opacity = '0';
      });

      splashes.forEach(splash => {
      splash.style.willChange = 'opacity';
      splash.style.transition = 'opacity 0.5s ease-in-out';
      splash.style.opacity = '0';
      });
    });


  });

});


const updateTransform = (event) => {
  const scrollTop = window.scrollY;
  const windowHeight = window.innerHeight;
  const centerX = window.innerWidth / 2;
  const centerY = window.innerHeight / 2;

  const openSim2RealItems = document.querySelectorAll('.project-portfolio__item-image.openSim2Real');
  openSim2RealItems.forEach((item) => {
    const itemRect = item.getBoundingClientRect();
    const itemCenterY = itemRect.top + itemRect.height / 2;
    const windowCenterY = windowHeight / 2;
    const distanceToCenter = Math.min(0, 1.5 * windowCenterY - itemCenterY);
    const maxDistance = windowHeight / 2;
    const rotation = Math.max(-35, -35 * (distanceToCenter / maxDistance));
    item.style.transform = `rotateZ(${rotation}deg)`;
  });

  const selfDrivingCars = document.querySelectorAll('.project-portfolio__item-image.self-driving-car .laptop-screen-div');
  selfDrivingCars.forEach((item) => {
    const itemRect = item.getBoundingClientRect();
    const itemCenterY = itemRect.top + itemRect.height / 2;
    const windowCenterY = windowHeight / 2;
    const distanceToCenter = Math.min(0, 1.5 * windowCenterY - itemCenterY);
    const maxDistance = windowHeight / 2;
    const rotation = Math.max(-90, -90 * (distanceToCenter / maxDistance));
    item.style.transform = `rotateX(${-rotation}deg)`;
    if (rotation === 0) {
      item.style.transformStyle = 'flat';
    }
  });

  const elements = document.querySelectorAll('.mouse-tracking-shuffle');
  elements.forEach((element) => {
    const offsetX = (mouseX - centerX) * 0.002;
    const offsetY = (mouseY - centerY) * 0.002;
    const distance = Math.sqrt(offsetX * offsetX + offsetY * offsetY);
    const zOffset = distance * 100;
    element.style.willChange = 'transform';
    const currentTransform = element.style.transform;
    const newTransform = `translate3d(${offsetX}%, ${offsetY}%, ${zOffset}px)`;
    const updatedTransform = currentTransform.replace(/translate3d\([^)]+\)/, newTransform);
    element.style.transform = updatedTransform.includes('translate3d') ? updatedTransform : `${newTransform} ${currentTransform}`;
    // element.style.transformStyle = 'preserve-3d';
  });
};

const parallaxContainer = document.querySelector('.parallax');

parallaxContainer.addEventListener('scroll', () => {
  document.dispatchEvent(new CustomEvent('updateTransform'));
});

let mouseX;
let mouseY;

document.addEventListener('mousemove', (event) => {
  const centerX = window.innerWidth / 2;
  const centerY = window.innerHeight / 2;
  mouseX = event.clientX;
  mouseY = event.clientY;

  document.dispatchEvent(new CustomEvent('updateTransform'));
});

document.addEventListener('updateTransform', updateTransform);

