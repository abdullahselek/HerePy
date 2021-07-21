#!/usr/bin/env python

import sys
import json
import requests

from random import randrange
from typing import Dict, Optional
from herepy.here_api import HEREApi
from herepy.utils import Utils
from herepy import (
    MercatorProjection,
    MapTileApiType,
    MapTileResourceType,
    BaseMapTileResourceType,
    AerialMapTileResourceType,
    TrafficMapTileResourceType,
)
from herepy.error import HEREError, InvalidRequestError, UnauthorizedError


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
        self._base_url = None

    def __get_error_from_response(self, json_data):
        if "error" in json_data:
            if json_data["error"] == "Unauthorized":
                return UnauthorizedError(json_data["error_description"])
        error_type = json_data.get("Type")
        error_message = json_data.get(
            "Message", "Error occurred on " + sys._getframe(1).f_code.co_name
        )
        if error_type == "Invalid Request":
            return InvalidRequestError(error_message)
        else:
            return HEREError(error_message)

    def get_maptile(
        self,
        latitude: float,
        longitude: float,
        zoom: int,
        api_type: MapTileApiType = MapTileApiType.base,
        resource_type: MapTileResourceType = BaseMapTileResourceType.alabeltile,
        map_id: str = "newest",
        scheme: str = "normal.day",
        size: int = 256,
        tile_format: str = "png8",
        query_parameters: Optional[Dict] = None,
    ) -> Optional[bytes]:
        """Returns optional bytes value of map tile with given parameters.
        Args:
          latitude (float):
            Latitude value to be used to fetch map tile.
          longitude (float):
            Longitude value to be used to fetch map tile.
          zoom (int):
            Zoom level of the map image.
          api_type (MapTileApiType):
            MapTileApiType used to generate url.
          resource_type (MapTileResourceType):
            Resource type to download map tile.
          map_id (str):
            Specifies the map version, either newest or with a hash value.
            https://developer.here.com/documentation/map-tile/dev_guide/topics/map-versions.html
          scheme (str):
            Specifies the view scheme. A complete list of the supported schemes may be obtained
            by using the https://developer.here.com/documentation/map-tile/dev_guide/topics/resource-info.html
            resource.
          size (int):
            Returned image size. The following sizes ([width, height]) are supported:
            256 = [256, 256]
            512 = [512, 512]
            The following sizes ([width, height]) are deprecated, although usage is still accepted:
            128 = [128, 128]
          tile_format (str):
            Returned image format. The following image formats are supported:
            png – PNG format, 24 bit, RGB
            png8 – PNG format, 8 bit, indexed color
            jpg – JPG format at 90% quality
            Please note that JPG is recommended for satellite and hybrid schemes only.
          query_parameters (Optional[Dict]):
            Optional Query Parameters. Refer to the API definition for values.
        Returns:
          Map tile as bytes.
        Raises:
          HEREError
        """

        server = randrange(1, 4)
        column, row = MercatorProjection.get_column_row(
            latitude=latitude, longitude=longitude, zoom=zoom
        )
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
        if isinstance(response.content, bytes):
            try:
                json_data = json.loads(response.content.decode("utf8"))
                if "error" in json_data:
                    error = self.__get_error_from_response(json_data)
                    raise error
            except UnicodeDecodeError as err:
                print("Map tile downloaded")
        return response.content
