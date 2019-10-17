#!/usr/bin/env python

from __future__ import division

import sys
import json
import requests

from herepy.here_api import HEREApi
from herepy.utils import Utils
from herepy.error import HEREError
from herepy.models import RoutingResponse, RoutingMatrixResponse
from herepy.here_enum import RouteMode

class RoutingApi(HEREApi):
    """A python interface into the HERE Routing API"""

    URL_CALCULATE_ROUTE = 'https://route.cit.api.here.com/routing/7.2/calculateroute.json'
    URL_CALCULATE_MATRIX = 'https://matrix.route.api.here.com/routing/7.2/calculatematrix.json'

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

    def __get(self, base_url, data, response_cls):
        url = Utils.build_url(base_url, extra_params=data)
        response = requests.get(url, timeout=self._timeout)
        json_data = json.loads(response.content.decode('utf8'))
        if json_data.get('response') is not None:
            return response_cls.new_from_jsondict(json_data)
        else:
            raise error_from_routing_service_error(json_data)

    @classmethod
    def __prepare_mode_values(cls, modes):
        mode_values = ""
        for mode in modes:
            mode_values += mode.__str__() + ';'
        mode_values = mode_values[:-1]
        return mode_values

    @classmethod
    def __array_to_waypoint(cls, waypoint_a):
        return str.format('geo!{0},{1}', waypoint_a[0], waypoint_a[1])

    def _route(self, waypoint_a, waypoint_b, modes=None):
        data = {'waypoint0': self.__array_to_waypoint(waypoint_a),
                'waypoint1': self.__array_to_waypoint(waypoint_b),
                'mode': self.__prepare_mode_values(modes),
                'app_id': self._app_id,
                'app_code': self._app_code,
                'departure': 'now'}
        response = self.__get(self.URL_CALCULATE_ROUTE, data, RoutingResponse)
        route = response.response["route"]
        maneuver = route[0]["leg"][0]["maneuver"]

        if any(mode in modes for mode in [RouteMode.car, RouteMode.truck]):
            # Get Route for Car and Truck
            response.route_short = self._get_route_from_vehicle_maneuver(maneuver)
        elif any(mode in modes for mode in [RouteMode.publicTransport, RouteMode.publicTransportTimeTable]):
            # Get Route for Public Transport
            public_transport_line = route[0]["publicTransportLine"]
            response.route_short = self._get_route_from_public_transport_line(
                public_transport_line
            )
        elif any(mode in modes for mode in [RouteMode.pedestrian, RouteMode.bicycle]):
            # Get Route for Pedestrian and Biyclce
            response.route_short = self._get_route_from_non_vehicle_maneuver(maneuver)
        return response

    def bicycle_route(self,
                  waypoint_a,
                  waypoint_b,
                  modes=None):
        """Request a bicycle route between two points
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
            modes = [RouteMode.bicycle, RouteMode.fastest]
        return self._route(waypoint_a, waypoint_b, modes)

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

    def public_transport_timetable(self,
                         waypoint_a,
                         waypoint_b,
                         combine_change,
                         modes=None):
        """Request a public transport route between two points based on timetables
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
            modes = [RouteMode.publicTransportTimeTable, RouteMode.fastest]
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

    def matrix(self,
               start_waypoints,
               destination_waypoints,
               departure='now',
               modes=[]):
        """Request a matrix of route summaries between M starts and N destinations.
        Args:
          start_waypoints (array):
            array of arrays of coordinates [lat,long] of start waypoints.
          destination_waypoints (array):
            array of arrays of coordinates [lat,long] of destination waypoints.
          departure (str):
            time when travel is expected to start, e.g.: '2013-07-04T17:00:00+02'
          modes (array):
            array of RouteMode enums following [Type, TransportMode, TrafficMode, Feature].
        Returns:
          RoutingMatrixResponse
        Raises:
          HEREError: If an error is received from the server.
        """
        data = {
            'app_id': self._app_id,
            'app_code': self._app_code,
            'departure': departure,
            'mode': self.__prepare_mode_values(modes)
        }
        for i, start_waypoint in enumerate(start_waypoints):
            data['start' + str(i)] = self.__array_to_waypoint(start_waypoint)
        for i, destination_waypoint in enumerate(destination_waypoints):
            data['destination' + str(i)] = self.__array_to_waypoint(destination_waypoint)
        response = self.__get(self.URL_CALCULATE_MATRIX, data, RoutingMatrixResponse)
        return response

    @staticmethod
    def _get_route_from_non_vehicle_maneuver(maneuver):
        """Extract a short route description from the maneuver instructions."""
        road_names = []

        for step in maneuver:
            instruction = step["instruction"]
            try:
                road_name = instruction.split('<span class="next-street">')[1].split(
                    "</span>"
                )[0]
                road_name = road_name.replace("(", "").replace(")", "")

                # Only add if it does not repeat
                if not road_names or road_names[-1] != road_name:
                    road_names.append(road_name)
            except IndexError:
                pass  # No street name found in this maneuver step
        route = "; ".join(list(map(str, road_names)))
        return route

    @staticmethod
    def _get_route_from_public_transport_line(
        public_transport_line_segment
    ):
        """Extract a short route description from the public transport lines."""
        lines = []
        for line_info in public_transport_line_segment:
            lines.append(line_info["lineName"] + " - " + line_info["destination"])

        route = "; ".join(list(map(str, lines)))
        return route

    @staticmethod
    def _get_route_from_vehicle_maneuver(maneuver):
        """Extract a short route description from the maneuver instructions."""
        road_names = []

        for step in maneuver:
            instruction = step["instruction"]
            try:
                road_number = instruction.split('<span class="number">')[1].split(
                    "</span>"
                )[0]
                road_name = road_number.replace("(", "").replace(")", "")

                try:
                    street_name = instruction.split('<span class="next-street">')[
                        1
                    ].split("</span>")[0]
                    street_name = street_name.replace("(", "").replace(")", "")

                    road_name += " - " + street_name
                except IndexError:
                    pass  # No street name found in this maneuver step

                # Only add if it does not repeat
                if not road_names or road_names[-1] != road_name:
                    road_names.append(road_name)
            except IndexError:
                pass  # No road number found in this maneuver step

        route = "; ".join(list(map(str, road_names)))
        return route



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
