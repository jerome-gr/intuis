"""DataUpdateCoordinator for intuis."""
from __future__ import annotations

from datetime import timedelta
from dataclasses import dataclass

from oauthlib.oauth2.rfc6749.errors import InvalidClientError
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
)

from .api import (
    IntuisApi,
)
from .const import DOMAIN, LOGGER


# https://developers.home-assistant.io/docs/integration_fetching_data#coordinated-single-api-poll-for-data-for-all-entities
class IntuisDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the API."""

    config_entry: ConfigEntry
    _homes: None

    def __init__(
        self,
        hass: HomeAssistant,
        client: IntuisApi,
    ) -> None:
        """Initialize."""
        self.client = client
        self._hass = hass
        super().__init__(
            hass=hass,
            logger=LOGGER,
            name=DOMAIN,
            update_interval=timedelta(minutes=5),
        )

    async def _async_update_data(self):
        """Update data via library."""
        try:
            await self._hass.async_add_executor_job(self.client.connect)

            homes = await self.async_get_homes()

            devices = {}
            for key in homes.homes:
                statuses = await self.async_get_radiator_status(homes.homes[key]["id"])

                for room in homes.homes[key]["rooms"]:
                    for module in room["modules"]:
                        module_id = homes.get_module(key, module).get("id")

                        devices[module_id] = IntuisDevice(
                            module_id,
                            room["name"],
                            homes.get_module(key, module).get("name"),
                            statuses.measured_temperature(room["id"]),
                            statuses.get_thermostat(module_id).get(
                                "firmware_revision_thirdparty"
                            ),
                        )
            return devices
        except InvalidClientError as exception:
            LOGGER.error("Not authorized %s", exception)
        except Exception as exception:
            LOGGER.error(type(exception))
            LOGGER.error(exception)

    async def async_get_homes(self):
        """TODO"""
        return await self._hass.async_add_executor_job(self.client.get_homes)

    async def async_get_radiator_status(self, home_id):
        """TODO"""
        return await self._hass.async_add_executor_job(
            self.client.get_radiator_status, home_id
        )


@dataclass
class IntuisDevice:
    """TODO"""

    id: int
    room_name: str
    name: str
    temp: str
    firmware: str


@dataclass
class IntuisHome:
    """Netatmo home class."""

    id: int
    name: str
    devices: list
