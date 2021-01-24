#!/usr/bin/env python

import sys
import json
import requests

from herepy.here_api import HEREApi


class MapTileApi(HEREApi):
    """A python interface into the HERE Map Tile API"""

    def __init__(self, api_key: str = None, timeout: int = None):
        """Returns a MapTileApi instance.
        Args:
          api_key (str):
            API key taken from HERE Developer Portal.
          timeout (int):
            Timeout limit for requests.
        """

        super(MapTileApi, self).__init__(api_key, timeout)
        self._base_url = "https://2.base.maps.ls.hereapi.com/maptile/2.1/"
