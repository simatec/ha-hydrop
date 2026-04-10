"""Sensor entity for the Hydrop integration."""

from __future__ import annotations

from datetime import timedelta
import logging

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
    UpdateFailed,
)

from .const import (
    API_BASE_URL,
    CONF_API_KEY,
    CONF_DEVICE_NAME,
    CONF_SENSOR_NAME,
    DOMAIN,
    SCAN_INTERVAL_SECONDS,
)

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(seconds=SCAN_INTERVAL_SECONDS)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up the Hydrop sensor platform."""
    device_name = config_entry.data[CONF_DEVICE_NAME]
    api_key = config_entry.data[CONF_API_KEY]
    sensor_name = config_entry.data[CONF_SENSOR_NAME]

    coordinator = HydropDataUpdateCoordinator(
        hass,
        config_entry=config_entry,
        device_name=device_name,
        api_key=api_key,
    )

    await coordinator.async_config_entry_first_refresh()

    async_add_entities([HydropSensor(coordinator, config_entry, sensor_name)])


class HydropDataUpdateCoordinator(DataUpdateCoordinator):
    """Coordinator to fetch data from Hydrop API."""

    def __init__(
        self,
        hass: HomeAssistant,
        config_entry: ConfigEntry,
        device_name: str,
        api_key: str,
    ) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=SCAN_INTERVAL,
            config_entry=config_entry,
        )
        self.device_name = device_name
        self.api_key = api_key
        self.url = API_BASE_URL.format(device_name=device_name)

    async def _async_update_data(self) -> dict:
        """Fetch data from Hydrop API."""
        session = async_get_clientsession(self.hass)
        try:
            async with session.get(
                self.url,
                headers={"apikey": self.api_key},
            ) as response:
                response.raise_for_status()
                return await response.json()
        except Exception as err:
            raise UpdateFailed(f"Error fetching Hydrop data: {err}") from err


class HydropSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Hydrop water meter sensor."""

    _attr_device_class = SensorDeviceClass.WATER
    _attr_state_class = SensorStateClass.TOTAL_INCREASING
    _attr_native_unit_of_measurement = "m³"

    def __init__(
        self,
        coordinator: HydropDataUpdateCoordinator,
        config_entry: ConfigEntry,
        sensor_name: str,
    ) -> None:
        """Initialize the Hydrop sensor."""
        super().__init__(coordinator, config_entry)
        self._attr_name = sensor_name
        self._attr_unique_id = f"hydrop_{config_entry.data[CONF_DEVICE_NAME]}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, config_entry.data[CONF_DEVICE_NAME])},
            name=sensor_name,
            manufacturer="Hydrop Systems",
            model="Wasserzähler",
            configuration_url="https://hydrop-systems.com",
        )

    @property
    def native_value(self) -> float | None:
        """Return the current meter value."""
        data = self.coordinator.data
        try:
            sensors = data.get("sensors", [])
            if sensors and sensors[0].get("records"):
                return float(sensors[0]["records"][0]["meterValue"])
        except (KeyError, IndexError, TypeError, ValueError) as err:
            _LOGGER.warning("Could not parse Hydrop meter value: %s", err)
        return None

    @property
    def extra_state_attributes(self) -> dict | None:
        """Return extra state attributes."""
        data = self.coordinator.data
        try:
            sensors = data.get("sensors", [])
            if sensors and sensors[0].get("records"):
                record = sensors[0]["records"][0]
                return {
                    "timestamp": record.get("timestamp"),
                    "meterValue": record.get("meterValue"),
                }
        except (KeyError, IndexError, TypeError):
            pass
        return None
