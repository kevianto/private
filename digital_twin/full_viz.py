import streamlit.components.v1 as components
import requests
import streamlit as st

@st.cache_data
def get_external_scripts():
    """Fetches JS libraries server-side to bypass browser-side CDN blocking."""
    try:
        three_js = requests.get("https://unpkg.com/three@0.160.0/build/three.min.js", timeout=10).text
        chart_js = requests.get("https://cdn.jsdelivr.net/npm/chart.js", timeout=10).text
        return three_js, chart_js
    except Exception as e:
        return f"console.error('Failed to load libraries: {str(e)}');", ""

def integrated_digital_twin_viz(base_wind, is_running, current_rpm=0):
    """
    Ultra-resilient 3D + Charts Component with server-side script injection.
    """
    three_src, chart_src = get_external_scripts()
    is_running_str = "true" if is_running else "false"
    
    html_code = f"""
    <div id="viz-container-root" style="width: 100%; height: 650px; background: #0f172a; border-radius: 20px; position: relative; overflow: hidden; font-family: sans-serif; border: 1px solid rgba(255,255,255,0.05);">
        <div id="status-overlay" style="position: absolute; inset: 0; background: #0f172a; display: flex; flex-direction: column; align-items: center; justify-content: center; z-index: 100; color: #38bdf8; text-align: center; padding: 20px;">
            <div id="status-text" style="font-size: 1.2rem; font-weight: bold; margin-bottom: 10px;">INITIALIZING CORE TELEMETRY...</div>
            <div id="error-details" style="font-size: 0.8rem; color: #94a3b8; margin-top: 10px; max-width: 80%; font-family: monospace;">Connecting to V52 Unit</div>
        </div>
        <div id="three-canvas-container" style="width: 100%; height: 100%; position: absolute; top: 0; left: 0;"></div>
        <div id="hud-overlay" style="position: absolute; top: 25px; left: 25px; pointer-events: none; z-index: 10; display: none;">
            <div style="color: #94a3b8; font-size: 0.7rem; font-weight: 800; letter-spacing: 2px;">LTWP V52 DT-PROTOTYPE</div>
            <h1 style="color: #f8fafc; margin: 0; font-size: 1.6rem; font-weight: 900; line-height: 1.2;">CORE ANALYTICS</h1>
            <div id="status-indicator" style="display: inline-block; margin-top: 10px; padding: 4px 10px; border-radius: 4px; background: rgba(30,41,59,0.9); color: #38bdf8; font-size: 0.7rem; font-weight: 800; border: 1px solid #38bdf8;">INITIALIZING</div>
            <div id="rpm-display" style="color: #fbbf24; font-size: 0.9rem; font-weight: 800; margin-top: 5px;">ROTOR SPEED: 0.0 RPM</div>
        </div>
        <div id="charts-overlay" style="position: absolute; bottom: 20px; left: 20px; right: 20px; height: 160px; display: grid; grid-template-columns: 1fr 1fr; gap: 20px; pointer-events: none; z-index: 10; display: none;">
            <div style="background: rgba(15, 23, 42, 0.9); border-radius: 12px; padding: 10px; border: 1px solid rgba(255,255,255,0.05);"><canvas id="jsWindChart"></canvas></div>
            <div style="background: rgba(15, 23, 42, 0.9); border-radius: 12px; padding: 10px; border: 1px solid rgba(255,255,255,0.05);"><canvas id="jsPowerChart"></canvas></div>
        </div>
    </div>

    <script>
        {three_src}
    </script>
    <script>
        {chart_src}
    </script>

    <script>
        window.onerror = function(msg) {{
            document.getElementById('status-text').innerText = "SYSTEM ERROR";
            document.getElementById('error-details').innerText = msg;
            return false;
        }};

        function init() {{
            const container = document.getElementById('three-canvas-container');
            const overlay = document.getElementById('status-overlay');
            const hud = document.getElementById('hud-overlay');
            const charts = document.getElementById('charts-overlay');
            const statusIndicator = document.getElementById('status-indicator');
            const rpmDisplay = document.getElementById('rpm-display');

            const width = container.clientWidth || window.innerWidth;
            const height = container.clientHeight || 650;

            if (width < 50) {{
                setTimeout(init, 200);
                return;
            }}

            const scene = new THREE.Scene();
            const camera = new THREE.PerspectiveCamera(45, width / height, 0.1, 1000);
            camera.position.set(80, 50, 100);
            camera.lookAt(0, 30, 0);

            const renderer = new THREE.WebGLRenderer({{ antialias: true, alpha: true }});
            renderer.setSize(width, height);
            container.appendChild(renderer.domElement);

            scene.add(new THREE.AmbientLight(0xffffff, 0.8));
            const sun = new THREE.DirectionalLight(0x00d4ff, 1.2);
            sun.position.set(50, 100, 50);
            scene.add(sun);

            const metalMat = new THREE.MeshStandardMaterial({{ color: 0x94a3b8, roughness: 0.1, metalness: 0.9 }});
            const tower = new THREE.Mesh(new THREE.CylinderGeometry(1, 2, 60, 16), metalMat);
            tower.position.y = 30;
            scene.add(tower);

            const nacelle = new THREE.Mesh(new THREE.BoxGeometry(4, 4, 8), metalMat);
            nacelle.position.set(0, 60, -1);
            scene.add(nacelle);

            const bladeGroup = new THREE.Group();
            bladeGroup.position.set(0, 60, 3.5);
            scene.add(bladeGroup);

            const bladeGeo = new THREE.CylinderGeometry(0.5, 0.3, 28, 8);
            for(let i=0; i<3; i++) {{
                const blade = new THREE.Mesh(bladeGeo, new THREE.MeshStandardMaterial({{ color: 0xffffff }}));
                blade.geometry.translate(0, 14, 0);
                blade.rotation.z = (i * Math.PI * 2) / 3;
                bladeGroup.add(blade);
            }}

            scene.add(new THREE.GridHelper(400, 40, 0x1e293b, 0x0f172a));

            const chartCfg = (color) => ({{
                type: 'line',
                data: {{ labels: Array(60).fill(''), datasets: [{{ data: Array(60).fill(0), borderColor: color, borderWidth: 2, fill: true, backgroundColor: color+'11', tension: 0.4, pointRadius: 0 }}] }},
                options: {{ responsive: true, maintainAspectRatio: false, animation: false, scales: {{ x:{{display:false}}, y:{{display:true, grid:{{color:'rgba(255,255,255,0.03)'}}, ticks:{{color:'#475569', font:{{size:9}}}}}} }}, plugins:{{legend:{{display:false}}}} }}
            }});

            const windChart = new Chart(document.getElementById('jsWindChart'), chartCfg('#38bdf8'));
            const powerChart = new Chart(document.getElementById('jsPowerChart'), chartCfg('#fbbf24'));

            let state = {{ baseWind: {base_wind}, running: {is_running_str}, v: 0, rot: 0 }};

            function animate() {{
                requestAnimationFrame(animate);
                if (state.running) {{
                    state.v += (state.baseWind - state.v) * 0.05 + (Math.random()-0.5)*0.1;
                    const v = state.v;
                    const pwr = (v > 3 && v < 25) ? Math.min(850, 0.4 * 0.5 * 1.225 * 2123 * Math.pow(v,3)/1000) : 0;
                    
                    let rpm = 0;
                    if (v >= 3 && v <= 25) {{
                        const ratio = Math.min(1.0, (v - 3.0) / (14.0 - 3.0));
                        rpm = 14.0 + (ratio * (26.0 - 14.0));
                    }}
                    
                    state.rot -= (rpm / 3600) * 2 * Math.PI * 5;
                    bladeGroup.rotation.z = state.rot;

                    statusIndicator.innerText = `ACTIVE | ${{state.v.toFixed(1)}} M/S`;
                    rpmDisplay.innerText = `ROTOR SPEED: ${{rpm.toFixed(1)}} RPM`;
                    
                    if (Math.random() > 0.8) {{
                        [windChart, powerChart].forEach((c, i) => {{
                            c.data.datasets[0].data.push(i==0 ? state.v : pwr);
                            c.data.datasets[0].data.shift();
                            c.update('none');
                        }});
                    }}
                }} else {{
                    statusIndicator.innerText = 'OFFLINE';
                    rpmDisplay.innerText = 'ROTOR SPEED: 0.0 RPM';
                }}
                renderer.render(scene, camera);
            }}

            overlay.style.display = 'none';
            hud.style.display = 'block';
            charts.style.display = 'grid';
            animate();
        }}

        init();
    </script>
    """
    components.html(html_code, height=660)
