# Wind Turbine 3D Digital Twin Prototype

A modular, scalable Digital Twin system for a **Vestas V52** wind turbine. This project simulates real-time turbine operations using physics-based modeling, anomaly detection, and interactive visualization.

## 🏗️ Architecture

The system follows a layered modular architecture:

1.  **Data Layer**: Simulated random wind data or CSV input (`digital_twin/data/wind_data.csv`).
2.  **Model Layer**: Physics-based turbine model (`turbine_model.py`) implementing the wind power equation.
3.  **Twin Engine**: Orchestrates simulation, state management, and history (`twin_engine.py`).
4.  **Anomaly Detection**: Rule-based engine for predictive maintenance and safety alerts (`anomaly_detection.py`).
5.  **Visualization Layer**: Real-time interactive dashboard built with **Streamlit** and **Plotly** (`dashboard.py`).

## ⚙️ Physics Model

The power output (P) is calculated using the standard wind power equation:
**P = 0.5 * ρ * A * v³ * Cp**

*   **ρ (rho)**: Air density (1.225 kg/m³)
*   **A**: Rotor swept area (Diameter: 52m)
*   **v**: Wind speed (m/s)
*   **Cp**: Power coefficient (0.4)

### Operational States:
*   **OFF**: Wind speed < 3 m/s
*   **RUNNING**: Wind speed between 3 m/s and 25 m/s
*   **SHUTDOWN**: Wind speed > 25 m/s (Safety cut-out)

## 🚀 How to Run

1.  **Install dependencies**:
    ```bash
    pip install -r digital_twin/requirements.txt
    ```

2.  **Launch the dashboard**:
    ```bash
    streamlit run digital_twin/dashboard.py
    ```
    *Alternatively, run via the main entry point:*
    ```bash
    python digital_twin/main.py
    ```

## 📊 Features

*   **Real-time Simulation**: Dynamic updates of wind speed and power output.
*   **Interactive Controls**: Adjustable base wind speed and update frequency.
*   **Anomaly Alerts**:
    *   **CRITICAL**: High wind shutdown (>25 m/s).
    *   **ERROR**: Mechanical failure (Zero output during valid wind).
    *   **WARNING**: Low efficiency (Low output at high wind).
*   **Data Flexibility**: Toggle between random simulation and historical CSV data.

## 🔮 Future Improvements

*   **3D Visualization**: Integrate Three.js or PyVista for a real-time 3D rendered model.
*   **Machine Learning**: Replace rule-based detection with LSTM/GRU for advanced failure prediction.
*   **IoT Integration**: Connect to real-world MQTT sensors for live turbine monitoring.
*   **Database**: Persist long-term historical data using PostgreSQL/InfluxDB.
