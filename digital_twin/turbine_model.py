import numpy as np

class TurbineModel:
    """
    Physics-based model for a wind turbine (Vestas V52 specifications).
    """
    def __init__(self):
        # Vestas V52 Specifications
        self.rotor_diameter = 52  # meters
        self.rotor_area = np.pi * (self.rotor_diameter / 2)**2
        self.air_density = 1.225  # kg/m^3 (sea level)
        self.cp = 0.4  # Power coefficient (efficiency)
        
        # Operating thresholds (Refined per LTWP V52 specs)
        self.cut_in_speed = 3.0   # m/s
        self.rated_speed = 14.0   # m/s (Per proposal specification)
        self.cut_out_speed = 25.0  # m/s
        self.rated_power = 850000 # 850 kW in Watts
        self.max_rpm = 26.0       # Max rotor speed for V52

    def calculate_power(self, wind_speed):
        """
        Calculates power output based on wind speed and turbine state.
        P = 0.5 * rho * A * v^3 * Cp
        """
        state = self.get_state(wind_speed)
        
        if state == "OFF" or state == "SHUTDOWN":
            return 0.0, state
        
        # RUNNING state
        if wind_speed >= self.rated_speed:
            return float(self.rated_power), state
        
        # Power equation
        power = 0.5 * self.air_density * self.rotor_area * (wind_speed**3) * self.cp
        return min(float(power), float(self.rated_power)), state

    def calculate_rpm(self, wind_speed):
        """
        Calculates approximate RPM. 
        Typical V52 range is 14-26 RPM.
        """
        state = self.get_state(wind_speed)
        if state == "OFF" or state == "SHUTDOWN":
            return 0.0
        
        if wind_speed >= self.rated_speed:
            return self.max_rpm
            
        # Linear approximation between cut-in and rated
        ratio = (wind_speed - self.cut_in_speed) / (self.rated_speed - self.cut_in_speed)
        rpm = 14.0 + (ratio * (self.max_rpm - 14.0))
        return float(rpm)

    def get_state(self, wind_speed):
        """Determines the operational state of the turbine."""
        if wind_speed < self.cut_in_speed:
            return "OFF"
        elif wind_speed > self.cut_out_speed:
            return "SHUTDOWN"
        else:
            return "RUNNING"
