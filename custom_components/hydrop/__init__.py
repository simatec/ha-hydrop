"""The Hydrop integration."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady

from .const import CONF_API_KEY, CONF_DEVICE_NAME, DOMAIN
from .sensor import HydropDataUpdateCoordinator

_PLATFORMS: list[Platform] = [Platform.SENSOR]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Hydrop from a config entry."""
    coordinator = HydropDataUpdateCoordinator(
        hass,
        config_entry=entry,
        device_name=entry.data[CONF_DEVICE_NAME],
        api_key=entry.data[CONF_API_KEY],
    )

    try:
        await coordinator.async_config_entry_first_refresh()
    except Exception as err:
        raise ConfigEntryNotReady(f"Could not connect to Hydrop API: {err}") from err

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, _PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, _PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok
