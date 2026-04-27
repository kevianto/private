class AnomalyDetector:
    """
    Rule-based anomaly detection for the wind turbine system.
    """
    def __init__(self, model):
        self.model = model

    def check_anomalies(self, wind_speed, power_output, state):
        """
        Returns a list of alerts based on current operational data.
        """
        alerts = []

        # 1. High Wind Shutdown Alert
        if wind_speed > self.model.cut_out_speed:
            alerts.append({
                "level": "CRITICAL",
                "message": f"High wind detected ({wind_speed:.1f} m/s). Automatic shutdown initiated."
            })

        # 2. Low power at high wind (potential efficiency drop or mechanical issue)
        # Only check if it's supposed to be RUNNING
        if state == "RUNNING" and wind_speed > 10.0:
            # Expected minimum power at 10m/s with some margin
            expected_min = self.model.rated_power * 0.5
            if power_output < expected_min:
                alerts.append({
                    "level": "WARNING",
                    "message": "Low power output detected despite optimal wind conditions."
                })

        # 3. Zero output at valid wind
        if state == "RUNNING" and wind_speed >= self.model.cut_in_speed and power_output <= 0:
            alerts.append({
                "level": "ERROR",
                "message": "Zero power output during operational wind speeds. Check for mechanical failure."
            })

        return alerts
