#!/usr/bin/env python

class HEREApi(object):
    """ Base class from which all wrappers inherit."""

    def __init__(self,
                 api_key: str=None,
                 timeout: int=None):
        """Returns a Api instance.
        Args:
          app_id (str):
            App Id taken from HERE Developer Portal.
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

    def __set_credentials(self,
                          api_key):
        """Setter for credentials.
        Args:
          api_key (str):
            API key taken from HERE Developer Portal.
        """
        self._api_key = api_key
