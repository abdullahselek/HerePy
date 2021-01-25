#!/usr/bin/env python

import sys
import json
import requests

from random import randrange
from herepy.here_api import HEREApi
from herepy import MapTileApiType


class MapTileApi(HEREApi):
    """A python interface into the HERE Map Tile API"""

    def __init__(self, api_key: str = None, api_type: MapTileApiType = MapTileApiType.base, timeout: int = None):
        """Returns a MapTileApi instance.
        Args:
          api_key (str):
            API key taken from HERE Developer Portal.
          api_type (MapTileApiType):
            Type of tile used in changing base url.
          timeout (int):
            Timeout limit for requests.
        """

        super(MapTileApi, self).__init__(api_key, timeout)
        server = randrange(1, 4)
        self._base_url = str.format("https://{}.{}.maps.ls.hereapi.com/maptile/2.1/", server, api_type.__str__())

