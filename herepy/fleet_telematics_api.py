#!/usr/bin/env python

import sys
import json
import requests

from typing import List, Optional

from herepy.here_api import HEREApi
from herepy.here_enum import RouteMode, MultiplePickupOfferType
from herepy.utils import Utils
from herepy.models import WaypointSequenceResponse
from herepy.error import HEREError


class FleetTelematicsApi(HEREApi):
    """A python interface into the HERE Fleet Telematics API"""

    def __init__(self, api_key: str = None, timeout: int = None):
        """Returns a FleetTelematicsApi instance.
        Args:
          api_key (str):
            API key taken from HERE Developer Portal.
          timeout (int):
            Timeout limit for requests.
        Returns:
          FleetTelematicsApi instance.
        """

        super(FleetTelematicsApi, self).__init__(api_key, timeout)
        self._base_url = "https://wse.ls.hereapi.com/2/"

    def __create_find_sequence_parameters(
        self,
        start: str,
        departure: str,
        intermediate_destinations: List[str],
        end: str,
        modes: List[RouteMode],
    ):
        data = {
            "apiKey": self._api_key,
            "start": start.__str__(),
            "departure": departure,
        }

        count = 0
        for destination_param in intermediate_destinations:
            count += 1
            data[str.format("destination{0}", count)] = destination_param

        data["end"] = end
        data["improveFor"] = "time"
        data["departure"] = "now"

        modes_str = ""
        for route_mode in modes:
            modes_str += route_mode.__str__() + ";"

        data["mode"] = modes_str
        return data

    def __create_find_pickup_parameters(
        self,
        modes: List[RouteMode],
        start: str,
        departure: str,
        capacity: int,
        vehicle_cost: float,
        driver_cost: int,
        max_detour: int,
        rest_times: str,
        end: str,
        intermediate_destinations: List[str],
    ):
        data = {}

        modes_str = ""
        for route_mode in modes:
            modes_str += route_mode.__str__() + ";"
        modes_str = modes_str[:-1]
        data["mode"] = modes_str
        data["start"] = "waypoint0;" + start
        data["departure"] = departure
        data["capacity"] = capacity
        data["vehicleCost"] = vehicle_cost
        data["driverCost"] = driver_cost
        data["maxDetour"] = max_detour
        data["restTimes"] = rest_times

        count = 0
        for destination_pickup_param in intermediate_destinations:
            data[str.format("destination{0}", count)] = (
                str.format("waypoint{0};", count + 1) + destination_pickup_param
            )
            count += 1

        data["end"] = str.format("waypoint{0};{1}", count + 1, end)
        return data

    def __get(self, base_url, data, response_cls):
        url = Utils.build_url(base_url, extra_params=data)
        response = requests.get(url, timeout=self._timeout)
        json_data = json.loads(response.content.decode("utf8"))
        if json_data.get("results") is not None:
            return response_cls.new_from_jsondict(json_data)
        else:
            raise error_from_fleet_telematics_service_error(json_data)

    def find_sequence(
        self,
        start: str,
        departure: str,
        intermediate_destinations: List[str],
        end: str,
        modes: List[RouteMode],
    ) -> Optional[WaypointSequenceResponse]:
        """Finds time-optimized waypoint sequence route.
        Args:
          start (str):
            Starting point. `str.format('{0};{1},{2}', text, latitude, longitude)`
          departure (str):
            Time when travel is expected to start. The format is as xsd type xs:datetime `[-]CCYY-MM-DDThh:mm:ss[Z|(+|-)hh:mm]`
          intermediate_destinations (List[str]):
            Intermediate points between start and end points. List of `str.format('{0};{1},{2}', text, latitude, longitude)`.
          end (str):
            End point. `str.format('{0};{1},{2}', text, latitude, longitude)`
          modes (List[RouteMode]):
            Route modes.
        Returns:
          WaypointSequenceResponse
        Raises:
          HEREError
        """

        data = self.__create_find_sequence_parameters(
            start=start,
            departure=departure,
            intermediate_destinations=intermediate_destinations,
            end=end,
            modes=modes,
        )
        response = self.__get(
            self._base_url + "findsequence.json", data, WaypointSequenceResponse
        )
        return response

    def find_pickups(
        self,
        modes: List[RouteMode],
        start: str,
        departure: str,
        capacity: int,
        vehicle_cost: float,
        driver_cost: int,
        max_detour: int,
        rest_times: str,
        intermediate_destinations: List[str],
        end: str,
    ) -> Optional[WaypointSequenceResponse]:
        """Finds cheaper route by picking up some additional goods along the route.
        Args:
          modes (List[RouteMode]):
            Route modes.
          start (str):
            Starting point. `str.format('{0};{1},{2}', text, latitude, longitude)`
          departure (str):
            Time when travel is expected to start. The format is as xsd type xs:datetime `[-]CCYY-MM-DDThh:mm:ss[Z|(+|-)hh:mm]`
          capacity (int):
            Amount of payload the vehicle including trailers can carry, volume and/or weight.
            No unit is specified, but the value must be in the same unit as the waypoint pickup load values.
          vehicle_cost (float):
            Cost per kilometer. No currency is specified, but the value must be in the same currency as the driverCost and
            the waypoint drop-off values.
          driver_cost (int):
            Cost per hour. No currency is specified, but the value must be in the same currency as the vehicleCost and
            the waypoint drop-off values.
          max_detour (int):
            Overall maximum additional seconds spent to pickup and drop-off items along the route, compared to the time
            without picking up anything.
          rest_times (str):
            The parameter restTimes can be set to
            `disabled`
               rest times are not considered. This is equivalent to omitting the parameter restTimes
            `default`
               Use internal default. The default are simplified European rules: After 4.5h driving 45min rest and after 9h driving 11h rest.
            `durations:...` and `serviceTimes:...`
               You can provide values for driving and rest periods and define if service times at waypoints can be used for resting. You must provide both parameters.
          intermediate_destinations (List[DestinationPickupParam]):
            Intermediate destinations, at least one. If no end parameter is provided, one of these values is
            selected as end of the sequence.
            `str.format('{0},{1};{2}:{3},value:{4}', latitude,
                  longitude, param_type,
                  item, value)`
            or
            `str.format('{0},{1};{2}:{3}', latitude, longitude,
                  param_type, item)`
          end (str):
            End of the journey. `str.format('{0};{1},{2}', text, latitude, longitude)`
        Returns:
          WaypointSequenceResponse
        Raises:
          HEREError
        """

        data = self.__create_find_pickup_parameters(
            modes=modes,
            start=start,
            departure=departure,
            capacity=capacity,
            vehicle_cost=vehicle_cost,
            driver_cost=driver_cost,
            max_detour=max_detour,
            rest_times=rest_times,
            intermediate_destinations=intermediate_destinations,
            end=end,
        )
        response = self.__get(
            self._base_url + "findpickups.json", data, WaypointSequenceResponse
        )
        return response


class UnauthorizedError(HEREError):

    """Unauthorized Error Type.
    This error is returned if the specified token was invalid or no contract
    could be found for this token.
    """


def error_from_fleet_telematics_service_error(json_data: dict):
    """Return the correct subclass for sequence errors"""

    if "error" in json_data:
        error_type = json_data["error"]
        message = json_data["error_description"]

        if error_type == "Unauthorized":
            return UnauthorizedError(message)
    # pylint: disable=W0212
    return HEREError("Error occurred on " + sys._getframe(1).f_code.co_name)
