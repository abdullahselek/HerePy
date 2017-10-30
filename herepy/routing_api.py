#!/usr/bin/env python

from __future__ import division

import json
import requests
import io
import warnings
import sys

from herepy.utils import Utils
from herepy.error import HEREError
from herepy.models import RoutingResponse

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
          modes (array): array including RouteMode enums.
        Returns:
          RoutingResponse instance or HEREError"""

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
        url = Utils.BuildUrl(self._baseUrl, extra_params=data)
        response = requests.get(url, timeout=self._timeout)
        jsonData = json.loads(response.content.decode('utf8'))
        if jsonData.get('response') != None:
            return RoutingResponse.NewFromJsonDict(jsonData)
        else:
            return HEREError(jsonData.get('details', 'Error occured on CarRoute'))

    def PedastrianRoute(self, 
                        waypoint_a, 
                        waypoint_b, 
                        modes):
        """Request a pedastrian route between two points
        Args:
          waypoint_a (array): array including latitude and longitude in order.
          waypoint_b (array): array including latitude and longitude in order.
          modes (array): array including RouteMode enums.
        Returns:
          RoutingResponse instance or HEREError"""

        mode_values = ""
        for m in modes:
            mode_values += m.__str__() + ';'
        mode_values = mode_values[:-1]
        data = {'waypoint0': str.format('{0},{1}', waypoint_a[0], waypoint_a[1]),
                'waypoint1': str.format('{0},{1}', waypoint_b[0], waypoint_b[1]),
                'mode': mode_values,
                'app_id': self._app_id,
                'app_code': self._app_code}
        url = Utils.BuildUrl(self._baseUrl, extra_params=data)
        response = requests.get(url, timeout=self._timeout)
        jsonData = json.loads(response.content.decode('utf8'))
        if jsonData.get('response') != None:
            return RoutingResponse.NewFromJsonDict(jsonData)
        else:
            return HEREError(jsonData.get('details', 'Error occured on PedastrianRoute'))

    def IntermediateRoute(self,
                          waypoint_a,
                          waypoint_b,
                          waypoint_c,
                          modes):
        """Request a intermediate route from three points
        Args:
          waypoint_a (array): Starting array including latitude and longitude in order.
          waypoint_b (array): Intermediate array including latitude and longitude in order.
          waypoint_c (array): Last array including latitude and longitude in order.
          modes (array): array including RouteMode enums.
        Returns:
          RoutingResponse instance or HEREError"""

        mode_values = ""
        for m in modes:
            mode_values += m.__str__() + ';'
        mode_values = mode_values[:-1]
        data = {'waypoint0': str.format('{0},{1}', waypoint_a[0], waypoint_a[1]),
                'waypoint1': str.format('{0},{1}', waypoint_b[0], waypoint_b[1]),
                'waypoint2': str.format('{0},{1}', waypoint_c[0], waypoint_c[1]),
                'mode': mode_values,
                'app_id': self._app_id,
                'app_code': self._app_code}
        url = Utils.BuildUrl(self._baseUrl, extra_params=data)
        response = requests.get(url, timeout=self._timeout)
        jsonData = json.loads(response.content.decode('utf8'))
        if jsonData.get('response') != None:
            return RoutingResponse.NewFromJsonDict(jsonData)
        else:
            return HEREError(jsonData.get('details', 'Error occured on IntermediateRoute'))

    def PublicTransport(self,
                        waypoint_a,
                        waypoint_b,
                        modes,
                        combine_change):
        """Request a public transport route between two points
        Args:
          waypoint_a (array): Starting array including latitude and longitude in order.
          waypoint_b (array): Intermediate array including latitude and longitude in order.
          modes (array): array including RouteMode enums.
          combine_change (bool): Enables the change manuever in the route response, which
            indicates a public transit line change.
        Returns:
          RoutingResponse instance or HEREError"""

        mode_values = ""
        for m in modes:
            mode_values += m.__str__() + ';'
        mode_values = mode_values[:-1]
        data = {'waypoint0': str.format('{0},{1}', waypoint_a[0], waypoint_a[1]),
                'waypoint1': str.format('{0},{1}', waypoint_b[0], waypoint_b[1]),
                'mode': mode_values,
                'combine_change': 'true' if combine_change == True else 'false',
                'app_id': self._app_id,
                'app_code': self._app_code}
        url = Utils.BuildUrl(self._baseUrl, extra_params=data)
        response = requests.get(url, timeout=self._timeout)
        jsonData = json.loads(response.content.decode('utf8'))
        if jsonData.get('response') != None:
            return RoutingResponse.NewFromJsonDict(jsonData)
        else:
            return HEREError(jsonData.get('details', 'Error occured on IntermediateRoute'))

    def LocationNearMotorway(self,
                             waypoint_a,
                             waypoint_b,
                             modes):
        """Calculates the fastest car route between two location
        Args:
          waypoint_a (array): array including latitude and longitude in order.
          waypoint_b (array): array including latitude and longitude in order.
          modes (array): array including RouteMode enums.
        Returns:
          RoutingResponse instance or HEREError"""

        mode_values = ""
        for m in modes:
            mode_values += m.__str__() + ';'
        mode_values = mode_values[:-1]
        data = {'waypoint0': str.format('{0},{1}', waypoint_a[0], waypoint_a[1]),
                'waypoint1': str.format('street!!{0},{1}', waypoint_b[0], waypoint_b[1]),
                'mode': mode_values,
                'app_id': self._app_id,
                'app_code': self._app_code}
        url = Utils.BuildUrl(self._baseUrl, extra_params=data)
        response = requests.get(url, timeout=self._timeout)
        jsonData = json.loads(response.content.decode('utf8'))
        if jsonData.get('response') != None:
            return RoutingResponse.NewFromJsonDict(jsonData)
        else:
            return HEREError(jsonData.get('details', 'Error occured on LocationNearMotorway'))
