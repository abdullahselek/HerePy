#!/usr/bin/env python

from __future__ import division

import json
import requests
import io
import warnings
import sys

try:
    # python 3
    from urllib.parse import urlparse, urlunparse, urlencode
except ImportError:
    from urlparse import urlparse, urlunparse
    from urllib import urlencode

from herepy.error import (
    HEREError
)

from herepy.models import (
    GeocoderResponse
)

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

    @staticmethod
    def EncodeParameters(parameters):
        """Return a string in key=value&key=value form.
        Values of None are not included in the output string.
        Args:
          parameters (dict): dictionary of query parameters to be converted.
        Returns:
          A URL-encoded string in "key=value&key=value" form
        """
        if parameters is None:
            return None
        if not isinstance(parameters, dict):
            raise HEREError("`parameters` must be a dict.")
        else:
            return urlencode(dict((k, v) for k, v in parameters.items() if v is not None))

    def BuildUrl(self, url, extra_params=None):
        """Builds a url with given parameters which will
        be used in requests.
        Args:
          url (string): base url.
          extra_params (dict): dictionary of query parameters.
        Returns:
          A encoded url ready for the request"""

        # Break url into constituent parts
        (scheme, netloc, path, params, query, fragment) = urlparse(url)

        # Add any additional query parameters to the query string
        if extra_params and len(extra_params) > 0:
            extra_query = self.EncodeParameters(extra_params)
            # Add it to the existing query
            if query:
                query += '&' + extra_query
            else:
                query = extra_query

        # Return the rebuilt URL
        return urlunparse((scheme, netloc, path, params, query, fragment))

    def FreeForm(self, searchtext):
        """Geocodes given search text
        Args:
          searchtext (string): possible address text.
        Returns:
          GeocoderResponse instance"""

        data = {'searchtext': searchtext, 'app_id': self._app_id, 'app_code': self._app_code}
        url = self.BuildUrl(self._baseUrl, extra_params=data)
        response = requests.get(url, timeout=self._timeout)
        return GeocoderResponse.NewFromJsonDict(json.loads(response.content.decode('utf8')))

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
        url = self.BuildUrl(self._baseUrl, extra_params=data)
        response = requests.get(url, timeout=self._timeout)
        return GeocoderResponse.NewFromJsonDict(json.loads(response.content.decode('utf8')))

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
        url = self.BuildUrl(self._baseUrl, extra_params=data)
        response = requests.get(url, timeout=self._timeout)
        return GeocoderResponse.NewFromJsonDict(json.loads(response.content.decode('utf8')))

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
        url = self.BuildUrl(self._baseUrl, extra_params=data)
        response = requests.get(url, timeout=self._timeout)
        return GeocoderResponse.NewFromJsonDict(json.loads(response.content.decode('utf8')))
