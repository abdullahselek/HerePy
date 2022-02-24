#!/usr/bin/env python

import sys
import json
import requests

from herepy.here_api import HEREApi
from herepy.utils import Utils
from herepy.error import HEREError, UnauthorizedError, InvalidRequestError
from herepy.models import (
    TrafficIncidentResponse,
    TrafficFlowResponse,
    TrafficFlowAvailabilityResponse,
)
from herepy.here_enum import (
    IncidentsCriticalityStr,
    IncidentsCriticalityInt,
    FlowProximityAdditionalAttributes,
)

from typing import List, Optional
from enum import Enum


class TrafficApi(HEREApi):
    """A python interface into the HERE Traffic API"""

    def __init__(self, api_key: str = None, timeout: int = None):
        """Returns a TrafficApi instance.
        Args:
          api_key (str):
            API key taken from HERE Developer Portal.
          timeout (int):
            Timeout limit for requests.
        """

        super(TrafficApi, self).__init__(api_key, timeout)
        self._base_url = "https://traffic.ls.hereapi.com/traffic/6.1/"

    def __get(self, url, data):
        url = Utils.build_url(url, extra_params=data)
        response = requests.get(url, timeout=self._timeout)
        json_data = json.loads(response._content.decode("utf8"))
        if json_data.get("TRAFFIC_ITEMS") != None:
            return TrafficIncidentResponse.new_from_jsondict(
                json_data, param_defaults={
                    "TIMESTAMP": None,
                    "VERSION": None,
                    "TRAFFIC_ITEMS": None,
                    "EXTENDED_COUNTRY_CODE": None,
                    "error": None,
                }
            )
        elif json_data.get("RWS") != None:
            return TrafficFlowResponse.new_from_jsondict(
                json_data, param_defaults={
                    "RWS": None,
                    "CREATED_TIMESTAMP": None,
                    "VERSION": None,
                    "UNITS": None,
                }
            )
        elif json_data.get("Response") != None:
            return TrafficFlowAvailabilityResponse.new_from_jsondict(
                json_data, param_defaults={"Response": None}
            )
        else:
            error = self.__get_error_from_response(json_data)
            raise error

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

    def __prepare_str_values(self, enums: [Enum]):
        values = ""
        for enum in enums:
            values += enum.__str__() + ","
        values = values[:-1]
        return values

    def __prepare_criticality_int_values(
        self, criticality_enums: [IncidentsCriticalityInt]
    ):
        criticality_values = ""
        for criticality in criticality_enums:
            criticality_values += str(criticality.__int__()) + ","
        criticality_values = criticality_values[:-1]
        return criticality_values

    def __prepare_corridor_value(self, points: List[List[float]], width: int):
        corridor_str = ""
        for lat_long_pair in points:
            corridor_str += str.format("{0},{1};", lat_long_pair[0], lat_long_pair[1])
        corridor_str += str(width)
        return corridor_str

    def incidents_in_bounding_box(
        self,
        top_left: List[float],
        bottom_right: List[float],
        criticality: [IncidentsCriticalityStr],
    ) -> Optional[TrafficIncidentResponse]:
        """Request traffic incident information within specified area.
        Args:
          top_left (List):
            List contains latitude and longitude in order.
          bottom_right (List):
            List contains latitude and longitude in order.
          criticality (List):
            List of IncidentsCriticalityStr.
        Returns:
          TrafficIncidentResponse
        Raises:
          HEREError"""

        data = {
            "bbox": str.format(
                "{0},{1};{2},{3}",
                top_left[0],
                top_left[1],
                bottom_right[0],
                bottom_right[1],
            ),
            "apiKey": self._api_key,
            "criticality": self.__prepare_str_values(enums=criticality),
        }
        return self.__get(self._base_url + "incidents.json", data)

    def incidents_in_corridor(
        self, points: List[List[float]], width: int
    ) -> Optional[TrafficIncidentResponse]:
        """Request traffic incidents for a defined route.
        Args:
          points (List):
            List contains lists of latitude and longitude pairs in order.
          width (int):
            Width of corridor.
        Returns:
          TrafficIncidentResponse
        Raises:
          HEREError"""

        data = {
            "corridor": self.__prepare_corridor_value(points=points, width=width),
            "apiKey": self._api_key,
        }
        return self.__get(self._base_url + "incidents.json", data)

    def incidents_via_proximity(
        self,
        latitude: float,
        longitude: float,
        radius: int,
        criticality: [IncidentsCriticalityInt],
    ) -> Optional[TrafficIncidentResponse]:
        """Request traffic incident information within specified area.
        Args:
          latitude (float):
            Latitude of specified area.
          longitude (float):
            Longitude of specified area.
          radius (int):
            Radius of area in meters.
          criticality (List):
            List of IncidentsCriticalityInt.
        Returns:
          TrafficIncidentResponse
        Raises:
          HEREError"""

        data = {
            "prox": str.format("{0},{1},{2}", latitude, longitude, radius),
            "criticality": self.__prepare_criticality_int_values(
                criticality_enums=criticality
            ),
            "apiKey": self._api_key,
        }
        return self.__get(self._base_url + "incidents.json", data)

    def flow_using_quadkey(self, quadkey: str) -> Optional[TrafficFlowResponse]:
        """Request traffic flow information using a quadkey.
        Args:
          quadkey (str):
            The quadkey unique defines a region of the globe using a standard addressing algortihm.
        Returns:
          TrafficFlowResponse
        Raises:
          HEREError"""

        data = {
            "quadkey": quadkey,
            "apiKey": self._api_key,
        }
        return self.__get(self._base_url + "flow.json", data)

    def flow_within_boundingbox(
        self,
        top_left: List[float],
        bottom_right: List[float],
    ) -> Optional[TrafficFlowResponse]:
        """Request traffic flow information within specified area.
        Args:
          top_left (List):
            List contains latitude and longitude in order.
          bottom_right (List):
            List contains latitude and longitude in order.
        Returns:
          TrafficFlowResponse
        Raises:
          HEREError"""

        data = {
            "bbox": str.format(
                "{0},{1};{2},{3}",
                top_left[0],
                top_left[1],
                bottom_right[0],
                bottom_right[1],
            ),
            "apiKey": self._api_key,
        }
        return self.__get(self._base_url + "flow.json", data)

    def flow_using_proximity(
        self, latitude: float, longitude: float, distance: int
    ) -> Optional[TrafficFlowResponse]:
        """Request traffic flow for a circle around a defined point.
        Args:
          latitude (float):
            List contains latitude and longitude in order.
          longitude (float):
            List contains latitude and longitude in order.
          distance (int):
            Extending a distance of metres in all directions.
        Returns:
          TrafficFlowResponse
        Raises:
          HEREError"""

        data = {
            "prox": str.format(
                "{0},{1},{2}",
                latitude,
                longitude,
                distance,
            ),
            "apiKey": self._api_key,
        }
        return self.__get(self._base_url + "flow.json", data)

    def flow_using_proximity_returning_additional_attributes(
        self,
        latitude: float,
        longitude: float,
        distance: int,
        attributes: [FlowProximityAdditionalAttributes],
    ) -> Optional[TrafficFlowResponse]:
        """Request traffic flow information using proximity, returning shape and functional class.
        Args:
          latitude (float):
            List contains latitude and longitude in order.
          longitude (float):
            List contains latitude and longitude in order.
          distance (int):
            Extending a distance of metres in all directions.
          attributes (List):
            List that contains FlowProximityAdditionalAttributes.
        Returns:
          TrafficFlowResponse
        Raises:
          HEREError"""

        data = {
            "prox": str.format(
                "{0},{1},{2}",
                latitude,
                longitude,
                distance,
            ),
            "responseattibutes": self.__prepare_str_values(enums=attributes),
            "apiKey": self._api_key,
        }
        return self.__get(self._base_url + "flow.json", data)

    def flow_with_minimum_jam_factor(
        self, top_left: List[float], bottom_right: List[float], min_jam_factor: int = 7
    ) -> Optional[TrafficFlowResponse]:
        """Request traffic flow information in specified area with a jam factor.
        Args:
          top_left (List):
            List contains latitude and longitude in order.
          bottom_right (List):
            List contains latitude and longitude in order.
          min_jam_factor (int):
            Severe congestion with a jam factor greater than 7.
        Returns:
          TrafficFlowResponse
        Raises:
          HEREError"""

        data = {
            "bbox": str.format(
                "{0},{1};{2},{3}",
                top_left[0],
                top_left[1],
                bottom_right[0],
                bottom_right[1],
            ),
            "minjamfactor": str.format("{0}", min_jam_factor),
            "apiKey": self._api_key,
        }
        return self.__get(self._base_url + "flow.json", data)

    def flow_in_corridor(
        self, points: List[List[float]], width: int
    ) -> Optional[TrafficFlowResponse]:
        """Request traffic flow for a defined route.
        Args:
          points (List):
            List contains lists of latitude and longitude pairs in order.
          width (int):
            Width of corridor (in meters).
        Returns:
          TrafficFlowResponse
        Raises:
          HEREError"""

        data = {
            "corridor": self.__prepare_corridor_value(points=points, width=width),
            "apiKey": self._api_key,
        }
        return self.__get(self._base_url + "flow.json", data)

    def flow_availability_data(self) -> Optional[TrafficFlowAvailabilityResponse]:
        """Flow availability requests allow you to see what traffic flow coverage exists in the current Traffic API.
        Returns:
          TrafficFlowAvailabilityResponse
        Raises:
          HEREError"""

        data = {
            "apiKey": self._api_key,
        }
        return self.__get(self._base_url + "flowavailability.json", data)

    def additional_attributes(
        self, quadkey: str, attributes: [FlowProximityAdditionalAttributes]
    ) -> [TrafficFlowResponse]:
        """Request traffic flow including shape and functional class information.
        Args:
          quadkey (str):
            The quadkey unique defines a region of the globe using a standard addressing algortihm.
          attributes (List):
            List that contains FlowProximityAdditionalAttributes.
        Returns:
          TrafficFlowResponse
        Raises:
          HEREError"""

        data = {
            "quadkey": quadkey,
            "responseattibutes": self.__prepare_str_values(enums=attributes),
            "apiKey": self._api_key,
        }
        return self.__get(self._base_url + "flow.json", data)
