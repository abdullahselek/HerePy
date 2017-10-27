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

from herepy.utils import Utils

from herepy.error import (
    HEREError
)

from herepy.models import (
    RoutingResponse
)

class RoutingApi(object):
    """A python interface into the HERE Routing API"""

    def __init__(self,
                 app_id=None,
                 app_code=None,
                 timeout=None):
        """Returns a RoutingApi instance.
        Args:
          app_id (string): App Id taken from HERE Developer Portal.
          app_code (string): App Code taken from HERE Developer Portal.
          timeout (int): Timeout limit for requests.
        """
        self.SetCredentials(app_id, app_code)
        self._baseUrl = 'https://route.cit.api.here.com/routing/7.2/calculateroute.json'
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

    def CarRoute(self, 
                 waypoint_a, 
                 waypoint_b, 
                 modes):
        """Request a driving route between two points
        Args:
          waypoint_a (array): array including latitude and longitude in order.
          waypoint_b (array): array including latitude and longitude in order.
          mode (array): array including RouteMode enums.
        Returns:
          RoutingResponse instance"""

        mode_values = ""
        for m in modes:
            mode_values += m.__str__() + ';'
        mode_values = mode_values[:-1]
        data = {'waypoint0': str.format('{0},{1}', waypoint_a[0], waypoint_a[1]),
                'waypoint1': str.format('{0},{1}', waypoint_b[0], waypoint_b[1]),
                'mode': mode_values,
                'app_id': self._app_id,
                'app_code': self._app_code,
                'departure': 'now'}
        response = requests.get(self._baseUrl, timeout=self._timeout)
        return RoutingResponse.NewFromJsonDict(json.loads(response.content.decode('utf8')))

    def PedastrianRoute(self, 
                        waypoint_a, 
                        waypoint_b, 
                        modes):
        """Request a pedastrian route between two points
        Args:
          waypoint_a (array): array including latitude and longitude in order.
          waypoint_b (array): array including latitude and longitude in order.
          mode (array): array including RouteMode enums.
        Returns:
          RoutingResponse instance"""

        mode_values = ""
        for m in modes:
            mode_values += m.__str__() + ';'
        mode_values = mode_values[:-1]
        data = {'waypoint0': str.format('{0},{1}', waypoint_a[0], waypoint_a[1]),
                'waypoint1': str.format('{0},{1}', waypoint_b[0], waypoint_b[1]),
                'mode': mode_values,
                'app_id': self._app_id,
                'app_code': self._app_code}
        response = requests.get(self._baseUrl, timeout=self._timeout)
        return RoutingResponse.NewFromJsonDict(json.loads(response.content.decode('utf8')))
