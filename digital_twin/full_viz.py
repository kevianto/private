import streamlit.components.v1 as components
import requests
import streamlit as st

@st.cache_data
def get_external_scripts():
    """Fetches JS libraries server-side with fallback to robust versions."""
    try:
        # Using r149 - the last version with full standard minified support
        three_js = requests.get("https://cdnjs.cloudflare.com/ajax/libs/three.js/r149/three.min.js", timeout=10).text
        chart_js = requests.get("https://cdn.jsdelivr.net/npm/chart.js", timeout=10).text
        return three_js, chart_js
    except Exception as e:
        return f"console.error('Fetch failed: {str(e)}');", ""

def integrated_digital_twin_viz(base_wind, is_running, current_rpm=0):
    """
    Stabilized 3D + Charts Component.
    Uses version 0.149.0 for maximum compatibility with standard script tags.
    """
    three_src, chart_src = get_external_scripts()
    is_running_str = "true" if is_running else "false"
    
    html_code = f"""
    <div id="viz-root" style="width: 100%; height: 650px; background: #0f172a; border-radius: 20px; position: relative; overflow: hidden; font-family: sans-serif;">
        <div id="overlay" style="position: absolute; inset: 0; background: #0f172a; display: flex; align-items: center; justify-content: center; z-index: 100; color: #38bdf8;">
            <div style="font-weight: bold;">SYNCHRONIZING DIGITAL TWIN...</div>
        </div>
        <div id="canvas-container" style="width: 100%; height: 100%;"></div>
        <div id="hud" style="position: absolute; top: 25px; left: 25px; pointer-events: none; z-index: 10; display: none;">
            <div style="color: #94a3b8; font-size: 0.7rem; font-weight: 800; letter-spacing: 2px;">LTWP V52 DT-UNIT</div>
            <h1 style="color: #f8fafc; margin: 0; font-size: 1.6rem; font-weight: 900;">CORE ANALYTICS</h1>
            <div id="status-ind" style="display: inline-block; margin-top: 10px; padding: 4px 10px; border-radius: 4px; background: rgba(56,189,248,0.1); color: #38bdf8; font-size: 0.7rem; font-weight: 800; border: 1px solid #38bdf8;">BOOTING</div>
            <div id="rpm-val" style="color: #fbbf24; font-size: 0.9rem; font-weight: 800; margin-top: 5px;">0.0 RPM</div>
        </div>
        <div id="charts" style="position: absolute; bottom: 20px; left: 20px; right: 20px; height: 160px; display: grid; grid-template-columns: 1fr 1fr; gap: 20px; pointer-events: none; z-index: 10; display: none;">
            <div style="background: rgba(15, 23, 42, 0.9); border-radius: 12px; padding: 10px; border: 1px solid rgba(255,255,255,0.05);"><canvas id="cWind"></canvas></div>
            <div style="background: rgba(15, 23, 42, 0.9); border-radius: 12px; padding: 10px; border: 1px solid rgba(255,255,255,0.05);"><canvas id="cPower"></canvas></div>
        </div>
    </div>

    <script>{three_src}</script>
    <script>{chart_src}</script>

    <script>
        function init() {{
            if (typeof THREE === 'undefined') {{
                setTimeout(init, 200);
                return;
            }}

            const container = document.getElementById('canvas-container');
            const w = container.clientWidth || window.innerWidth;
            const h = container.clientHeight || 650;

            const scene = new THREE.Scene();
            const camera = new THREE.PerspectiveCamera(45, w/h, 0.1, 1000);
            camera.position.set(80, 50, 100);
            camera.lookAt(0, 30, 0);

            const renderer = new THREE.WebGLRenderer({{ antialias: true, alpha: true }});
            renderer.setSize(w, h);
            container.appendChild(renderer.domElement);

            scene.add(new THREE.AmbientLight(0xffffff, 0.8));
            const light = new THREE.DirectionalLight(0x00d4ff, 1);
            light.position.set(50, 100, 50);
            scene.add(light);

            const metal = new THREE.MeshStandardMaterial({{ color: 0x94a3b8, roughness: 0.1, metalness: 0.9 }});
            const tower = new THREE.Mesh(new THREE.CylinderGeometry(0.8, 2, 60, 16), metal);
            tower.position.y = 30;
            scene.add(tower);

            const nacelle = new THREE.Mesh(new THREE.BoxGeometry(4, 4, 8), metal);
            nacelle.position.set(0, 60, -1);
            scene.add(nacelle);

            const bladeGroup = new THREE.Group();
            bladeGroup.position.set(0, 60, 3.5);
            scene.add(bladeGroup);

            const bGeo = new THREE.CylinderGeometry(0.5, 0.2, 28, 8);
            for(let i=0; i<3; i++) {{
                const b = new THREE.Mesh(bGeo, new THREE.MeshStandardMaterial({{ color: 0xffffff }}));
                b.geometry.translate(0, 14, 0);
                b.rotation.z = (i * Math.PI * 2) / 3;
                bladeGroup.add(b);
            }}

            scene.add(new THREE.GridHelper(400, 40, 0x1e293b, 0x0f172a));

            const cfg = (col) => ({{
                type: 'line',
                data: {{ labels: Array(60).fill(''), datasets: [{{ data: Array(60).fill(0), borderColor: col, borderWidth: 2, fill: true, backgroundColor: col+'11', tension: 0.4, pointRadius: 0 }}] }},
                options: {{ responsive: true, maintainAspectRatio: false, animation: false, scales: {{ x:{{display:false}}, y:{{display:true, grid:{{color:'rgba(255,255,255,0.03)'}}, ticks:{{color:'#475569', font:{{size:9}}}}}} }}, plugins:{{legend:{{display:false}}}} }}
            }});

            const chartW = new Chart(document.getElementById('cWind'), cfg('#38bdf8'));
            const chartP = new Chart(document.getElementById('cPower'), cfg('#fbbf24'));

            let state = {{ bw: {base_wind}, run: {is_running_str}, v: 0, rot: 0 }};

            function animate() {{
                requestAnimationFrame(animate);
                if (state.run) {{
                    state.v += (state.bw - state.v) * 0.05 + (Math.random()-0.5)*0.1;
                    const p = (state.v > 3 && state.v < 25) ? Math.min(850, 0.4 * 0.5 * 1.225 * 2123 * Math.pow(state.v,3)/1000) : 0;
                    let rpm = state.v >= 3 && state.v <= 25 ? 14.0 + (Math.min(1.0, (state.v-3)/11.0) * 12.0) : 0;
                    state.rot -= (rpm / 3600) * 2 * Math.PI * 5;
                    bladeGroup.rotation.z = state.rot;
                    document.getElementById('status-ind').innerText = 'ACTIVE | ' + state.v.toFixed(1) + ' M/S';
                    document.getElementById('rpm-val').innerText = 'ROTOR: ' + rpm.toFixed(1) + ' RPM';
                    if (Math.random() > 0.8) {{
                        [chartW, chartP].forEach((c, i) => {{
                            c.data.datasets[0].data.push(i==0 ? state.v : p);
                            c.data.datasets[0].data.shift();
                            c.update('none');
                        }});
                    }}
                }} else {{
                    document.getElementById('status-ind').innerText = 'OFFLINE';
                }}
                renderer.render(scene, camera);
            }}

            document.getElementById('overlay').style.display = 'none';
            document.getElementById('hud').style.display = 'block';
            document.getElementById('charts').style.display = 'grid';
            animate();
        }}
        init();
    </script>
    """
    components.html(html_code, height=660)
