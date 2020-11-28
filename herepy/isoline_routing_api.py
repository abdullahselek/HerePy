#!/usr/bin/env python

import sys
import json
import requests

from typing import List, Optional
from herepy.here_api import HEREApi
from herepy.utils import Utils
from herepy.models import IsolineRoutingResponse
from herepy.error import HEREError, UnauthorizedError, InvalidRequestError
from herepy.here_enum import IsolineRoutingTransportMode, IsolineRoutingMode, IsolineRoutingRangeType


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
            "Message", "Error occured on " + sys._getframe(1).f_code.co_name
        )
        if error_type == "Invalid Request":
            return InvalidRequestError(error_message)
        else:
            return HEREError(error_message)

    def __get(self, url, data):
        url = Utils.build_url(url, extra_params=data)
        response = requests.get(url, timeout=self._timeout)
        json_data = json.loads(response.content.decode("utf8"))
        if json_data.get("departure") != None and json_data.get("isolines") != None:
            return IsolineRoutingResponse.new_from_jsondict(
                json_data, param_defaults={"departure": None, "isolines": None}
            )
        else:
            error = self.__get_error_from_response(json_data)
            raise error

    def distance_based_isoline(
        self,
        transport_mode: IsolineRoutingTransportMode,
        origin: List[float],
        range: int,
        routing_mode: IsolineRoutingMode,
    ) -> Optional[IsolineRoutingResponse]:
        """A distance-based isoline, also called an Isodistance,
        can be requested using range[type]=distance and providing range[values] in meters.
        Args:
          transport_mode (IsolineRoutingTransportMode):
            Transport mode of routing.
          origin (List):
            List including latitude and longitude in order.
          range (int):
            Range of isoline in meters.
          routing_mode (IsolineRoutingMode):
            Isoline routing mode.
        Returns:
          IsolineRoutingResponse
        Raises:
          HEREError"""

        data = {
            "transportMode": transport_mode.__str__(),
            "origin": str.format("{0},{1}", origin[0], origin[1]),
            "range[type]": IsolineRoutingRangeType.distance.__str__(),
            "range[values]": range,
            "routingMode": routing_mode.__str__(),
            "apiKey": self._api_key,
        }
        return self.__get(self._base_url, data)

    def time_isoline(
        self,
        transport_mode: IsolineRoutingTransportMode,
        origin: List[float],
        range: int,
    ) -> Optional[IsolineRoutingResponse]:
        """A time-based isoline, also called an Isochrone,
        can be requested by using range[type]=time and providing range[values] in seconds.
        Args:
          transport_mode (IsolineRoutingTransportMode):
            Transport mode of routing.
          origin (List):
            List including latitude and longitude in order.
          range (int):
            Range of isoline in meters.
        Returns:
          IsolineRoutingResponse
        Raises:
          HEREError"""

        data = {
            "transportMode": transport_mode.__str__(),
            "origin": str.format("{0},{1}", origin[0], origin[1]),
            "range[type]": IsolineRoutingRangeType.time.__str__(),
            "range[values]": range,
            "apiKey": self._api_key,
        }
        return self.__get(self._base_url, data)

    def isoline_based_on_consumption(
        self,
        origin: List[float],
        range: int,
        transport_mode: IsolineRoutingTransportMode,
        free_flow_speed_table: List[float],
        traffic_speed_table: List[float],
        ascent: int,
        descent: float,
        auxiliary_consumption: float
    ):
        free_speed_table = [0]
        free_speed_table.extend(free_flow_speed_table)
        free_speed_table_str = ','.join([str(n) for n in free_speed_table])
        

        speed_table = [0]
        speed_table.extend(traffic_speed_table)
        speed_table_str = ','.join([str(n) for n in speed_table])

        data = {
            "origin": str.format("{0},{1}", origin[0], origin[1]),
            "range[type]": IsolineRoutingRangeType.consumption.__str__(),
            "range[values]": range,
            "transportMode": transport_mode.__str__(),
            "ev[freeFlowSpeedTable]": free_speed_table_str,
            "ev[trafficSpeedTable]": speed_table_str,
            "ev[ascent]": ascent,
            "ev[descent]": descent,
            "ev[auxiliaryConsumption]": auxiliary_consumption,
            "apiKey": self._api_key,
        }
        return self.__get(self._base_url, data)
