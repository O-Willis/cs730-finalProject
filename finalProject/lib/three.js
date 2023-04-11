// Initialize Three.js
var scene = new THREE.Scene();
var camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
var renderer = new THREE.WebGLRenderer({canvas: document.getElementById("canvas")});
renderer.setSize(window.innerWidth, window.innerHeight);

// Create the circle geometry and material
var circleGeometry = new THREE.CircleGeometry(0.3, 32);
var circleMaterial = new THREE.MeshBasicMaterial({color: 0xffffff});

// Create the circles and position them in a diamond shape
var circles = [];
var radius = 5;
var centerX = 0;
var centerY = 0;
for (var i = 0; i < 35; i++) {
    var circle = new THREE.Mesh(circleGeometry, circleMaterial);
    var angle = i * Math.PI / 18;
    var x = centerX + radius * Math.cos(angle);
    var y = centerY + radius * Math.sin(angle) * 2;
    circle.position.set(x, 0, y);
    circles.push(circle);
    scene.add(circle);
}

// Add interactivity to the circles
var raycaster = new THREE.Raycaster();
var mouse = new THREE.Vector2();
renderer.domElement.addEventListener('mousedown', onMouseDown, false);
function onMouseDown(event) {
    // calculate mouse position in normalized device coordinates
    // (-1 to +1) for both components
    mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
    mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;

    // update the picking ray with the camera and mouse position
    raycaster.setFromCamera(mouse, camera);

    // calculate objects intersecting the picking ray
    var intersects = raycaster.intersectObjects(circles);

    if (intersects.length > 0) {
        // Do something when a circle is clicked
        var clickedCircle = intersects[0].object;
        console.log("Circle clicked: ", clickedCircle.position);
    }
}

// Set camera position
camera.position.set(0, 10, 0);
camera.lookAt(scene.position);

// Render the scene
function render() {
    requestAnimationFrame(render);
    renderer.render(scene, camera);
}
render();