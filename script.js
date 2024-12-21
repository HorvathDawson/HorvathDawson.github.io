document.addEventListener('DOMContentLoaded', () => {
  const items = document.querySelectorAll('.project-portfolio__item');

  // Event delegation for mouse events
  document.body.addEventListener('mouseenter', (e) => handleHover(e, 'mouseenter'), true);
  document.body.addEventListener('mouseleave', (e) => handleHover(e, 'mouseleave'), true);

  function handleHover(event, type) {
    const item = event.target.closest('.project-portfolio__item');
    if (!item) return;

    const canvases = item.querySelectorAll('canvas');
    if (canvases) {
      canvases.forEach((canvas) => {
        canvas.dataset.hover = type === 'mouseenter' ? 'true' : 'false';
      });
    }
    const backgrounds = item.querySelectorAll('.background');
    const foregrounds = item.querySelectorAll('.foreground');
    const splashes = item.querySelectorAll('.splash');

    if (type === 'mouseenter') {
      toggleOpacity(backgrounds, '0');
      toggleOpacity(foregrounds, '1');
      toggleOpacity(splashes, '1');
    } else if (type === 'mouseleave') {
      toggleOpacity(backgrounds, '1');
      toggleOpacity(foregrounds, '0');
      toggleOpacity(splashes, '0');
    }

  }

  function toggleOpacity(elements, value) {
    elements.forEach((el) => (el.style.opacity = value));
  }

  function setupCanvas() {
    const canvas1 = document.querySelector('#opensim2real-canvas1');
    const canvas2 = document.querySelector('#opensim2real-canvas2');

    // Use gifler to handle animations
    let gif1, gif2;
    const gif1Url = 'public/assets/projects/opensim2real/leg-spin-body-small.gif';
    const gif2Url = 'public/assets/projects/opensim2real/leg-spin-edge-small.gif';

    const loadGif = (url) => {
      return new Promise((resolve) => {
      const img = new Image();
      img.src = url;
      img.onload = () => resolve(url);
      });
    };

    Promise.all([loadGif(gif1Url), loadGif(gif2Url)]).then(([loadedGif1Url, loadedGif2Url]) => {
      gif1 = gifler(loadedGif1Url);
      gif2 = gifler(loadedGif2Url);

      let anim1, anim2;
      gif1.get((animation) => {
      anim1 = animation;
      anim1.animateInCanvas(canvas1, (frameCtx) => {
        frameCtx.drawImage(animation.image, 0, 0, canvas1.width, canvas1.height);
      });
      });

      gif2.get((animation) => {
      anim2 = animation;
      anim2.animateInCanvas(canvas2, (frameCtx) => {
        frameCtx.drawImage(animation.image, 0, 0, canvas2.width, canvas2.height);
      });
      });
    });
  }

  setupCanvas();

});

const parallaxContainer = document.querySelector('.parallax');
let scrollAnimationFrame;

parallaxContainer.addEventListener('scroll', () => {
  if (scrollAnimationFrame) return;

  scrollAnimationFrame = requestAnimationFrame(() => {
    const windowHeight = window.innerHeight;
    const windowCenterY = windowHeight / 2;
    const maxDistance = windowHeight / 2;

    // Cached item rotations
    const cachedItems = [
      { selector: '.project-portfolio__item-image.openSim2Real', axis: 'Z', min: -35, max: 35 },
      // { selector: '.project-portfolio__item-image.fume-extractor', axis: 'Y', min: -35, max: 20.5 },
      { selector: '.project-portfolio__item-image.self-driving-car .laptop-screen-div', axis: 'X', min: -60, max: 60 },
    ];

    cachedItems.forEach(({ selector, axis, min, max }) => {
      document.querySelectorAll(selector).forEach((item) => {
        const rect = item.getBoundingClientRect();
        const itemCenterY = rect.top + rect.height / 2;
        const distanceToCenter = Math.min(0, 1.5 * windowCenterY - itemCenterY);
        let rotation = axis === 'Z' ? Math.max(min, min * (distanceToCenter / maxDistance)) : Math.min(max, min * (distanceToCenter / maxDistance));
        if (axis === 'X') rotation = -rotation;

        item.style.transform = `rotate${axis}(${rotation}deg)`;

      });
    });

    // Apply dynamic part translations
    applyDynamicPartTranslation(windowCenterY);

    // Apply car movement animation
    applyCarTranslation(windowCenterY);

    scrollAnimationFrame = null;
  });


});

function applyDynamicPartTranslation(windowCenterY) {
  const baseDistance = 30; // Base distance in pixels
  const angleInDegrees = 60; // Angle above horizontal
  const angleInRadians = (angleInDegrees * Math.PI) / 180; // Convert to radians

  document.querySelectorAll('.project-portfolio__item').forEach((item) => {
    const rect = item.getBoundingClientRect();
    const itemCenterY = rect.top + rect.height / 2;

    // Calculate closeness factor
    const distanceToCenter = Math.abs(itemCenterY - windowCenterY);
    const factor = Math.max(0, 1 - distanceToCenter / windowCenterY); // Factor reduces as item moves away

    // Translate each part__x dynamically
    item.querySelectorAll('[class*="part__"]').forEach((part) => {
      const match = part.className.match(/part__(\d+)/); // Extract part number
      if (!match) return;

      const partNumber = parseInt(match[1], 10);
      const distance = baseDistance * partNumber * factor; // Scale translation

      const translateX = distance * Math.cos(angleInRadians);
      const translateY = -distance * Math.sin(angleInRadians);

      part.style.transform = `translate(${translateX}px, ${translateY}px)`;
    });
  });
}

function applyCarTranslation(windowCenterY) {
  const baseDistance = -75; // Starting position
  const angleInDegrees = 30; // Angle of movement
  const angleInRadians = (angleInDegrees * Math.PI) / 180; // Convert to radians

  document.querySelectorAll('.project-portfolio__item-image.a40austin').forEach((car) => {
    const rect = car.getBoundingClientRect();
    const itemCenterY = rect.top + rect.height / 2;

    // Calculate closeness factor
    const distanceToCenter = Math.max(0, itemCenterY - windowCenterY);
    const factor = Math.max(0, distanceToCenter / windowCenterY); // Factor reduces as item moves away

    // Calculate translation along the specified axis
    const translateX = baseDistance * factor * Math.cos(angleInRadians);
    const translateY = baseDistance * factor * Math.sin(angleInRadians);

    car.style.transform = `translate(${translateX}px, ${translateY}px)`;
  });
}

// Mouse tracking for shuffle effect
let mouseX, mouseY;
let mouseAnimationFrame;

document.addEventListener('mousemove', (event) => {
  mouseX = event.clientX;
  mouseY = event.clientY;

  if (mouseAnimationFrame) return;

  mouseAnimationFrame = requestAnimationFrame(() => {
    const centerX = window.innerWidth / 2;
    const centerY = window.innerHeight / 2;
    const offsetX = (mouseX - centerX) * 0.002;
    const offsetY = (mouseY - centerY) * 0.002;
    const distance = Math.sqrt(offsetX * offsetX + offsetY * offsetY);
    const zOffset = distance * 100;

    document.querySelectorAll('.mouse-tracking-shuffle').forEach((element) => {
      element.style.transform = `translate3d(${offsetX}%, ${offsetY}%, ${zOffset}px)`;
    });

    mouseAnimationFrame = null;
  });
});
