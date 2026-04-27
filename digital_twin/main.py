import os
import sys
import subprocess

def run_dashboard():
    """Launcher for the Streamlit dashboard."""
    try:
        print("Starting Wind Turbine Digital Twin Dashboard...")
        subprocess.run(["streamlit", "run", "digital_twin/dashboard.py"])
    except KeyboardInterrupt:
        print("\nStopping simulation.")
    except Exception as e:
        print(f"Error starting dashboard: {e}")

if __name__ == "__main__":
    run_dashboard()
