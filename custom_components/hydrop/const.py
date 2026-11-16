"""Constants for the Hydrop integration."""

DOMAIN = "hydrop"

CONF_API_KEY = "apikey"
CONF_DEVICE_NAME = "device_name"
CONF_SENSOR_NAME = "name"
CONF_SCAN_INTERVAL = "scan_interval"

DEFAULT_SENSOR_NAME = "Wasserzähler"

# Polling interval in minutes
DEFAULT_SCAN_INTERVAL = 10
MIN_SCAN_INTERVAL = 5
MAX_SCAN_INTERVAL = 1440

API_BASE_URL = "https://api.hydrop-systems.com/sensors/ID/{device_name}/newest"
