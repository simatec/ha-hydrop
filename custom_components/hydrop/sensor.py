"""Sensor entity for the Hydrop integration."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
import logging
from typing import Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
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
    CONF_DEVICE_NAME,
    CONF_SENSOR_NAME,
    DOMAIN,
    SCAN_INTERVAL_SECONDS,
)

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(seconds=SCAN_INTERVAL_SECONDS)


SENSOR_DESCRIPTIONS: tuple[SensorEntityDescription, ...] = (
    SensorEntityDescription(
        key="meterReading",
        translation_key="meter_reading",
        device_class=SensorDeviceClass.WATER,
        state_class=SensorStateClass.TOTAL_INCREASING,
        native_unit_of_measurement="m³",
        icon="mdi:water-pump",
    ),
    SensorEntityDescription(
        key="averageFlowRate",
        translation_key="average_flow_rate",
        device_class=None,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement="L/min",
        icon="mdi:water-flow",
    ),
    SensorEntityDescription(
        key="dailyConsumption",
        translation_key="daily_consumption",
        device_class=SensorDeviceClass.WATER,
        state_class=SensorStateClass.TOTAL_INCREASING,
        native_unit_of_measurement="L",
        icon="mdi:water",
    ),
    SensorEntityDescription(
        key="measurementTime",
        translation_key="measurement_time",
        device_class=SensorDeviceClass.TIMESTAMP,
        state_class=None,
        native_unit_of_measurement=None,
        icon="mdi:clock-outline",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up the Hydrop sensor platform."""
    coordinator: HydropDataUpdateCoordinator = hass.data[DOMAIN][config_entry.entry_id]
    sensor_name = config_entry.data[CONF_SENSOR_NAME]

    async_add_entities(
        HydropSensor(coordinator, config_entry, sensor_name, description)
        for description in SENSOR_DESCRIPTIONS
    )


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
        self._last_meter_value: float | None = None
        self._last_timestamp: int | None = None
        self._day_start_value: float | None = None
        self._day_start_date: str | None = None

    async def _async_update_data(self) -> dict:
        """Fetch data from Hydrop API."""
        session = async_get_clientsession(self.hass)
        try:
            async with session.get(
                self.url,
                headers={"apikey": self.api_key},
            ) as response:
                response.raise_for_status()
                raw = await response.json()
                return self._parse(raw)
        except Exception as err:
            raise UpdateFailed(f"Error fetching Hydrop data: {err}") from err

    def _parse(self, data: dict) -> dict:
        """Extract and compute all sensor values from raw API response."""
        result: dict[str, Any] = {}
        try:
            sensors = data.get("sensors", [])
            if not sensors or not sensors[0].get("records"):
                return result

            records = sensors[0]["records"]
            latest = records[0]

            current_value = float(latest["meterValue"])
            raw_ts = latest.get("timestamp")

            result["meterReading"] = current_value

            # Unix-Timestamp → timezone-aware datetime
            if raw_ts is not None:
                try:
                    result["measurementTime"] = datetime.fromtimestamp(
                        int(raw_ts), tz=timezone.utc
                    )
                except (ValueError, TypeError, OSError):
                    result["measurementTime"] = None
            else:
                result["measurementTime"] = None

            # Tagesbeginn-Wert zurücksetzen wenn neuer Tag
            today = datetime.now(tz=timezone.utc).strftime("%Y-%m-%d")
            if self._day_start_date != today:
                self._day_start_value = current_value
                self._day_start_date = today

            # Tagesverbrauch in Liter
            if self._day_start_value is not None:
                daily_m3 = current_value - self._day_start_value
                result["dailyConsumption"] = round(daily_m3 * 1000, 2)
            else:
                result["dailyConsumption"] = 0.0

            # Durchfluss: Differenz zum letzten Messwert in L/min
            if (
                self._last_meter_value is not None
                and self._last_timestamp is not None
                and raw_ts is not None
                and int(raw_ts) != self._last_timestamp
            ):
                delta_m3 = current_value - self._last_meter_value
                delta_sec = int(raw_ts) - self._last_timestamp
                if delta_sec > 0:
                    result["averageFlowRate"] = round(
                        (delta_m3 * 1000) / (delta_sec / 60), 3
                    )
                else:
                    result["averageFlowRate"] = 0.0
            else:
                result["averageFlowRate"] = 0.0

            # Aktuelle Werte für nächsten Durchlauf speichern
            self._last_meter_value = current_value
            self._last_timestamp = int(raw_ts) if raw_ts is not None else None

        except (KeyError, IndexError, TypeError, ValueError) as err:
            _LOGGER.warning("Could not parse Hydrop data: %s", err)

        return result


class HydropSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Hydrop sensor."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: HydropDataUpdateCoordinator,
        config_entry: ConfigEntry,
        sensor_name: str,
        description: SensorEntityDescription,
    ) -> None:
        """Initialize the Hydrop sensor."""
        super().__init__(coordinator, config_entry)
        self.entity_description = description
        self._attr_unique_id = (
            f"hydrop_{config_entry.data[CONF_DEVICE_NAME]}_{description.key}"
        )
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, config_entry.data[CONF_DEVICE_NAME])},
            name=sensor_name,
            manufacturer="Hydrop Systems",
            model="Wasserzähler",
            configuration_url="https://hydrop-systems.com",
        )

    @property
    def native_value(self) -> Any:
        """Return the current sensor value."""
        if self.coordinator.data is None:
            return None
        return self.coordinator.data.get(self.entity_description.key)
