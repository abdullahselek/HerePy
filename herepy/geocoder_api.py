#!/usr/bin/env python

from __future__ import division

import json
import requests
import io
import warnings
import sys

from herepy.utils import Utils
from herepy.error import HEREError
from herepy.models import GeocoderResponse

class GeocoderApi(object):
    """A python interface into the HERE Geocoder API"""

    _API_REALM = 'HERE Geocoder API'

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
        self.SetCredentials(app_id, app_code)
        self._baseUrl = 'https://geocoder.cit.api.here.com/6.2/geocode.json'
        if timeout:
            self._timeout = timeout
        else:
            self._timeout = 20

    def SetCredentials(self, 
                       app_id, 
                       app_code):
        """Setter for credentials.
        Args:
          app_id (string): App Id taken from HERE Developer Portal.
          app_code (string): App Code taken from HERE Developer Portal.
        """
        self._app_id = app_id
        self._app_code = app_code

    def FreeForm(self, searchtext):
        """Geocodes given search text
        Args:
          searchtext (string): possible address text.
        Returns:
          GeocoderResponse instance"""

        data = {'searchtext': searchtext, 'app_id': self._app_id, 'app_code': self._app_code}
        url = Utils.BuildUrl(self._baseUrl, extra_params=data)
        response = requests.get(url, timeout=self._timeout)
        jsonData = json.loads(response.content.decode('utf8'))
        if jsonData.get('Response') != None:
            return GeocoderResponse.NewFromJsonDict(jsonData)
        else:
            return HEREError(jsonData.get('Details', 'Error occured on FreeForm'))

    def AddressWithBoundingBox(self, searchtext, top_left, bottom_right):
        """Geocodes given search text with in given boundingbox
        Args:
          searchtext (string): possible address text.
          top_left (array): array including latitude and longitude in order.
          bottom_right (array): array including latitude and longitude in order.
        Returns:
          GeocoderResponse instance"""

        data = {'searchtext': searchtext,
                'mapview': str.format('{0},{1};{2},{3}', top_left[0], top_left[1], bottom_right[0], bottom_right[1]),
                'app_id': self._app_id,
                'app_code': self._app_code}
        url = Utils.BuildUrl(self._baseUrl, extra_params=data)
        response = requests.get(url, timeout=self._timeout)
        jsonData = json.loads(response.content.decode('utf8'))
        if jsonData.get('Response') != None:
            return GeocoderResponse.NewFromJsonDict(jsonData)
        else:
            return HEREError(jsonData.get('Details', 'Error occured on AddressWithBoundingBox'))

    def AddressWithDetails(self,
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
          GeocoderResponse instance"""

        data = {'housenumber': house_number,
                'street': street,
                'city': city,
                'country': country,
                'app_id': self._app_id,
                'app_code': self._app_code}
        url = Utils.BuildUrl(self._baseUrl, extra_params=data)
        response = requests.get(url, timeout=self._timeout)
        jsonData = json.loads(response.content.decode('utf8'))
        if jsonData.get('Response') != None:
            return GeocoderResponse.NewFromJsonDict(jsonData)
        else:
            return HEREError(jsonData.get('Details', 'Error occured on AddressWithDetails'))

    def StreetIntersection(self,
                           street,
                           city):
        """Geocodes with given street and city
        Args:
          street (string): street name.
          city (string): city name.
        Returns:
          GeocoderResponse instance"""

        data = {'street': street,
                'city': city,
                'app_id': self._app_id,
                'app_code': self._app_code}
        url = Utils.BuildUrl(self._baseUrl, extra_params=data)
        response = requests.get(url, timeout=self._timeout)
        jsonData = json.loads(response.content.decode('utf8'))
        if jsonData.get('Response') != None:
            return GeocoderResponse.NewFromJsonDict(jsonData)
        else:
            return HEREError(jsonData.get('Details', 'Error occured on StreetIntersection'))
