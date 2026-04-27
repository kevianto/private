import pandas as pd
import numpy as np
import time
from datetime import datetime
from turbine_model import TurbineModel
from anomaly_detection import AnomalyDetector

class TwinEngine:
    """
    Simulation engine for the Wind Turbine Digital Twin.
    Manages state history and time-stepping.
    """
    def __init__(self):
        self.model = TurbineModel()
        self.detector = AnomalyDetector(self.model)
        self.history = pd.DataFrame(columns=[
            "timestamp", "wind_speed", "power_kw", "rpm", "state", "alerts"
        ])

    def step(self, wind_speed):
        """Executes a single simulation time step."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Calculate values from model
        power_watts, state = self.model.calculate_power(wind_speed)
        power_kw = power_watts / 1000.0
        rpm = self.model.calculate_rpm(wind_speed)
        
        # Check for anomalies
        alerts = self.detector.check_anomalies(wind_speed, power_watts, state)
        alert_msg = "; ".join([a['message'] for a in alerts]) if alerts else "None"
        
        # Update history
        new_row = {
            "timestamp": timestamp,
            "wind_speed": float(wind_speed),
            "power_kw": float(power_kw),
            "rpm": float(rpm),
            "state": state,
            "alerts": alert_msg
        }
        
        self.history = pd.concat([self.history, pd.DataFrame([new_row])], ignore_index=True)
        
        # Keep only last 100 steps for performance
        if len(self.history) > 100:
            self.history = self.history.iloc[1:].reset_index(drop=True)
            
        return new_row, alerts

    def generate_random_wind(self, base_speed=12.0):
        """Generates realistic fluctuating wind speed."""
        noise = np.random.normal(0, 1.5)
        return max(0.0, base_speed + noise)

    def reset_history(self):
        self.history = self.history.iloc[0:0]
