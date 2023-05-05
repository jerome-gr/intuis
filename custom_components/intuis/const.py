"""Constants for intuis."""
from logging import Logger, getLogger

LOGGER: Logger = getLogger(__package__)

NAME = "Intuis (ex Intuitiv Muller)"
DOMAIN = "intuis"
ATTRIBUTION = "Data provided by Intuis API"

BASE_URL = "https://app.muller-intuitiv.net/"
USER_PREFIX = "muller"
SCOPE = ["read_muller", "write_muller"]
CLIENT_ID = "NTllNjA0OTQ4ZmUyODNmZDRkYzdlMzU1"
CLIENT_SECRET = "ckFlV3U4WTNZcVhFUHFSSjRCcEZ6Rkc5OE1SWHBDY3o="
