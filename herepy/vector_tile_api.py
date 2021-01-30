#!/usr/bin/env python

import sys
import json
import requests

from typing import Optional, Dict
from herepy.here_api import HEREApi
from herepy.utils import Utils
from herepy import VectorMapTileLayer


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

    def get_vectortile(
        self,
        x: int,
        y: int,
        layer: VectorMapTileLayer = VectorMapTileLayer.base,
        projection: str = "mc",
        zoom: int = 11,
        tile_format: str = "omv",
        query_parameters: Optional[Dict] = None,
    ) -> Optional[bytes]:
        """Retrieves the protocol buffer encoded binary tile.
          x (int):
            Specifies the X coordinate index. This parameter is dependent upon the tile Zoom level.
          y (int):
            Specifies the Y coordinate index. This parameter is dependent upon the tile Zoom level.
          layer (VectorMapTileLayer):
            Specifies the layers available in the tile. The access to each layer is determined by the contract of the user.
          projection (str):
            Specifies the tile projection. mc - Mercator Projection.
          zoom (int):
            Specifies the tile Zoom level. Accepted values range from 0-17. minimum - 0, maximum - 17.
          tile_format (str):
            Specifies the tile format.
            omv - Optimized Map for Visualization (follows Map Vector Tile open specification).
          query_parameters (Optional[Dict]):
            Optional Query Parameter. Refer to the API definition for values.
        Returns:
          Vector tile as bytes.
        Raises:
          HEREError
        """

        url = str.format(
            self._base_url + "{}/{}/{}/{}/{}/{}",
            layer.__str__(),
            projection,
            zoom,
            x,
            y,
            tile_format,
        )
        if query_parameters:
            query_parameters.update({"apiKey": self._api_key})
        else:
            query_parameters = {"apiKey": self._api_key}
        url = Utils.build_url(url, extra_params=query_parameters)
        response = requests.get(url, timeout=self._timeout, stream=True)
        if isinstance(response.content, bytes):
            try:
                json_data = json.loads(response.content.decode("utf8"))
                if "error" in json_data:
                    error = self.__get_error_from_response(json_data)
                    raise error
            except UnicodeDecodeError as err:
                print("Vector tile downloaded")
        return response.content
