import streamlit.components.v1 as components

def integrated_digital_twin_viz(base_wind, is_running):
    """
    Final Robust Integrated Visualization.
    Features CDN loading with SVG fallback for maximum reliability.
    """
    is_running_str = "true" if is_running else "false"
    
    html_code = f"""
    <div id="viz-container" style="width: 100%; height: 600px; background: #0f172a; border-radius: 20px; position: relative; overflow: hidden; font-family: sans-serif; border: 1px solid rgba(255,255,255,0.05);">
        
        <!-- FALLBACK SVG (Visible until 3D loads) -->
        <div id="fallback-svg" style="position: absolute; inset: 0; display: flex; align-items: center; justify-content: center; z-index: 5;">
            <svg width="200" height="300" viewBox="0 0 100 150">
                <rect x="48" y="50" width="4" height="100" fill="#334155" />
                <g id="svg-blades">
                    <circle cx="50" cy="50" r="3" fill="#94a3b8" />
                    <line x1="50" y1="50" x2="50" y2="10" stroke="#f8fafc" stroke-width="3" />
                    <line x1="50" y1="50" x2="15" y2="70" stroke="#f8fafc" stroke-width="3" />
                    <line x1="50" y1="50" x2="85" y2="70" stroke="#f8fafc" stroke-width="3" />
                </g>
            </svg>
            <div style="position: absolute; bottom: 40px; color: #475569; font-size: 0.7rem;">LOADING 3D ENGINE...</div>
        </div>

        <!-- 3D CANVAS -->
        <div id="three-canvas" style="width: 100%; height: 100%; position: absolute; z-index: 10; opacity: 0; transition: opacity 1s;"></div>
        
        <!-- HUD -->
        <div id="hud" style="position: absolute; top: 20px; left: 20px; z-index: 20; pointer-events: none;">
            <h2 style="color: #f8fafc; margin: 0; font-size: 1.2rem;">V52 CORE TELEMETRY</h2>
            <div id="stat" style="color: #38bdf8; font-weight: 800; font-size: 0.8rem; margin-top: 5px;">SYSTEM STANDBY</div>
        </div>

        <!-- CHARTS -->
        <div style="position: absolute; bottom: 20px; left: 20px; right: 20px; height: 140px; z-index: 20; display: grid; grid-template-columns: 1fr 1fr; gap: 15px; pointer-events: none;">
            <div style="background: rgba(15,23,42,0.8); border-radius: 10px; border: 1px solid rgba(255,255,255,0.05);"><canvas id="wChart"></canvas></div>
            <div style="background: rgba(15,23,42,0.8); border-radius: 10px; border: 1px solid rgba(255,255,255,0.05);"><canvas id="pChart"></canvas></div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/three@0.149.0/build/three.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

    <script>
        const state = {{ bw: {base_wind}, run: {is_running_str}, v: 0, rot: 0 }};
        
        // 2D Animation (Always works)
        let svgRot = 0;
        function animateSVG() {{
            if (state.run) {{
                svgRot += state.bw * 0.5;
                document.getElementById('svg-blades').setAttribute('transform', 'rotate(' + svgRot + ' 50 50)');
            }}
            requestAnimationFrame(animateSVG);
        }}
        animateSVG();

        // 3D Initialization
        function init3D() {{
            if (typeof THREE === 'undefined' || typeof Chart === 'undefined') {{
                setTimeout(init3D, 500);
                return;
            }}

            const container = document.getElementById('three-canvas');
            const w = container.clientWidth || 800;
            const h = container.clientHeight || 600;

            const scene = new THREE.Scene();
            const camera = new THREE.PerspectiveCamera(45, w/h, 0.1, 1000);
            camera.position.set(80, 50, 100);
            camera.lookAt(0, 30, 0);

            const renderer = new THREE.WebGLRenderer({{ antialias: true, alpha: true }});
            renderer.setSize(w, h);
            container.appendChild(renderer.domElement);

            scene.add(new THREE.AmbientLight(0xffffff, 0.7));
            const l = new THREE.DirectionalLight(0x00d4ff, 1);
            l.position.set(50, 100, 50);
            scene.add(l);

            const mat = new THREE.MeshStandardMaterial({{ color: 0x94a3b8, roughness: 0.1, metalness: 0.9 }});
            const tower = new THREE.Mesh(new THREE.CylinderGeometry(0.8, 2, 60, 16), mat);
            tower.position.y = 30;
            scene.add(tower);

            const nac = new THREE.Mesh(new THREE.BoxGeometry(4, 4, 8), mat);
            nac.position.set(0, 60, -1);
            scene.add(nac);

            const blades = new THREE.Group();
            blades.position.set(0, 60, 3.5);
            scene.add(blades);

            for(let i=0; i<3; i++) {{
                const b = new THREE.Mesh(new THREE.CylinderGeometry(0.5, 0.2, 28, 8), new THREE.MeshStandardMaterial({{ color: 0xffffff }}));
                b.geometry.translate(0, 14, 0);
                b.rotation.z = (i * Math.PI * 2) / 3;
                blades.add(b);
            }}

            scene.add(new THREE.GridHelper(400, 40, 0x1e293b, 0x0f172a));

            const cfg = (col) => ({{
                type: 'line',
                data: {{ labels: Array(60).fill(''), datasets: [{{ data: Array(60).fill(0), borderColor: col, borderWidth: 2, fill: true, backgroundColor: col+'11', tension: 0.4, pointRadius: 0 }}] }},
                options: {{ responsive: true, maintainAspectRatio: false, animation: false, scales: {{ x:{{display:false}}, y:{{display:true, grid:{{color:'rgba(255,255,255,0.03)'}}, ticks:{{color:'#475569', font:{{size:9}}}}}} }}, plugins:{{legend:{{display:false}}}} }}
            }});

            const chartW = new Chart(document.getElementById('wChart'), cfg('#38bdf8'));
            const chartP = new Chart(document.getElementById('pChart'), cfg('#fbbf24'));

            function loop() {{
                requestAnimationFrame(loop);
                if (state.run) {{
                    state.v += (state.bw - state.v) * 0.05 + (Math.random()-0.5)*0.1;
                    const p = state.v > 3 && state.v < 25 ? Math.min(850, 0.4 * 0.5 * 1.225 * 2123 * Math.pow(state.v,3)/1000) : 0;
                    let rpm = state.v >= 3 && state.v <= 25 ? 14 + (Math.min(1, (state.v-3)/11) * 12) : 0;
                    state.rot -= (rpm / 3600) * 2 * Math.PI * 5;
                    blades.rotation.z = state.rot;
                    document.getElementById('stat').innerText = 'ACTIVE | ' + state.v.toFixed(1) + ' M/S | ' + rpm.toFixed(1) + ' RPM';
                    if (Math.random() > 0.8) {{
                        [chartW, chartP].forEach((c, i) => {{
                            c.data.datasets[0].data.push(i==0 ? state.v : p);
                            c.data.datasets[0].data.shift();
                            c.update('none');
                        }});
                    }}
                }} else {{
                    document.getElementById('stat').innerText = 'SYSTEM STANDBY';
                }}
                renderer.render(scene, camera);
            }}

            container.style.opacity = 1;
            document.getElementById('fallback-svg').style.display = 'none';
            loop();
        }}
        init3D();
    </script>
    """
    components.html(html_code, height=620)
