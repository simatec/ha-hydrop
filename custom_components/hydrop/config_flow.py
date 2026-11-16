"""Config flow for the Hydrop integration."""

from __future__ import annotations

import logging
from typing import Any

import aiohttp
import voluptuous as vol

from homeassistant.config_entries import (
    ConfigEntry,
    ConfigFlow,
    ConfigFlowResult,
    OptionsFlowWithReload,
)
from homeassistant.core import callback
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.selector import (
    NumberSelector,
    NumberSelectorConfig,
    NumberSelectorMode,
)

from .const import (
    API_BASE_URL,
    CONF_API_KEY,
    CONF_DEVICE_NAME,
    CONF_SCAN_INTERVAL,
    CONF_SENSOR_NAME,
    DEFAULT_SCAN_INTERVAL,
    DEFAULT_SENSOR_NAME,
    DOMAIN,
    MAX_SCAN_INTERVAL,
    MIN_SCAN_INTERVAL,
)

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL_SELECTOR = NumberSelector(
    NumberSelectorConfig(
        min=MIN_SCAN_INTERVAL,
        max=MAX_SCAN_INTERVAL,
        step=1,
        mode=NumberSelectorMode.BOX,
        unit_of_measurement="min",
    )
)

SCHEMA_DEVICE = vol.Schema(
    {
        vol.Required(CONF_SENSOR_NAME, default=DEFAULT_SENSOR_NAME): cv.string,
        vol.Required(CONF_DEVICE_NAME): cv.string,
        vol.Required(CONF_API_KEY): cv.string,
        vol.Required(
            CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL
        ): SCAN_INTERVAL_SELECTOR,
    }
)


async def _test_credentials(hass, device_name: str, api_key: str) -> bool:
    """Test if the provided credentials are valid."""
    url = API_BASE_URL.format(device_name=device_name)
    session = async_get_clientsession(hass)
    try:
        async with session.get(
            url,
            headers={"apikey": api_key},
            timeout=aiohttp.ClientTimeout(total=10),
        ) as response:
            if response.status == 200:
                return True
            _LOGGER.error(
                "Hydrop API returned status %s for device '%s'",
                response.status,
                device_name,
            )
            return False
    except (aiohttp.ClientError, TimeoutError) as err:
        _LOGGER.error("Error connecting to Hydrop API: %s", err)
        return False


class HydropFlowHandler(ConfigFlow, domain=DOMAIN):
    """Config flow for Hydrop."""

    VERSION = 1

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: ConfigEntry) -> HydropOptionsFlow:
        """Return the options flow handler."""
        return HydropOptionsFlow()

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle a flow initialized by the user."""
        errors = {}

        if user_input is not None:
            device_name = user_input[CONF_DEVICE_NAME]
            api_key = user_input[CONF_API_KEY]

            await self.async_set_unique_id(device_name)
            self._abort_if_unique_id_configured()

            if await _test_credentials(self.hass, device_name, api_key):
                return self.async_create_entry(
                    title=user_input[CONF_SENSOR_NAME],
                    data={
                        CONF_SENSOR_NAME: user_input[CONF_SENSOR_NAME],
                        CONF_DEVICE_NAME: device_name,
                        CONF_API_KEY: api_key,
                    },
                    options={
                        CONF_SCAN_INTERVAL: int(user_input[CONF_SCAN_INTERVAL]),
                    },
                )
            errors["base"] = "cannot_connect"

        return self.async_show_form(
            step_id="user",
            data_schema=self.add_suggested_values_to_schema(
                SCHEMA_DEVICE, user_input
            ),
            errors=errors,
        )

    async def async_step_reconfigure(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Allow changing display name and API key of an existing entry."""
        entry = self._get_reconfigure_entry()
        errors = {}

        if user_input is not None:
            device_name = entry.data[CONF_DEVICE_NAME]
            if await _test_credentials(
                self.hass, device_name, user_input[CONF_API_KEY]
            ):
                return self.async_update_reload_and_abort(
                    entry,
                    title=user_input[CONF_SENSOR_NAME],
                    data_updates={
                        CONF_SENSOR_NAME: user_input[CONF_SENSOR_NAME],
                        CONF_API_KEY: user_input[CONF_API_KEY],
                    },
                )
            errors["base"] = "cannot_connect"

        schema = vol.Schema(
            {
                vol.Required(CONF_SENSOR_NAME): cv.string,
                vol.Required(CONF_API_KEY): cv.string,
            }
        )
        return self.async_show_form(
            step_id="reconfigure",
            data_schema=self.add_suggested_values_to_schema(
                schema, user_input or entry.data
            ),
            description_placeholders={
                "device_name": entry.data[CONF_DEVICE_NAME]
            },
            errors=errors,
        )


class HydropOptionsFlow(OptionsFlowWithReload):
    """Options flow for Hydrop (polling interval)."""

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(
                data={CONF_SCAN_INTERVAL: int(user_input[CONF_SCAN_INTERVAL])}
            )

        current = self.config_entry.options.get(
            CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL
        )
        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_SCAN_INTERVAL, default=current
                    ): SCAN_INTERVAL_SELECTOR,
                }
            ),
        )
