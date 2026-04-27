import plotly.graph_objects as go
import numpy as np

def create_turbine_3d(rotation_angle_deg):
    """
    Creates a 3D Plotly figure representing a wind turbine.
    """
    angle_rad = np.radians(rotation_angle_deg)
    
    # Turbine Dimensions
    tower_height = 50
    blade_length = 25
    hub_radius = 2
    
    fig = go.Figure()

    # 1. Tower (Vertical Cylinder/Line)
    fig.add_trace(go.Scatter3d(
        x=[0, 0], y=[0, 0], z=[0, tower_height],
        mode='lines',
        line=dict(color='silver', width=10),
        name="Tower"
    ))

    # 2. Hub (Sphere-ish)
    fig.add_trace(go.Scatter3d(
        x=[0], y=[0], z=[tower_height],
        mode='markers',
        marker=dict(size=8, color='darkgray'),
        name="Hub"
    ))

    # 3. Blades (3 lines offset by 120 degrees)
    for i in range(3):
        blade_angle = angle_rad + (i * 2 * np.pi / 3)
        # Blades rotate in the YZ plane (facing X)
        by = [0, blade_length * np.cos(blade_angle)]
        bz = [tower_height, tower_height + blade_length * np.sin(blade_angle)]
        bx = [0, 0]
        
        fig.add_trace(go.Scatter3d(
            x=bx, y=by, z=bz,
            mode='lines',
            line=dict(color='white', width=8),
            name=f"Blade {i+1}"
        ))

    # 4. Foundation / Ground
    ground_size = 40
    fig.add_trace(go.Mesh3d(
        x=[-ground_size, ground_size, ground_size, -ground_size],
        y=[-ground_size, -ground_size, ground_size, ground_size],
        z=[0, 0, 0, 0],
        color='green', opacity=0.3,
        name="Ground"
    ))

    # Layout settings
    fig.update_layout(
        showlegend=False,
        scene=dict(
            xaxis=dict(nticks=4, range=[-50, 50], showbackground=False),
            yaxis=dict(nticks=4, range=[-50, 50], showbackground=False),
            zaxis=dict(nticks=4, range=[0, 80], showbackground=False),
            aspectmode='cube'
        ),
        margin=dict(r=0, l=0, b=0, t=0),
        height=400
    )
    
    return fig
