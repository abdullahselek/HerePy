#!/usr/bin/env python

import sys
import json
import requests

from herepy.here_api import HEREApi
from herepy.utils import Utils
from herepy.error import HEREError
from herepy.models import GeocoderResponse
from typing import List, Optional


class GeocoderApi(HEREApi):
    """A python interface into the HERE Geocoder API"""

    def __init__(self, api_key: str = None, timeout: int = None):
        """Returns a GeocoderApi instance.
        Args:
          api_key (str):
            API key taken from HERE Developer Portal.
          timeout (int):
            Timeout limit for requests.
        """

        super(GeocoderApi, self).__init__(api_key, timeout)
        self._base_url = "https://geocode.search.hereapi.com/v1/geocode"

    def __get(self, data):
        url = Utils.build_url(self._base_url, extra_params=data)
        response = requests.get(url, timeout=self._timeout)
        try:
            json_data = json.loads(response.content.decode("utf8"))
            if json_data.get("items") != None:
                return GeocoderResponse.new_from_jsondict(json_data)
            else:
                raise HEREError(
                    json_data.get(
                        "Details",
                        "Error occurred on function " + sys._getframe(1).f_code.co_name,
                    )
                )
        except ValueError as err:
            raise HEREError(
                "Error occurred on function "
                + sys._getframe(1).f_code.co_name
                + " "
                + str(err)
            )

    def free_form(
        self, searchtext: str, lang: str = "en-US"
    ) -> Optional[GeocoderResponse]:
        """Geocodes given search text
        Args:
          searchtext (str):
            possible address text.
          lang (str):
            BCP47 compliant Language Code.
        Returns:
          GeocoderResponse
        Raises:
          HEREError"""

        data = {"q": searchtext, "apiKey": self._api_key, "lang": lang}
        return self.__get(data)

    def address_with_boundingbox(
        self,
        searchtext: str,
        top_left: List[float],
        bottom_right: List[float],
        lang: str = "en-US",
    ) -> Optional[GeocoderResponse]:
        """Geocodes given search text with in given boundingbox
        Args:
          searchtext (str):
            possible address text.
          top_left (List):
            List contains latitude and longitude in order.
          bottom_right (List):
            List contains latitude and longitude in order.
          lang (str):
            BCP47 compliant Language Code.
        Returns:
          GeocoderResponse
        Raises:
          HEREError"""

        data = {
            "q": searchtext,
            "mapView": str.format(
                "{0},{1};{2},{3}",
                top_left[0],
                top_left[1],
                bottom_right[0],
                bottom_right[1],
            ),
            "apiKey": self._api_key,
            "lang": lang,
        }
        return self.__get(data)

    def address_with_details(
        self,
        house_number: int,
        street: str,
        city: str,
        country: str,
        lang: str = "en-US",
    ) -> Optional[GeocoderResponse]:
        """Geocodes with given address details
        Args:
          house_number (int):
            house number.
          street (str):
            street name.
          city (str):
            city name.
          country (str):
            country name.
          lang (str):
            BCP47 compliant Language Code.
        Returns:
          GeocoderResponse
        Raises:
          HEREError"""

        data = {
            "qq": str.format("houseNumber={0};", house_number)
            + str.format("street={0};", street)
            + str.format("city={0};", city)
            + str.format("country={0}", country),
            "apiKey": self._api_key,
            "lang": lang,
        }
        return self.__get(data)

    def street_intersection(
        self, street: str, city: str, lang: str = "en-US"
    ) -> Optional[GeocoderResponse]:
        """Geocodes with given street and city
        Args:
          street (str):
            street name.
          city (str):
            city name.
          lang (str):
            BCP47 compliant Language Code.
        Returns:
          GeocoderResponse
        Raises:
          HEREError"""

        data = {
            "qq": str.format("street={0};", street) + str.format("city={0}", city),
            "apiKey": self._api_key,
            "lang": lang,
        }
        return self.__get(data)
