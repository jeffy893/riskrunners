"""
Project Crucible — Configuration
Reads NERIS API credentials from environment variables.
Falls back to simulated data if credentials are not available.
"""

import os

# NERIS API Configuration
API_BASE_URL = "https://api.neris.fsri.org/v1"
DEFAULT_STATE = "AZ"
DEFAULT_INCIDENT_TYPES = "FIRE"
DEFAULT_PAGE_SIZE = 100

# Credentials from environment
NERIS_CLIENT_ID = os.environ.get("NERIS_CLIENT_ID")
NERIS_CLIENT_SECRET = os.environ.get("NERIS_CLIENT_SECRET")

# If credentials are not set, use simulated data
USE_SIMULATED_DATA = not (NERIS_CLIENT_ID and NERIS_CLIENT_SECRET)

# Output configuration
OUTPUT_DIR = "output"
OUTPUT_KML_FILENAME = "az_fire_incidents.kml"
