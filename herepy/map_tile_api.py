#!/usr/bin/env python

import sys
import json
import requests

from random import randrange
from typing import Dict, Optional
from herepy.here_api import HEREApi
from herepy.utils import Utils
from herepy import (
    MapTileApiType,
    MapTileResourceType,
    BaseMapTileResourceType,
    AerialMapTileResourceType,
    TrafficMapTileResourceType,
)


class MapTileApi(HEREApi):
    """A python interface into the HERE Map Tile API"""

    def __init__(self, api_key: str = None, timeout: int = None):
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
        self._base_url = None

    def get_maptile(
        self,
        api_type: MapTileApiType = MapTileApiType.base,
        resource_type: MapTileResourceType = BaseMapTileResourceType.alabeltile,
        map_id: str = "newest",
        scheme: str = "normal.day",
        zoom: int = 13,
        column: int = 4400,
        row: int = 2686,
        size: int = 256,
        tile_format: str = "png8",
        query_parameters: Optional[Dict] = None,
    ) -> Optional[bytes]:
        server = randrange(1, 4)
        url = str.format(
            "https://{}.{}.maps.ls.hereapi.com/maptile/2.1/{}/{}/{}/{}/{}/{}/{}/{}",
            server,
            api_type.__str__(),
            resource_type.__str__(),
            map_id,
            scheme,
            zoom,
            column,
            row,
            size,
            tile_format,
        )
        if query_parameters:
            query_parameters.update({"apiKey": self._api_key})
        else:
            query_parameters = {"apiKey": self._api_key}
        url = Utils.build_url(url, extra_params=query_parameters)
        response = requests.get(url, timeout=self._timeout, stream=True)
        return response.content
