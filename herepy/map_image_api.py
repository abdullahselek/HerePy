#!/usr/bin/env python

import sys
import json
import requests

from herepy.here_api import HEREApi


class MapImageApi(HEREApi):
    """A python interface into the HERE Map Image API"""

    def __init__(self, api_key: str = None, timeout: int = None):
        """Returns a MapImageApi instance.
        Args:
          api_key (str):
            API key taken from HERE Developer Portal.
          timeout (int):
            Timeout limit for requests.
        """

        super(MapImageApi, self).__init__(api_key, timeout)
        self._base_url = "https://image.maps.ls.hereapi.com/mia/1.6/mapview"
