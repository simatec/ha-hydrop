"""Config flow for the Hydrop integration."""

from __future__ import annotations

import logging
from typing import Any

import aiohttp
import voluptuous as vol

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.helpers import config_validation as cv

from .const import (
    API_BASE_URL,
    CONF_API_KEY,
    CONF_DEVICE_NAME,
    CONF_SENSOR_NAME,
    DEFAULT_SENSOR_NAME,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)

SCHEMA_DEVICE = vol.Schema(
    {
        vol.Required(CONF_SENSOR_NAME, default=DEFAULT_SENSOR_NAME): cv.string,
        vol.Required(CONF_DEVICE_NAME): cv.string,
        vol.Required(CONF_API_KEY): cv.string,
    }
)


class HydropFlowHandler(ConfigFlow, domain=DOMAIN):
    """Config flow for Hydrop."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle a flow initialized by the user."""
        errors = {}

        if user_input is not None:
            device_name = user_input[CONF_DEVICE_NAME]
            api_key = user_input[CONF_API_KEY]

            # Validate credentials by making a test API request
            valid = await self._test_credentials(device_name, api_key)

            if valid:
                await self.async_set_unique_id(device_name)
                self._abort_if_unique_id_configured()

                return self.async_create_entry(
                    title=user_input[CONF_SENSOR_NAME],
                    data=user_input,
                )
            errors["base"] = "cannot_connect"

        return self.async_show_form(
            step_id="user",
            data_schema=SCHEMA_DEVICE,
            errors=errors,
        )

    async def _test_credentials(self, device_name: str, api_key: str) -> bool:
        """Test if the provided credentials are valid."""
        url = API_BASE_URL.format(device_name=device_name)
        try:
            async with aiohttp.ClientSession() as session, session.get(
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
        except aiohttp.ClientError as err:
            _LOGGER.error("Error connecting to Hydrop API: %s", err)
            return False
