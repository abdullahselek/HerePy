#!/usr/bin/env python

from herepy.here_api import HEREApi


class IsolineRoutingApi(HEREApi):
    """A python interface into the HERE Isoline Routing API"""

    def __init__(self, api_key: str = None, timeout: int = None):
        """Returns a IsolineRoutingApi instance.
        Args:
          api_key (str):
            API key taken from HERE Developer Portal.
          timeout (int):
            Timeout limit for requests.
        """

        super(IsolineRoutingApi, self).__init__(api_key, timeout)
        self._base_url = "https://isoline.router.hereapi.com/v8/isolines"
