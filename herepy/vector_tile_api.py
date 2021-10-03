#!/usr/bin/env python

import sys
import json
import requests

from typing import Optional, Dict
from herepy.here_api import HEREApi
from herepy.utils import Utils
from herepy import VectorMapTileLayer, MercatorProjection
from herepy.error import HEREError, InvalidRequestError, UnauthorizedError


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

    def __get_error_from_response(self, json_data):
        if "error" in json_data:
            error_description = json_data["error_description"]
            if json_data["error"] == "Unauthorized":
                return UnauthorizedError(error_description)
        error_type = json_data.get("Type")
        error_message = json_data.get(
            "Message",
            error_description
            + ", error occurred on "
            + sys._getframe(1).f_code.co_name,
        )
        if error_type == "Invalid Request":
            return InvalidRequestError(error_message)
        else:
            return HEREError(error_message)

    def get_vectortile(
        self,
        latitude: float,
        longitude: float,
        zoom: int,
        layer: VectorMapTileLayer = VectorMapTileLayer.base,
        projection: str = "mc",
        tile_format: str = "omv",
        query_parameters: Optional[Dict] = None,
        headers: Optional[Dict] = None,
    ) -> Optional[bytes]:
        """Retrieves the protocol buffer encoded binary tile.
        Args:
          latitude (float):
            Latitude value to be used to fetch map tile.
          longitude (float):
            Longitude value to be used to fetch map tile.
          zoom (int):
            Specifies the tile Zoom level. Accepted values range from 0-17. minimum - 0, maximum - 17.
          layer (VectorMapTileLayer):
            Specifies the layers available in the tile. The access to each layer is determined by the contract of the user.
          projection (str):
            Specifies the tile projection. mc - Mercator Projection.
          tile_format (str):
            Specifies the tile format.
            omv - Optimized Map for Visualization (follows Map Vector Tile open specification).
          query_parameters (Optional[Dict]):
            Optional Query Parameters. Refer to the API definition for values.
          headers (Optional[Dict]):
            Optional headers. Refer to the API definition for values.
        Returns:
          Vector tile as bytes.
        Raises:
          HEREError
        """

        column, row = MercatorProjection.get_column_row(
            latitude=latitude, longitude=longitude, zoom=zoom
        )
        url = str.format(
            self._base_url + "{}/{}/{}/{}/{}/{}",
            layer.__str__(),
            projection,
            zoom,
            column,
            row,
            tile_format,
        )
        if query_parameters:
            query_parameters.update({"apiKey": self._api_key})
        else:
            query_parameters = {"apiKey": self._api_key}
        url = Utils.build_url(url, extra_params=query_parameters)
        response = requests.get(
            url, headers=headers, timeout=self._timeout, stream=True
        )
        if isinstance(response.content, bytes):
            try:
                json_data = json.loads(response.content.decode("utf8"))
                if "error" in json_data:
                    error = self.__get_error_from_response(json_data)
                    raise error
            except UnicodeDecodeError as err:
                print("Vector tile downloaded")
        return response.content
