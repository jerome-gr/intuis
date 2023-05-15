"""Sensor platform for intuis."""
from __future__ import annotations

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription
from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorStateClass,
)
from homeassistant.core import callback
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from homeassistant.const import TEMP_CELSIUS
from .const import DOMAIN, NAME
from .coordinator import IntuisDataUpdateCoordinator

ENTITY_DESCRIPTIONS = (
    SensorEntityDescription(
        key="intuis",
        name="Intuis Sensor",
        icon="mdi:format-quote-close",
    ),
)


async def async_setup_entry(hass, entry, async_add_devices):
    """Set up the sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    if coordinator.data is not None:
        devices = []
        for key in coordinator.data:
            device = coordinator.data[key]
            devices.append(
                IntuisTempSensor(
                    coordinator,
                    device.id,
                    device.name,
                    device.temp,
                    device.firmware,
                )
            )
        async_add_devices(devices)


class IntuisTempSensor(SensorEntity, CoordinatorEntity):
    """Intuis radiator Sensor."""

    _attr_native_unit_of_measurement = TEMP_CELSIUS
    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(
        self,
        coordinator: IntuisDataUpdateCoordinator,
        unique_id: str,
        name: str,
        temp: str,
        firmware: str,
    ) -> None:
        """Init temp Sensor."""
        super().__init__(coordinator)
        self._attr_unique_id = unique_id
        self._attr_name = name
        self._attr_native_value = temp
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self.unique_id)},
            name=f"{DOMAIN} ({self.name})",
            model=firmware,
            manufacturer=NAME,
        )

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._attr_native_value = self.coordinator.data[self._attr_unique_id].temp
        self.async_write_ha_state()

    @property
    def native_value(self) -> str:
        """Return the native value of the sensor."""
        return self._attr_native_value
