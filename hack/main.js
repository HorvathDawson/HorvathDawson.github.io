import * as THREE from 'three';
import { gsap }from 'gsap';


const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera( 75, window.innerWidth / window.innerHeight, 0.1, 1000 );

const renderer = new THREE.WebGLRenderer();
renderer.setSize( window.innerWidth, window.innerHeight );
renderer.setAnimationLoop( animate );
document.body.appendChild( renderer.domElement );


const geometry = new THREE.BoxGeometry( 1, 1, 1 );
const material = new THREE.MeshBasicMaterial( { color: 0x00ff00 } );



const cube = new THREE.Mesh( geometry, material );
scene.add( cube );

camera.position.z = 1.5;

// Rotation tracking
let scrollDelta = 0; // Tracks cumulative scroll movement
const snapThreshold = 100; // Pixels of scroll needed to trigger a snap
const snapRotation = Math.PI / 2; // Rotation per "page"

// Handle scroll
let isAnimating = false;

window.addEventListener('wheel', (event) => {
    event.preventDefault();

    if (isAnimating) return; // Prevent event from being called again while animating

    // Accumulate scroll delta
    scrollDelta += event.deltaY;

    // Determine snap points
    if (Math.abs(scrollDelta) >= snapThreshold) {
        const direction = Math.sign(scrollDelta); // 1 for down, -1 for up
        scrollDelta = 0; // Reset delta after snapping

        // Target rotation
        const targetRotationX = cube.rotation.y + direction * snapRotation;

        // Animate the rotation
        isAnimating = true;
        gsap.to(cube.rotation, {
            y: targetRotationX,
            duration: 0.75,
            ease: 'power2.out',
            onComplete: () => {
                isAnimating = false; // Reset flag after animation completes
            }
        });
    }
}, { passive: false });

// Animation loop
function animate(first_call = false) {
    if (isAnimating || first_call) {
        requestAnimationFrame(animate);
        renderer.render(scene, camera);
    }
}
animate(true);

// const raycaster = new THREE.Raycaster();
// const mouse = new THREE.Vector2();

// window.addEventListener('click', (event) => {
//     // Normalize mouse position
//     mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
//     mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;

//     // Cast a ray
//     raycaster.setFromCamera(mouse, camera);
//     const intersects = raycaster.intersectObject(cube);

//     if (intersects.length > 0) {
//         console.log('Face clicked:', intersects[0].faceIndex);
//     }
// });




// ==============================


// const loader = new THREE.TextureLoader();
// const texture = loader.load('public/OpenSim2RealCover.png');
// texture.minFilter = THREE.LinearFilter;
// // texture.magFilter = THREE.LinearFilter;
// texture.anisotropy = renderer.capabilities.getMaxAnisotropy(); // Improve sharpness
// const material = new THREE.MeshBasicMaterial({ map: texture });

// const buttonMaterials = [
//     // new THREE.MeshBasicMaterial({ map: loader.load('public/OpenSim2RealCover.png') }),  // Front
//     createButtonMaterialWithText('front'),   // front
//     createButtonMaterialWithText('Back'),   // Back
//     createButtonMaterialWithText('Top'),    // Top
//     createButtonMaterialWithText('Bottom'), // Bottom
//     // createButtonMaterialWithText('Left'),   // Left
//     material,
//     createButtonMaterialWithText('Right')   // Right
// ];
// function createButtonMaterialWithText(text) {
//     const canvas = document.createElement('canvas');
//     const context = canvas.getContext('2d');
//     canvas.width = 256;
//     canvas.height = 256;

//     // Draw content on the canvas
//     context.fillStyle = 'blue';
//     context.fillRect(0, 0, canvas.width, canvas.height);
//     context.fillStyle = 'white';
//     context.font = '20px Arial';
//     context.fillText(text, 80, 130);

//     const canvasTexture = new THREE.CanvasTexture(canvas);
//     return new THREE.MeshBasicMaterial({ map: canvasTexture });
// }