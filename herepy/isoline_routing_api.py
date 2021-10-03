#!/usr/bin/env python

import sys
import json
import requests

from typing import List, Optional
from herepy.here_api import HEREApi
from herepy.utils import Utils
from herepy.models import IsolineRoutingResponse
from herepy.error import HEREError, UnauthorizedError, InvalidRequestError
from herepy.here_enum import (
    IsolineRoutingTransportMode,
    IsolineRoutingMode,
    IsolineRoutingRangeType,
)


class IsolineRoutingApi(HEREApi):
    """A python interface into the HERE Isoline Routing API"""

    def __init__(self, api_key: str = None, timeout: int = None):
        """Returns a IsolineRoutingApi instance.
        Args:
          api_key (str):
            API key taken from HERE Developer Portal.
          timeout (int):
            Timeout limit for requests.
        """

        super(IsolineRoutingApi, self).__init__(api_key, timeout)
        self._base_url = "https://isoline.router.hereapi.com/v8/isolines"

    def __get_error_from_response(self, json_data):
        if "error" in json_data:
            if json_data["error"] == "Unauthorized":
                return UnauthorizedError(json_data["error_description"])
        error_type = json_data.get("Type")
        error_message = json_data.get(
            "Message", "Error occurred on " + sys._getframe(1).f_code.co_name
        )
        if error_type == "Invalid Request":
            return InvalidRequestError(error_message)
        else:
            return HEREError(error_message)

    def __get_client_error_from_response(self, json_data):
        if "title" in json_data and "cause" in json_data:
            return HEREError(
                "Error on client: "
                + json_data["title"]
                + " cause: "
                + json_data["cause"]
            )
        else:
            return HEREError("herepy got a 400 from isoline router API")

    def __get(self, url, data, json_key):
        url = Utils.build_url(url, extra_params=data)
        response = requests.get(url, timeout=self._timeout)
        json_data = json.loads(response.content.decode("utf8"))
        if json_data.get(json_key) != None and json_data.get("isolines") != None:
            return IsolineRoutingResponse.new_from_jsondict(
                json_data, param_defaults={json_key: None, "isolines": None}
            )
        elif response.status_code == 400:
            error = self.__get_client_error_from_response(json_data=json_data)
            raise error
        else:
            error = self.__get_error_from_response(json_data)
            raise error

    def distance_based_isoline(
        self,
        transport_mode: IsolineRoutingTransportMode,
        origin: List[float],
        ranges: List[int],
        routing_mode: IsolineRoutingMode,
    ) -> Optional[IsolineRoutingResponse]:
        """A distance-based isoline, also called an Isodistance,
        can be requested using range[type]=distance and providing range[values] in meters.
        Args:
          transport_mode (IsolineRoutingTransportMode):
            Transport mode of routing.
          origin (List):
            List including latitude and longitude in order.
          ranges (List):
            List of range values for isoline (in meters).
          routing_mode (IsolineRoutingMode):
            Isoline routing mode.
        Returns:
          IsolineRoutingResponse
        Raises:
          HEREError"""

        string_ranges = [str(int) for int in ranges]
        data = {
            "transportMode": transport_mode.__str__(),
            "origin": str.format("{0},{1}", origin[0], origin[1]),
            "range[type]": IsolineRoutingRangeType.distance.__str__(),
            "range[values]": ",".join(string_ranges),
            "routingMode": routing_mode.__str__(),
            "apiKey": self._api_key,
        }
        return self.__get(self._base_url, data, "departure")

    def time_isoline(
        self,
        transport_mode: IsolineRoutingTransportMode,
        origin: List[float],
        ranges: List[int],
    ) -> Optional[IsolineRoutingResponse]:
        """A time-based isoline, also called an Isochrone,
        can be requested by using range[type]=time and providing range[values] in seconds.
        Args:
          transport_mode (IsolineRoutingTransportMode):
            Transport mode of routing.
          origin (List):
            List including latitude and longitude in order.
          ranges (List):
            List of range values for isoline (in meters).
        Returns:
          IsolineRoutingResponse
        Raises:
          HEREError"""

        string_ranges = [str(int) for int in ranges]
        data = {
            "transportMode": transport_mode.__str__(),
            "origin": str.format("{0},{1}", origin[0], origin[1]),
            "range[type]": IsolineRoutingRangeType.time.__str__(),
            "range[values]": ",".join(string_ranges),
            "apiKey": self._api_key,
        }
        return self.__get(self._base_url, data, "departure")

    def isoline_based_on_consumption(
        self,
        origin: List[float],
        ranges: List[int],
        transport_mode: IsolineRoutingTransportMode,
        free_flow_speed_table: List[float],
        traffic_speed_table: List[float],
        ascent: int,
        descent: float,
        auxiliary_consumption: float,
    ):
        """Electric vehicles have a limited reachable range based on their current battery
        charge and factors affecting the rate of energy consumed, such as road slope or auxiliary
        power usage. Therefore, it is useful to visualize the appropriate range to avoid running
        out of energy before reaching a charging point.
        Args:
          transport_mode (IsolineRoutingTransportMode):
            Transport mode of routing.
          origin (List):
            List including latitude and longitude in order.
          ranges (List):
            List of range values for isoline (in meters).
          transport_mode (IsolineRoutingTransportMode):
            Transport mode of routing.
          free_flow_speed_table (List[float]):
            Free flow speed table.
          traffic_speed_table (List[float]):
            Traffic speed table.
          ascent (int):
            Int value of ascent.
          descent (float):
            Value of descent.
          auxiliary_consumption (float):
            Auxiliary consumption.
        Returns:
          IsolineRoutingResponse
        Raises:
          HEREError"""

        string_ranges = [str(int) for int in ranges]

        free_speed_table = [0]
        free_speed_table.extend(free_flow_speed_table)
        free_speed_table_str = ",".join([str(n) for n in free_speed_table])

        speed_table = [0]
        speed_table.extend(traffic_speed_table)
        speed_table_str = ",".join([str(n) for n in speed_table])

        data = {
            "origin": str.format("{0},{1}", origin[0], origin[1]),
            "range[type]": IsolineRoutingRangeType.consumption.__str__(),
            "range[values]": ",".join(string_ranges),
            "transportMode": transport_mode.__str__(),
            "ev[freeFlowSpeedTable]": free_speed_table_str,
            "ev[trafficSpeedTable]": speed_table_str,
            "ev[ascent]": ascent,
            "ev[descent]": descent,
            "ev[auxiliaryConsumption]": auxiliary_consumption,
            "apiKey": self._api_key,
        }
        return self.__get(self._base_url, data, "departure")

    def isoline_routing_at_specific_time(
        self,
        transport_mode: IsolineRoutingTransportMode,
        ranges: List[int],
        origin: Optional[List[float]] = None,
        departure_time: Optional[str] = None,
        destination: Optional[List[float]] = None,
        arrival_time: Optional[str] = None,
    ):
        """To calculate an isoline around an origin with a specific time, use departureTime.
        For a reverse isoline, that is, when using destination, you can use arrivalTime.
        If departureTime or arrivalTime are specified as "any", the isoline calculation will
        not take traffic flow and other time-dependent effects into account. This can be useful
        when it is not certain for what time of the day the isoline needs to be computed.
        Args:
          transport_mode (IsolineRoutingTransportMode):
            Transport mode of routing.
          ranges (List):
            List of range values for isoline (in meters).
          origin (List):
            List including latitude and longitude in order.
          departure_time (str):
            Departure time of the routing in format yyyy-MM-ddThh:mm:ss.
          destination (List):
            List including latitude and longitude in order.
          arrival_time (str):
            Arrival time of the planned routing in format yyyy-MM-ddThh:mm:ss.
        Returns:
          IsolineRoutingResponse
        Raises:
          HEREError"""

        string_ranges = [str(int) for int in ranges]
        if origin and departure_time:
            data = {
                "transportMode": transport_mode.__str__(),
                "origin": str.format("{0},{1}", origin[0], origin[1]),
                "departureTime": departure_time,
                "range[type]": IsolineRoutingRangeType.time.__str__(),
                "range[values]": ",".join(string_ranges),
                "apiKey": self._api_key,
            }
            return self.__get(self._base_url, data, "departure")
        elif destination and arrival_time:
            data = {
                "transportMode": transport_mode.__str__(),
                "destination": str.format("{0},{1}", destination[0], destination[1]),
                "arrivalTime": arrival_time,
                "range[type]": IsolineRoutingRangeType.time.__str__(),
                "range[values]": ",".join(string_ranges),
                "apiKey": self._api_key,
            }
            return self.__get(self._base_url, data, "arrival")
        else:
            raise HEREError(
                "Please provide either origin & departure_time or destination & arrival_time."
            )

    def multi_range_routing(
        self,
        transport_mode: IsolineRoutingTransportMode,
        ranges: List[int],
        origin: Optional[List[float]] = None,
        destination: Optional[List[float]] = None,
    ):
        """Isoline routing can be requested with multiple ranges which allows for the calculation
        of many isolines with the same start or destination.
        Args:
          transport_mode (IsolineRoutingTransportMode):
            Transport mode of routing.
          ranges (List):
            Range values for isoline routing.
          origin (List):
            List including latitude and longitude in order.
          destination (List):
            List including latitude and longitude in order.
        Returns:
          IsolineRoutingResponse
        Raises:
          HEREError"""

        string_ranges = [str(int) for int in ranges]
        if origin:
            data = {
                "transportMode": transport_mode.__str__(),
                "origin": str.format("{0},{1}", origin[0], origin[1]),
                "range[type]": IsolineRoutingRangeType.distance.__str__(),
                "range[values]": ",".join(string_ranges),
                "apiKey": self._api_key,
            }
            return self.__get(self._base_url, data, "departure")
        elif destination:
            data = {
                "transportMode": transport_mode.__str__(),
                "destination": str.format("{0},{1}", destination[0], destination[1]),
                "range[type]": IsolineRoutingRangeType.distance.__str__(),
                "range[values]": ",".join(string_ranges),
                "apiKey": self._api_key,
            }
            return self.__get(self._base_url, data, "arrival")
        else:
            raise HEREError(
                "Please provide values for origin or destination parameter."
            )

    def reverse_direction_isoline(
        self,
        transport_mode: IsolineRoutingTransportMode,
        ranges: List[int],
        origin: Optional[List[float]] = None,
        destination: Optional[List[float]] = None,
    ):
        """Calculates an isoline in the reverse direction. To trigger calculation in reverse direction,
        use the destination parameter instead of origin.
        Args:
          transport_mode (IsolineRoutingTransportMode):
            Transport mode of routing.
          ranges (List):
            Range values for isoline routing.
          origin (List):
            List including latitude and longitude in order.
          destination (List):
            List including latitude and longitude in order.
        Returns:
          IsolineRoutingResponse
        Raises:
          HEREError"""

        string_ranges = [str(int) for int in ranges]
        if origin:
            data = {
                "transportMode": transport_mode.__str__(),
                "origin": str.format("{0},{1}", origin[0], origin[1]),
                "range[type]": IsolineRoutingRangeType.time.__str__(),
                "range[values]": ",".join(string_ranges),
                "apiKey": self._api_key,
            }
            return self.__get(self._base_url, data, "departure")
        elif destination:
            data = {
                "transportMode": transport_mode.__str__(),
                "destination": str.format("{0},{1}", destination[0], destination[1]),
                "range[type]": IsolineRoutingRangeType.time.__str__(),
                "range[values]": range,
                "apiKey": self._api_key,
            }
            return self.__get(self._base_url, data, "arrival")
        else:
            raise HEREError(
                "Please provide values for origin or destination parameter."
            )
