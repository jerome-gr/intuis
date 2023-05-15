"""Sample API Client."""
from __future__ import annotations

import base64
import pyatmo


from .thermostat import IntuisRadiatorStatus, IntuisHome
from .const import BASE_URL, USER_PREFIX, SCOPE


class IntuisApi:
    """Intuis API Client."""

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        username: str,
        password: str,
    ) -> None:
        """Init API Client."""
        self._client_id = base64.b64decode(client_id)
        self._client_secret = base64.b64decode(client_secret)
        self._username = username
        self._password = password
        self._client = None

    def connect(self) -> any:
        """Connect to API."""
        if self._client is None:
            self._client = pyatmo.ClientAuth(
                self._client_id,
                self._client_secret,
                self._username,
                self._password,
                SCOPE,
                USER_PREFIX,
                BASE_URL,
            )
        return self._client

    def get_homes(self) -> any:
        """Retrieve homes."""
        self.connect()
        homes = IntuisHome(self._client)
        homes.update()
        return homes

    def get_radiator_status(self, home_id) -> any:
        """Retrieve radiator statuses."""
        self.connect()
        status = IntuisRadiatorStatus(self._client, home_id)
        status.update()
        return status

    def refresh_tokens(self) -> any:
        """Refresh token."""
        return self._client.refresh_tokens()
