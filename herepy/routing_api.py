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
          app_id (str):
            App Id taken from HERE Developer Portal.
          app_code (str):
            App Code taken from HERE Developer Portal.
          timeout (int):
            Timeout limit for requests.
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
            raise error_from_routing_service_error(json_data)

    @classmethod
    def __prepare_mode_values(cls, modes):
        mode_values = ""
        for mode in modes:
            mode_values += mode.__str__() + ';'
        mode_values = mode_values[:-1]
        return mode_values

    def _route(self, waypoint_a, waypoint_b, modes=None):
        data = {'waypoint0': str.format('{0},{1}', waypoint_a[0], waypoint_a[1]),
                'waypoint1': str.format('{0},{1}', waypoint_b[0], waypoint_b[1]),
                'mode': self.__prepare_mode_values(modes),
                'app_id': self._app_id,
                'app_code': self._app_code,
                'departure': 'now'}
        return self.__get(data)

    def car_route(self,
                  waypoint_a,
                  waypoint_b,
                  modes=None):
        """Request a driving route between two points
        Args:
          waypoint_a (array):
            array including latitude and longitude in order.
          waypoint_b (array):
            array including latitude and longitude in order.
          modes (array):
            array including RouteMode enums.
        Returns:
          RoutingResponse
        Raises:
          HEREError"""

        if modes is None:
            modes = [RouteMode.car, RouteMode.fastest]
        return self._route(waypoint_a, waypoint_b, modes)

    def pedastrian_route(self,
                         waypoint_a,
                         waypoint_b,
                         modes=None):
        """Request a pedastrian route between two points
        Args:
          waypoint_a (array):
            array including latitude and longitude in order.
          waypoint_b (array):
            array including latitude and longitude in order.
          modes (array):
            array including RouteMode enums.
        Returns:
          RoutingResponse
        Raises:
          HEREError"""

        if modes is None:
            modes = [RouteMode.pedestrian, RouteMode.fastest]
        return self._route(waypoint_a, waypoint_b, modes)

    def intermediate_route(self,
                           waypoint_a,
                           waypoint_b,
                           waypoint_c,
                           modes=None):
        """Request a intermediate route from three points
        Args:
          waypoint_a (array):
            Starting array including latitude and longitude in order.
          waypoint_b (array):
            Intermediate array including latitude and longitude in order.
          waypoint_c (array):
            Last array including latitude and longitude in order.
          modes (array):
            array including RouteMode enums.
        Returns:
          RoutingResponse
        Raises:
          HEREError"""

        if modes is None:
            modes = [RouteMode.car, RouteMode.fastest]
        return self._route(waypoint_a, waypoint_b, modes)

    def public_transport(self,
                         waypoint_a,
                         waypoint_b,
                         combine_change,
                         modes=None):
        """Request a public transport route between two points
        Args:
          waypoint_a (array):
            Starting array including latitude and longitude in order.
          waypoint_b (array):
            Intermediate array including latitude and longitude in order.
          combine_change (bool):
            Enables the change manuever in the route response, which
            indicates a public transit line change.
          modes (array):
            array including RouteMode enums.
        Returns:
          RoutingResponse
        Raises:
          HEREError"""

        if modes is None:
            modes = [RouteMode.publicTransport, RouteMode.fastest]
        return self._route(waypoint_a, waypoint_b, modes)

    def location_near_motorway(self,
                               waypoint_a,
                               waypoint_b,
                               modes=None):
        """Calculates the fastest car route between two location
        Args:
          waypoint_a (array):
            array including latitude and longitude in order.
          waypoint_b (array):
            array including latitude and longitude in order.
          modes (array):
            array including RouteMode enums.
        Returns:
          RoutingResponse
        Raises:
          HEREError"""

        if modes is None:
            modes = [RouteMode.car, RouteMode.fastest]
        return self._route(waypoint_a, waypoint_b, modes)

    def truck_route(self,
                    waypoint_a,
                    waypoint_b,
                    modes=None):
        """Calculates the fastest truck route between two location
        Args:
          waypoint_a (array):
            array including latitude and longitude in order.
          waypoint_b (array):
            array including latitude and longitude in order.
          modes (array):
            array including RouteMode enums.
        Returns:
          RoutingResponse
        Raises:
          HEREError"""

        if modes is None:
            modes = [RouteMode.truck, RouteMode.fastest]
        return self._route(waypoint_a, waypoint_b, modes)



class InvalidCredentialsError(HEREError):

    """Invalid Credentials Error Type.

    This error is returned if the specified token was invalid or no contract
    could be found for this token.
    """


class InvalidInputDataError(HEREError):

    """Invalid Input Data Error Type.

    This error is returned if the specified request parameters contain invalid
    data, such as due to wrong parameter syntax or invalid parameter
    combinations.
    """


class WaypointNotFoundError(HEREError):

    """Waypoint not found Error Type.

    This error indicates that one of the requested waypoints
    (start/end or via point) could not be found in the routing network.
    """


class NoRouteFoundError(HEREError):

    """No Route Found Error Type.

    This error indicates that no route could be constructed based on the input
    parameter.
    """


class LinkIdNotFoundError(HEREError):

    """Link Not Found Error Type.

    This error indicates that a link ID passed as input parameter could not be
    found in the underlying map data.
    """


class RouteNotReconstructedError(HEREError):

    """Route Not Reconstructed Error Type.

    This error indicates that the RouteId is invalid (RouteId can not be
    decoded into valid data) or route failed to be reconstructed from the
    RouteId. In every case a mitigation is to re-run CalculateRoute request to
    acquire a new proper RouteId.
    """

# pylint: disable=R0911
def error_from_routing_service_error(json_data):
    """Return the correct subclass for routing errors"""
    if 'subtype' in json_data:
        subtype = json_data['subtype']
        details = json_data['details']

        if subtype == 'InvalidCredentials':
            return InvalidCredentialsError(details)
        if subtype == 'InvalidInputData':
            return InvalidInputDataError(details)
        if subtype == 'WaypointNotFound':
            return WaypointNotFoundError(details)
        if subtype == 'NoRouteFound':
            return NoRouteFoundError(details)
        if subtype == 'LinkIdNotFound':
            return LinkIdNotFoundError(details)
        if subtype == 'RouteNotReconstructed':
            return RouteNotReconstructedError(details)
    # pylint: disable=W0212
    return HEREError('Error occured on ' + sys._getframe(1).f_code.co_name)
