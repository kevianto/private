import os
import sys

# Ensure the digital_twin directory is in the path for internal imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'digital_twin'))

# Import the dashboard as the main entry point
from digital_twin import dashboard
