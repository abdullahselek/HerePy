#!/usr/bin/env python

import sys
import json
import requests

from typing import List, Optional
from herepy.here_api import HEREApi
from herepy.utils import Utils
from herepy import MapImageResourceType
from herepy.error import HEREError, InvalidRequestError, UnauthorizedError


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

    def __get_error_from_response(self, json_data):
        if "error" in json_data:
            error_description = json_data["error_description"]
            if json_data["error"] == "Unauthorized":
                return UnauthorizedError(error_description)
        error_type = json_data.get("Type")
        error_message = json_data.get(
            "Message",
            error_description + ", error occured on " + sys._getframe(1).f_code.co_name,
        )
        if error_type == "Invalid Request":
            return InvalidRequestError(error_message)
        else:
            return HEREError(error_message)

    def get_mapimage(
        self,
        coordinates: List[float],
        zoom: int = 8,
        map_scheme: Optional[int] = None,
        uncertainty: Optional[str] = None,
    ):
        """Retrieves the map image with given parameters.
        Args:
          coordinates (List):
            List contains latitude and longitude in order.
          zoom (int):
            Zoom level for the map image.
          map_scheme (Optional[int]):
            Determines the map scheme to use for the map image.
          uncertainty (Optional[str]):
            The parameter u specifies position uncertainty, which is shown as a filled circle around a
            location defined in terms of its latitude and longitude. The value of the parameter u indicates
            the radius of the circle representing uncertainty. In this case, the radius is set to 5 myriameters,
            which is 50000 meters.
        Returns:
          Map image as bytes.
        """
        data = {
            "c": str.format("{0},{1}", coordinates[0], coordinates[1]),
            "z": zoom,
            "apiKey": self._api_key,
        }
        if map_scheme:
            data["t"] = map_scheme
        if uncertainty:
            data["u"] = uncertainty
        url = Utils.build_url(self._base_url, extra_params=data)
        response = requests.get(url, timeout=self._timeout)
        if isinstance(response.content, bytes):
            try:
                json_data = json.loads(response.content.decode("utf8"))
                if "error" in json_data:
                    error = self.__get_error_from_response(json_data)
                    raise error
            except UnicodeDecodeError as err:
                print("Map image downloaded")
        return response.content
