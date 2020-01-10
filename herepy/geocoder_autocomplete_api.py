#!/usr/bin/env python

import sys
import json
import requests

from herepy.here_api import HEREApi
from herepy.utils import Utils
from herepy.error import HEREError
from herepy.models import GeocoderAutoCompleteResponse
from typing import List

class GeocoderAutoCompleteApi(HEREApi):
    """A python interface into the HERE Geocoder Auto Complete API"""

    def __init__(self,
                 api_key: str=None,
                 timeout: int=None):
        """Returns a GeocoderAutoCompleteApi instance.
        Args:
          api_key (str):
            API key taken from HERE Developer Portal.
          timeout (int):
            Timeout limit for requests.
        """

        super(GeocoderAutoCompleteApi, self).__init__(api_key, timeout)
        self._base_url = 'http://autocomplete.geocoder.ls.hereapi.com/6.2/suggest.json'

    def __get(self, data):
        url = Utils.build_url(self._base_url, extra_params=data)
        response = requests.get(url, timeout=self._timeout)
        json_data = json.loads(response.content.decode('utf8'))
        if json_data.get('suggestions') != None:
            return GeocoderAutoCompleteResponse.new_from_jsondict(json_data)
        else:
            raise HEREError(json_data.get('error_description', 'Error occured on ' + sys._getframe(1).f_code.co_name))

    def address_suggestion(self, query: str, prox: List[float], radius: int):
        """Request a list of suggested addresses found within a specified area
        Args:
          query (str):
            Query search string
          prox (array):
            Array including latitude and longitude in order.
          radius (int):
            Radius in meters
        Returns:
          GeocoderAutoCompleteApi
        Raises:
          HEREError"""

        data = {'query': query,
                'prox': str.format('{0},{1},{2}', prox[0], prox[1], radius),
                'apikey': self._api_key}
        return self.__get(data)

    def limit_results_byaddress(self, query: str, country_code: str):
        """Request a list of suggested addresses within a single country
        Args:
          query (str):
            Query search string
          countryCode (str):
            Country code (USA etc.)
        Returns:
          GeocoderAutoCompleteApi
        Raises:
          HEREError"""

        data = {'query': query,
                'country': country_code,
                'apikey': self._api_key}
        return self.__get(data)

    def highlighting_matches(self, query: str, begin_highlight: str, end_highlight: str):
        """Request an annotated list of suggested addresses with matching tokens highlighted
        Args:
          query (str):
            Query search string
          begin_highlight (str):
            Mark the beginning of match in a token
          end_highlight (str):
            Mark the end of match in a token
        Returns:
          GeocoderAutoCompleteApi
        Raises:
          HEREError"""

        data = {'query': query,
                'beginHighlight': begin_highlight,
                'endHighlight': end_highlight,
                'apikey': self._api_key}
        return self.__get(data)
