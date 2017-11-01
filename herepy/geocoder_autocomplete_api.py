#!/usr/bin/env python

from __future__ import division

import json
import requests
import io
import warnings
import sys

from herepy.utils import Utils
from herepy.error import HEREError
from herepy.models import GeocoderAutoCompleteResponse

class GeocoderAutoCompleteApi(object):
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
        self.SetCredentials(app_id, app_code)
        self._baseUrl = 'https://autocomplete.geocoder.cit.api.here.com/6.2/suggest.json'
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

    def AddressSuggestion(self, prox, radius):
        """Request a list of suggested addresses found within a specified area
        Args:
          prox (array): array including latitude and longitude in order.
          radius (int): Radius in meters
        Returns:
          GeocoderAutoCompleteApi or HEREError instance"""

        data = {'query': 'High',
                'prox': str.format('{0},{1},{2}', prox[0], prox[1], radius),
                'app_id': self._app_id,
                'app_code': self._app_code}
        url = Utils.BuildUrl(self._baseUrl, extra_params=data)
        response = requests.get(url, timeout=self._timeout)
        jsonData = json.loads(response.content.decode('utf8'))
        if jsonData.get('suggestions') != None:
            return GeocoderAutoCompleteResponse.NewFromJsonDict(jsonData)
        else:
            return HEREError(jsonData.get('error_description', 'Error occured on AddressSuggestion'))
