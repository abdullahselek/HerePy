#!/usr/bin/env python

from __future__ import division

import sys
import json
import requests

from herepy.here_api import HEREApi
from herepy.utils import Utils
from herepy.error import HEREError
from herepy.models import PublicTransitResponse
from herepy.here_enum import PublicTransitSearchMethod

class PublicTransitApi(HEREApi):
    """A python interface into the HERE Public Transit API"""

    def __init__(self,
                 app_id=None,
                 app_code=None,
                 timeout=None):
        """Return a PublicTransitApi instance.
        Args:
          app_id (string): App Id taken from HERE Developer Portal.
          app_code (string): App Code taken from HERE Developer Portal.
          timeout (int): Timeout limit for requests.
        """

        super(PublicTransitApi, self).__init__(app_id, app_code, timeout)
        self._base_url = 'https://cit.transit.api.here.com/v3/stations/'

    def __get(self, data, path, json_node):
        url = Utils.build_url(self._base_url + path, extra_params=data)
        response = requests.get(url, timeout=self._timeout)
        json_data = json.loads(response.content.decode('utf8'))
        if json_node in json_data.get('Res', {}):
            return PublicTransitResponse.new_from_jsondict(json_data)
        elif 'text' in json_data.get('Res', {}).get('Message', {}):
            return HEREError(json_data['Res']['Message']['text'], 'Error occured on ' + sys._getframe(1).f_code.co_name)
        else:
            return HEREError('Error occured on ' + sys._getframe(1).f_code.co_name)

    def find_stations_by_name(self,
                              center,
                              name,
                              max=5,
                              method=PublicTransitSearchMethod.fuzzy,
                              radius=20000):
        """Request a list of public transit stations based on name.
        Args:
          center (array): array including latitude and longitude in order.
          name (string): station name.
          max (int): maximum number of stations  (Default is 5).
          method (enum): Matching method from PublicTransitSearchMethod (Default is fuzzy).
          radius (int): array including latitude and longitude in order (Default is 20000km).
        """

        data = {'center': str.format('{0},{1}', center[0], center[1]),
                'name':  name,
                'app_id': self._app_id,
                'app_code': self._app_code,
                'max': max,
                'method': method.__str__(),
                'radius': radius}
        return self.__get(data, 'by_name.json', 'Stations')

    def find_stations_nearby(self, center, radius=500, max=5):
        """Request a list of public transit stations within a given geo-location.
        Args:
          center (array): array including latitude and longitude in order.
          radius (int): array including latitude and longitude in order (Default is 500m).
          max (int): maximum number of stations  (Default is 5).
        """

        data = {'center': str.format('{0},{1}', center[0], center[1]),
                'radius': radius,
                'app_id': self._app_id,
                'app_code': self._app_code,
                'max': max}
        return self.__get(data, 'by_geocoord.json', 'Stations')
