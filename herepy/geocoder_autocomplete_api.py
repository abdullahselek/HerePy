#!/usr/bin/env python

from __future__ import division

import sys
import json
import requests

from herepy.here_api import HEREApi
from herepy.utils import Utils
from herepy.error import HEREError
from herepy.models import GeocoderAutoCompleteResponse

class GeocoderAutoCompleteApi(HEREApi):
    """A python interface into the HERE Geocoder Auto Complete API"""

    def __init__(self,
                 app_id=None,
                 app_code=None,
                 timeout=None):
        """Return a GeocoderAutoCompleteApi instance.
        Args:
          app_id (string): App Id taken from HERE Developer Portal.
          app_code (string): App Code taken from HERE Developer Portal.
          timeout (int): Timeout limit for requests.
        """

        super(GeocoderAutoCompleteApi, self).__init__(app_id, app_code, timeout)
        self._base_url = 'https://autocomplete.geocoder.cit.api.here.com/6.2/suggest.json'

    def __get(self, data):
        url = Utils.build_url(self._base_url, extra_params=data)
        response = requests.get(url, timeout=self._timeout)
        json_data = json.loads(response.content.decode('utf8'))
        if json_data.get('suggestions') != None:
            return GeocoderAutoCompleteResponse.new_from_jsondict(json_data)
        else:
            return HEREError(json_data.get('error_description', 'Error occured on ' + sys._getframe(1).f_code.co_name))

    def address_suggestion(self, query, prox, radius):
        """Request a list of suggested addresses found within a specified area
        Args:
          prox (array): array including latitude and longitude in order.
          radius (int): Radius in meters
        Returns:
          GeocoderAutoCompleteApi or HEREError instance"""

        data = {'query': query,
                'prox': str.format('{0},{1},{2}', prox[0], prox[1], radius),
                'app_id': self._app_id,
                'app_code': self._app_code}
        return self.__get(data)

    def limit_results_byaddress(self, query, country_code):
        """Request a list of suggested addresses within a single country
        Args:
          query (string): Query search string
          countryCode (string): Country code (USA etc.)
        Returns:
          GeocoderAutoCompleteApi or HEREError instance"""

        data = {'query': query,
                'country': country_code,
                'app_id': self._app_id,
                'app_code': self._app_code}
        return self.__get(data)

    def highlighting_matches(self, query, begin_highlight, end_highlight):
        """Request an annotated list of suggested addresses with matching tokens highlighted
        Args:
          query (string): Query search string
          begin_highlight (string): Mark the beginning of match in a token
          end_highlight (string): Mark the end of match in a token
        Returns:
          GeocoderAutoCompleteApi or HEREError instance"""

        data = {'query': query,
                'beginHighlight': begin_highlight,
                'endHighlight': end_highlight,
                'app_id': self._app_id,
                'app_code': self._app_code}
        return self.__get(data)
