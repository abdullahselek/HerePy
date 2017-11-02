#!/usr/bin/env python

from __future__ import division

import sys
import json
import requests

from herepy.here_api import HEREApi
from herepy.utils import Utils
from herepy.error import HEREError
from herepy.models import GeocoderResponse

class GeocoderApi(HEREApi):
    """A python interface into the HERE Geocoder API"""

    def __init__(self,
                 app_id=None,
                 app_code=None,
                 timeout=None):
        """Return a GeocoderApi instance.
        Args:
          app_id (string): App Id taken from HERE Developer Portal.
          app_code (string): App Code taken from HERE Developer Portal.
          timeout (int): Timeout limit for requests.
        """

        super(GeocoderApi, self).__init__(app_id, app_code, timeout)
        self._base_url = 'https://geocoder.cit.api.here.com/6.2/geocode.json'

    def __get(self, data):
        url = Utils.build_url(self._base_url, extra_params=data)
        response = requests.get(url, timeout=self._timeout)
        try:
            json_data = json.loads(response.content.decode('utf8'))
            if json_data.get('Response') != None:
                return GeocoderResponse.new_from_jsondict(json_data)
            else:
                return HEREError(json_data.get('Details', 'Error occured on function ' + sys._getframe(1).f_code.co_name))
        except ValueError as err:
            return HEREError('Error occured on function ' + sys._getframe(1).f_code.co_name + ' ' + str(err))

    def free_form(self, searchtext):
        """Geocodes given search text
        Args:
          searchtext (string): possible address text.
        Returns:
          GeocoderResponse or HEREError instance"""

        data = {'searchtext': searchtext, 'app_id': self._app_id, 'app_code': self._app_code}
        return self.__get(data)

    def address_with_boundingbox(self, searchtext, top_left, bottom_right):
        """Geocodes given search text with in given boundingbox
        Args:
          searchtext (string): possible address text.
          top_left (array): array including latitude and longitude in order.
          bottom_right (array): array including latitude and longitude in order.
        Returns:
          GeocoderResponse or HEREError instance"""

        data = {'searchtext': searchtext,
                'mapview': str.format('{0},{1};{2},{3}', top_left[0], top_left[1], bottom_right[0], bottom_right[1]),
                'app_id': self._app_id,
                'app_code': self._app_code}
        return self.__get(data)

    def address_with_details(self,
                             house_number,
                             street,
                             city,
                             country):
        """Geocodes with given address details
        Args:
          house_number (int): house number.
          street (string): street name.
          city (string): city name.
          country (string): country name.
        Returns:
          GeocoderResponse or HEREError instance"""

        data = {'housenumber': house_number,
                'street': street,
                'city': city,
                'country': country,
                'app_id': self._app_id,
                'app_code': self._app_code}
        return self.__get(data)

    def street_intersection(self,
                            street,
                            city):
        """Geocodes with given street and city
        Args:
          street (string): street name.
          city (string): city name.
        Returns:
          GeocoderResponse or HEREError instance"""

        data = {'street': street,
                'city': city,
                'app_id': self._app_id,
                'app_code': self._app_code}
        return self.__get(data)
