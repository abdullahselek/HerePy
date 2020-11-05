#!/usr/bin/env python

import sys
import json
import requests

from herepy.here_api import HEREApi
from herepy.utils import Utils
from herepy.error import HEREError
from herepy.models import GeocoderAutoCompleteResponse
from typing import List, Optional


class GeocoderAutoCompleteApi(HEREApi):
    """A python interface into the HERE Geocoder Auto Complete API"""

    def __init__(self, api_key: str = None, timeout: int = None):
        """Returns a GeocoderAutoCompleteApi instance.
        Args:
          api_key (str):
            API key taken from HERE Developer Portal.
          timeout (int):
            Timeout limit for requests.
        """

        super(GeocoderAutoCompleteApi, self).__init__(api_key, timeout)
        self._base_url = "https://autosuggest.search.hereapi.com/v1/autosuggest"

    def __get(self, data):
        url = Utils.build_url(self._base_url, extra_params=data)
        response = requests.get(url, timeout=self._timeout)
        json_data = json.loads(response.content.decode("utf8"))
        if json_data.get("items") != None:
            return GeocoderAutoCompleteResponse.new_from_jsondict(json_data)
        else:
            raise HEREError(
                json_data.get(
                    "error_description",
                    "Error occured on " + sys._getframe(1).f_code.co_name,
                )
            )

    def address_suggestion(
        self, query: str, prox: List[float], radius: int, lang: str = "en-US"
    ) -> Optional[GeocoderAutoCompleteResponse]:
        """Request a list of suggested addresses found within a specified area
        Args:
          query (str):
            Query search string
          prox (List):
            List contains latitude and longitude in order.
          radius (int):
            Radius in meters
          lang (str):
            BCP47 compliant Language Code.
        Returns:
          GeocoderAutoCompleteResponse
        Raises:
          HEREError"""

        data = {
            "q": query,
            "in": str.format("circle:{0},{1};r={2}", prox[0], prox[1], radius),
            "apikey": self._api_key,
            "lang": lang,
        }
        return self.__get(data)

    def limit_results_byaddress(
        self, query: str, country_code: str, lang: str = "en-US"
    ) -> Optional[GeocoderAutoCompleteResponse]:
        """Request a list of suggested addresses within a single country
        Args:
          query (str):
            Query search string
          countryCode (str):
            Country code (USA etc.)
          lang (str):
            BCP47 compliant Language Code.
        Returns:
          GeocoderAutoCompleteResponse
        Raises:
          HEREError"""

        data = {
            "q": query,
            "in": "countryCode:" + country_code,
            "apikey": self._api_key,
            "lang": lang,
        }
        return self.__get(data)
