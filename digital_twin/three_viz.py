import streamlit.components.v1 as components

def three_js_turbine(wind_speed, power_kw, state):
    """
    High-end Three.js 3D turbine visualization with professional aesthetics.
    """
    rotation_speed = (wind_speed * 0.05) if state == "RUNNING" else 0
    
    html_code = f"""
    <div id="container" style="width: 100%; height: 500px; background: radial-gradient(circle, #1e293b 0%, #0f172a 100%); border-radius: 15px; overflow: hidden; box-shadow: 0 10px 30px rgba(0,0,0,0.5);"></div>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script>
        const container = document.getElementById('container');
        const scene = new THREE.Scene();
        
        const camera = new THREE.PerspectiveCamera(60, container.clientWidth / container.clientHeight, 0.1, 1000);
        camera.position.set(60, 40, 80);
        camera.lookAt(0, 25, 0);

        const renderer = new THREE.WebGLRenderer({{ antialias: true, alpha: true }});
        renderer.setSize(container.clientWidth, container.clientHeight);
        renderer.setPixelRatio(window.devicePixelRatio);
        container.appendChild(renderer.domElement);

        // Lights
        const ambientLight = new THREE.AmbientLight(0xffffff, 0.4);
        scene.add(ambientLight);

        const spotLight = new THREE.SpotLight(0x00d4ff, 1);
        spotLight.position.set(100, 100, 100);
        scene.add(spotLight);

        const pointLight = new THREE.PointLight(0xffffff, 0.8);
        pointLight.position.set(-50, 50, 50);
        scene.add(pointLight);

        // Materials
        const metalMat = new THREE.MeshStandardMaterial({{ color: 0xe2e8f0, roughness: 0.3, metalness: 0.8 }});
        const bladeMat = new THREE.MeshStandardMaterial({{ color: 0xffffff, roughness: 0.5, metalness: 0.2 }});
        const groundMat = new THREE.MeshPhongMaterial({{ color: 0x1e293b, emissive: 0x00d4ff, emissiveIntensity: 0.1, transparent: true, opacity: 0.8 }});

        // Tower (Tapered)
        const towerGeo = new THREE.CylinderGeometry(1.2, 2.5, 60, 32);
        const tower = new THREE.Mesh(towerGeo, metalMat);
        tower.position.y = 30;
        scene.add(tower);

        // Nacelle (The "Box" on top)
        const nacelleGeo = new THREE.BoxGeometry(4, 4, 8);
        const nacelle = new THREE.Mesh(nacelleGeo, metalMat);
        nacelle.position.set(0, 60, -1);
        scene.add(nacelle);

        // Hub
        const hubGeo = new THREE.SphereGeometry(2.5, 32, 32);
        const hub = new THREE.Mesh(hubGeo, metalMat);
        hub.position.set(0, 60, 3);
        scene.add(hub);

        // Blades
        const bladeGroup = new THREE.Group();
        bladeGroup.position.set(0, 60, 4);
        scene.add(bladeGroup);

        for (let i = 0; i < 3; i++) {{
            const bladeShape = new THREE.CapsuleGeometry(0.8, 30, 4, 16);
            const blade = new THREE.Mesh(bladeShape, bladeMat);
            blade.geometry.translate(0, 15, 0);
            blade.rotation.z = (i * Math.PI * 2) / 3;
            bladeGroup.add(blade);
        }}

        // Ground Grid
        const grid = new THREE.GridHelper(200, 20, 0x00d4ff, 0x1e293b);
        grid.position.y = 0.1;
        scene.add(grid);

        // Animation Loop
        let rotationSpeed = {rotation_speed};
        let frame = 0;

        function animate() {{
            requestAnimationFrame(animate);
            frame += 0.01;
            
            // Subtle camera "breathing" effect
            camera.position.x += Math.sin(frame) * 0.02;
            camera.position.y += Math.cos(frame) * 0.02;
            camera.lookAt(0, 30, 0);

            bladeGroup.rotation.z -= rotationSpeed; // Rotate blades
            renderer.render(scene, camera);
        }}

        animate();

        window.addEventListener('resize', () => {{
            camera.aspect = container.clientWidth / container.clientHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(container.clientWidth, container.clientHeight);
        }});
    </script>
    """
    components.html(html_code, height=520)
