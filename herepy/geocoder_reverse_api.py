#!/usr/bin/env python

import sys
import json
import requests

from herepy.here_api import HEREApi
from herepy.utils import Utils
from herepy.error import HEREError, UnauthorizedError
from herepy.models import GeocoderReverseResponse
from typing import List, Optional


class GeocoderReverseApi(HEREApi):
    """A python interface into the HERE Geocoder Reverse API"""

    def __init__(self, api_key: str = None, timeout: int = None):
        """Returns a GeocoderApi instance.
        Args:
          api_key (str):
            API key taken from HERE Developer Portal.
          timeout (int):
            Timeout limit for requests.
        """

        super(GeocoderReverseApi, self).__init__(api_key, timeout)
        self._base_url = "https://revgeocode.search.hereapi.com/v1/revgeocode"

    def __get(self, data):
        url = Utils.build_url(self._base_url, extra_params=data)
        response = requests.get(url, timeout=self._timeout)
        try:
            json_data = json.loads(response.content.decode("utf8"))
            if json_data.get("items") != None:
                return GeocoderReverseResponse.new_from_jsondict(json_data)
            elif "error" in json_data:
                if json_data["error"] == "Unauthorized":
                    raise UnauthorizedError(json_data["error_description"])
            else:
                raise HEREError(
                    json_data.get(
                        "Details",
                        "Error occured on function " + sys._getframe(1).f_code.co_name,
                    )
                )
        except ValueError as err:
            raise HEREError(
                "Error occured on function "
                + sys._getframe(1).f_code.co_name
                + " "
                + str(err)
            )

    def retrieve_addresses(
        self, prox: List[float], limit: int = 1, lang: str = "en-US"
    ) -> Optional[GeocoderReverseResponse]:
        """Gets the address information of a point.
        Args:
          prox (lat/lon):
            latitude longitude of the point
          limit (int):
            Limits items to return, with default value 1. Max value 100.
          lang (str):
            BCP47 compliant Language Code.
        Returns:
          GeocoderReverseResponse
        Raises:
          HEREError"""

        data = {
            "at": str.format("{0},{1}", prox[0], prox[1]),
            "limit": limit,
            "lang": lang,
            "apiKey": self._api_key,
        }
        return self.__get(data)
