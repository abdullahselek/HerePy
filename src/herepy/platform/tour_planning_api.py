"""Client for the HERE Tour Planning API."""

from herepy.here_api import HEREApi


class TourPlanningApi(HEREApi):
    """A python interface into the HERE Tour Planning API."""

    def __init__(self, api_key: str = None, timeout: int = None):
        """
        Initialize the Tour Planning API client.

        Args:
          api_key (str):
            API key taken from HERE Developer Portal.
          timeout (int):
            Timeout limit for requests.

        """
        super().__init__(api_key, timeout)
        self._base_url = "https://tourplanning.hereapi.com/v3/"
