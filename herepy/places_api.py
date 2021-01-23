#!/usr/bin/env python

import sys
import json
import requests

from herepy.here_api import HEREApi
from herepy.utils import Utils
from herepy.error import HEREError, UnauthorizedError
from herepy.models import PlacesResponse
from herepy.here_enum import PlacesCategory
from typing import List, Optional


class PlacesApi(HEREApi):
    """A python interface into the HERE Places (Search) API"""

    def __init__(self, api_key: str = None, timeout: int = None):
        """Returns a PlacesApi instance.
        Args:
          api_key (str):
            API key taken from HERE Developer Portal.
          timeout (int):
            Timeout limit for requests.
        """

        super(PlacesApi, self).__init__(api_key, timeout)
        self._base_url = "https://discover.search.hereapi.com/v1/discover"

    def __get(self, data):
        url = Utils.build_url(self._base_url, extra_params=data)
        response = requests.get(url, timeout=self._timeout)
        json_data = json.loads(response.content.decode("utf8"))
        if json_data.get("items") != None:
            return PlacesResponse.new_from_jsondict(json_data)
        elif "error" in json_data:
            if json_data["error"] == "Unauthorized":
                raise UnauthorizedError(json_data["error_description"])
        else:
            raise HEREError(
                json_data.get(
                    "message", "Error occured on " + sys._getframe(1).f_code.co_name
                )
            )

    def onebox_search(
        self, coordinates: List[float], query: str, limit: int = 20, lang: str = "en-US"
    ) -> Optional[PlacesResponse]:
        """Request a list of places based on a query string.
        Args:
          coordinates (List):
            List contains latitude and longitude in order.
          query (str):
            search term.
          limit (int):
            Limits items to return, with default value 10. Max value 100.
          lang (str):
            BCP47 compliant Language Code.
        Returns:
          PlacesResponse
        Raises:
          HEREError"""

        data = {
            "at": str.format("{0},{1}", coordinates[0], coordinates[1]),
            "q": query,
            "limit": limit,
            "lang": lang,
            "apiKey": self._api_key,
        }
        return self.__get(data)

    def search_in_country(
        self,
        coordinates: List[float],
        query: str,
        country_code: str,
        limit: int = 20,
        lang: str = "en-US",
    ) -> Optional[PlacesResponse]:
        """Request a list of places based on a query string.
        Args:
          coordinates (List):
            List contains latitude and longitude in order.
          query (str):
            search term.
          country_code (str):
            ISO 3166-1 alpha-3 country code.
          limit (int):
            Limits items to return. Max value 100.
          lang (str):
            BCP47 compliant Language Code
        Returns:
          PlacesResponse
        Raises:
          HEREError"""

        data = {
            "at": str.format("{0},{1}", coordinates[0], coordinates[1]),
            "q": query,
            "limit": limit,
            "in": "countryCode:" + country_code,
            "lang": lang,
            "apiKey": self._api_key,
        }
        return self.__get(data)

    def places_in_circle(
        self,
        coordinates: List[float],
        radius: int,
        query: str,
        limit: int = 20,
        lang: str = "en-US",
    ) -> Optional[PlacesResponse]:
        """Request a list of popular places around a location
        Args:
          coordinates (List):
            List contains latitude and longitude in order.
          radius (int):
            Circle radius (in meters).
          query (str):
            search term.
          lang (str):
            BCP47 compliant Language Code
        Returns:
          PlacesResponse
        Raises:
          HEREError"""

        data = {
            "in": str.format(
                "circle:{0},{1};r={2}", coordinates[0], coordinates[1], radius
            ),
            "q": query,
            "limit": limit,
            "lang": lang,
            "apiKey": self._api_key,
        }
        return self.__get(data)
