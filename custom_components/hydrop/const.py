"""Constants for the Hydrop integration."""

DOMAIN = "hydrop"

CONF_API_KEY = "apikey"
CONF_DEVICE_NAME = "device_name"
CONF_SENSOR_NAME = "name"

DEFAULT_SENSOR_NAME = "Wasserzähler"
SCAN_INTERVAL_SECONDS = 300

API_BASE_URL = "https://api.hydrop-systems.com/sensors/ID/{device_name}/newest"
