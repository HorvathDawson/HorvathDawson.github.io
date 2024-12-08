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


});
  