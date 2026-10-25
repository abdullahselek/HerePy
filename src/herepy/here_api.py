#!/usr/bin/env python
"""Base classes shared by HERE API clients."""


class HEREApi:
    """Base class from which all wrappers inherit."""

    def __init__(self, api_key: str = None, timeout: int = None):
        """
        Initialize the API client.

        Args:
          api_key (str):
            API key taken from HERE Developer Portal.
          timeout (int):
            Timeout limit for requests.

        """
        self.__set_credentials(api_key)
        if timeout:
            self._timeout = timeout
        else:
            self._timeout = 20

    def __set_credentials(self, api_key):
        """
        Setter for credentials.

        Args:
          api_key (str):
            API key taken from HERE Developer Portal.

        """
        self._api_key = api_key
