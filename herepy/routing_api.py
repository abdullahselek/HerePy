#!/usr/bin/env python

from __future__ import division

import sys
import json
import requests

from herepy.here_api import HEREApi
from herepy.utils import Utils
from herepy.error import HEREError
from herepy.models import RoutingResponse
from herepy.here_enum import RouteMode

class RoutingApi(HEREApi):
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

        super(RoutingApi, self).__init__(app_id, app_code, timeout)
        self._base_url = 'https://route.cit.api.here.com/routing/7.2/calculateroute.json'

    def __get(self, data):
        url = Utils.build_url(self._base_url, extra_params=data)
        response = requests.get(url, timeout=self._timeout)
        json_data = json.loads(response.content.decode('utf8'))
        if json_data.get('response') != None:
            return RoutingResponse.new_from_jsondict(json_data)
        else:
            return HEREError(json_data.get('details', 'Error occured on ' + sys._getframe(1).f_code.co_name))

    @classmethod
    def __prepare_mode_values(cls, modes):
        mode_values = ""
        for mode in modes:
            mode_values += mode.__str__() + ';'
        mode_values = mode_values[:-1]
        return mode_values

    def car_route(self,
                  waypoint_a,
                  waypoint_b,
                  modes=None):
        """Request a driving route between two points
        Args:
          waypoint_a (array): array including latitude and longitude in order.
          waypoint_b (array): array including latitude and longitude in order.
          modes (array): array including RouteMode enums.
        Returns:
          RoutingResponse instance or HEREError"""

        if modes is None:
            modes = [RouteMode.car, RouteMode.fastest]

        data = {'waypoint0': str.format('{0},{1}', waypoint_a[0], waypoint_a[1]),
                'waypoint1': str.format('{0},{1}', waypoint_b[0], waypoint_b[1]),
                'mode':  self.__prepare_mode_values(modes),
                'app_id': self._app_id,
                'app_code': self._app_code,
                'departure': 'now'}
        return self.__get(data)

    def pedastrian_route(self,
                         waypoint_a,
                         waypoint_b,
                         modes=None):
        """Request a pedastrian route between two points
        Args:
          waypoint_a (array): array including latitude and longitude in order.
          waypoint_b (array): array including latitude and longitude in order.
          modes (array): array including RouteMode enums.
        Returns:
          RoutingResponse instance or HEREError"""

        if modes is None:
            modes = [RouteMode.pedestrian, RouteMode.fastest]

        data = {'waypoint0': str.format('{0},{1}', waypoint_a[0], waypoint_a[1]),
                'waypoint1': str.format('{0},{1}', waypoint_b[0], waypoint_b[1]),
                'mode':  self.__prepare_mode_values(modes),
                'app_id': self._app_id,
                'app_code': self._app_code}
        return self.__get(data)

    def intermediate_route(self,
                           waypoint_a,
                           waypoint_b,
                           waypoint_c,
                           modes=None):
        """Request a intermediate route from three points
        Args:
          waypoint_a (array): Starting array including latitude and longitude in order.
          waypoint_b (array): Intermediate array including latitude and longitude in order.
          waypoint_c (array): Last array including latitude and longitude in order.
          modes (array): array including RouteMode enums.
        Returns:
          RoutingResponse instance or HEREError"""

        if modes is None:
            modes = [RouteMode.car, RouteMode.fastest]

        data = {'waypoint0': str.format('{0},{1}', waypoint_a[0], waypoint_a[1]),
                'waypoint1': str.format('{0},{1}', waypoint_b[0], waypoint_b[1]),
                'waypoint2': str.format('{0},{1}', waypoint_c[0], waypoint_c[1]),
                'mode':  self.__prepare_mode_values(modes),
                'app_id': self._app_id,
                'app_code': self._app_code}
        return self.__get(data)

    def public_transport(self,
                         waypoint_a,
                         waypoint_b,
                         combine_change,
                         modes=None):
        """Request a public transport route between two points
        Args:
          waypoint_a (array): Starting array including latitude and longitude in order.
          waypoint_b (array): Intermediate array including latitude and longitude in order.
          combine_change (bool): Enables the change manuever in the route response, which
            indicates a public transit line change.
          modes (array): array including RouteMode enums.
        Returns:
          RoutingResponse instance or HEREError"""

        if modes is None:
            modes = [RouteMode.publicTransport, RouteMode.fastest]

        data = {'waypoint0': str.format('{0},{1}', waypoint_a[0], waypoint_a[1]),
                'waypoint1': str.format('{0},{1}', waypoint_b[0], waypoint_b[1]),
                'mode':  self.__prepare_mode_values(modes),
                'combine_change': 'true' if combine_change == True else 'false',
                'app_id': self._app_id,
                'app_code': self._app_code}
        return self.__get(data)

    def location_near_motorway(self,
                               waypoint_a,
                               waypoint_b,
                               modes=None):
        """Calculates the fastest car route between two location
        Args:
          waypoint_a (array): array including latitude and longitude in order.
          waypoint_b (array): array including latitude and longitude in order.
          modes (array): array including RouteMode enums.
        Returns:
          RoutingResponse instance or HEREError"""

        if modes is None:
            modes = [RouteMode.car, RouteMode.fastest]

        data = {'waypoint0': str.format('{0},{1}', waypoint_a[0], waypoint_a[1]),
                'waypoint1': str.format('street!!{0},{1}', waypoint_b[0], waypoint_b[1]),
                'mode':  self.__prepare_mode_values(modes),
                'app_id': self._app_id,
                'app_code': self._app_code}
        return self.__get(data)

    def truck_route(self,
                    waypoint_a,
                    waypoint_b,
                    modes=None):
        """Calculates the fastest truck route between two location
        Args:
          waypoint_a (array): array including latitude and longitude in order.
          waypoint_b (array): array including latitude and longitude in order.
          modes (array): array including RouteMode enums.
        Returns:
          RoutingResponse instance or HEREError"""

        if modes is None:
            modes = [RouteMode.truck, RouteMode.fastest]

        data = {'waypoint0': str.format('{0},{1}', waypoint_a[0], waypoint_a[1]),
                'waypoint1': str.format('{0},{1}', waypoint_b[0], waypoint_b[1]),
                'mode':  self.__prepare_mode_values(modes),
                'app_id': self._app_id,
                'app_code': self._app_code}
        return self.__get(data)
