#!/usr/bin/env python

import sys
import json
import requests

from herepy.here_api import HEREApi


class VectorTileApi(HEREApi):
    """A python interface into the HERE Vector Tile API"""

    def __init__(self, api_key: str = None, timeout: int = None):
        """Returns a VectorTileApi instance.
        Args:
          api_key (str):
            API key taken from HERE Developer Portal.
          timeout (int):
            Timeout limit for requests.
        """

        super(VectorTileApi, self).__init__(api_key, timeout)
        self._base_url = "https://vector.hereapi.com/v2/vectortiles/"
