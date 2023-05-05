"""Thermostat class for intuis."""
from pyatmo import HomeStatus, HomeData
from pyatmo.exceptions import InvalidHome


class IntuisHome(HomeData):
    """Home class for intuis."""

    def get_module(self, home_id: str, room_id: str) -> dict:
        """Return thermostat data for a given room id."""
        if home_id not in self.modules:
            raise InvalidHome(f"{home_id} is not a valid home id")

        for value in self.modules[home_id].values():
            if value["id"] == room_id:
                return value


class IntuisRadiatorStatus(HomeStatus):
    """Thermostat class for intuis."""

    def process(self) -> None:
        super().process()
        for module in self.raw_data.get("modules", []):
            if module["type"] in {"NMH"}:
                self.thermostats[module["id"]] = module

    def open_window(self, room_id: str) -> bool | None:
        """Return the window open detection of a given room."""
        return self.get_room(room_id).get("open_window")

    def presence(self, room_id: str) -> bool | None:
        """Return the presence of a given room."""
        return self.get_room(room_id).get("presence")
