#!/usr/bin/env python

import sys
import json
import requests

from typing import List, Optional
from herepy.here_enum import EVStationConnectorTypes
from herepy.utils import Utils
from herepy.error import HEREError
from herepy.models import EVChargingStationsResponse


class EVChargingStationsApi:
    """A python interface into the HERE EV Charging Stations API"""

    def __init__(self, api_key: str = None, timeout: int = None):
        """Returns a EVChargingStationsApi instance.
        Args:
          api_key (str):
            API key taken from HERE Developer Portal.
          timeout (int):
            Timeout limit for requests.
        """

        self._api_key = api_key
        if timeout:
            self._timeout = timeout
        else:
            self._timeout = 20
        self._base_url = "https://ev-v2.cit.cc.api.here.com/ev/"

    def __get(self, base_url, data, response_cls):
        url = Utils.build_url(base_url, extra_params=data)
        response = requests.get(url, timeout=self._timeout)
        json_data = json.loads(response.content.decode("utf8"))
        if json_data.get("evStations") is not None:
            return response_cls.new_from_jsondict(json_data)
        else:
            raise error_from_ev_charging_service_error(json_data)

    def __connector_types_str(self, connector_types: List[EVStationConnectorTypes]):
        connector_types_str = ""
        for connector_type in connector_types:
            connector_types_str += str.format("{0},", connector_type._value_)
        connector_types_str = connector_types_str[:-1]
        return connector_types_str

    def __corridor_str(self, points: List[float]):
        if len(points) % 2 != 0:
            points = points[:-1]
        corridor_str = ""
        for i in range(0, len(points), 2):
            corridor_str += str.format("{0},{1};", points[i], points[i + 1])
        corridor_str = corridor_str[:-1]
        return corridor_str

    def get_stations_circular_search(
        self,
        latitude: float,
        longitude: float,
        radius: int,
        connectortypes: List[EVStationConnectorTypes] = None,
        maxresults: int = 50,
        offset: int = 0,
    ) -> Optional[EVChargingStationsResponse]:
        """Makes a search request for charging stations.
           A circular search area defined by the latitude and longitude of its center
           (compliant with WGS 84) and an integer representing the radius of the area
           in meters, all separated by commas.
        Args:
          latitude (float):
            latitude.
          longitude (float):
            longitude.
          radius (int):
            Radius of circular area in meter. Radius can be a maximum of 200 km (200000).
          connectortypes (List[EVStationConnectorTypes]):
            Optional, to identify the connector types.
          maxresults (int):
            The maximum number of results a response can contain.
            This parameter can be used with the offset parameter in the query and HasMore in the response for pagination.
          offset (int):
            A value specifying the index of the first result. The offset together with the "maxresults" value can be used to support a paging mechanism on search results.
            This parameter can be used with the maxresults parameter in the query and HasMore in the response for pagination.
        Returns:
          EVChargingStationsResponse
        Raises:
          HEREError
        """

        if connectortypes:
            connector_types_str = self.__connector_types_str(connectortypes)
            data = {
                "apiKey": self._api_key,
                "prox": str.format("{0},{1},{2}", latitude, longitude, radius),
                "connectortype": connector_types_str,
                "maxresults": maxresults,
                "offset": offset,
            }
        else:
            data = {
                "apiKey": self._api_key,
                "prox": str.format("{0},{1},{2}", latitude, longitude, radius),
                "maxresults": maxresults,
                "offset": offset,
            }
        response = self.__get(
            self._base_url + "stations.json", data, EVChargingStationsResponse
        )
        return response

    def get_stations_bounding_box(
        self,
        top_left: List[float],
        bottom_right: List[float],
        connectortypes: List[EVStationConnectorTypes] = None,
        maxresults: int = 50,
        offset: int = 0,
    ) -> Optional[EVChargingStationsResponse]:
        """Makes a search request for charging stations with in given
           bounding box. The bounding box can have a maximum height / width of 400km.
        Args:
          top_left (List):
            List contains latitude and longitude in order.
          bottom_right (List):
            List contains latitude and longitude in order.
          connectortypes (List[EVStationConnectorTypes]):
            Optional, to identify the connector types.
          maxresults (int):
            The maximum number of results a response can contain.
            This parameter can be used with the offset parameter in the query and HasMore in the response for pagination.
          offset (int):
            A value specifying the index of the first result. The offset together with the "maxresults" value can be used to support a paging mechanism on search results.
            This parameter can be used with the maxresults parameter in the query and HasMore in the response for pagination.
        Returns:
          EVChargingStationsResponse
        Raises:
          HEREError
        """

        if connectortypes:
            connector_types_str = self.__connector_types_str(connectortypes)
            data = {
                "apiKey": self._api_key,
                "bbox": str.format(
                    "{0},{1};{2},{3}",
                    top_left[0],
                    top_left[1],
                    bottom_right[0],
                    bottom_right[1],
                ),
                "connectortype": connector_types_str,
                "maxresults": maxresults,
                "offset": offset,
            }
        else:
            data = {
                "apiKey": self._api_key,
                "bbox": str.format(
                    "{0},{1};{2},{3}",
                    top_left[0],
                    top_left[1],
                    bottom_right[0],
                    bottom_right[1],
                ),
                "maxresults": maxresults,
                "offset": offset,
            }
        response = self.__get(
            self._base_url + "stations.json", data, EVChargingStationsResponse
        )
        return response

    def get_stations_corridor(
        self,
        points: List[float],
        connectortypes: List[EVStationConnectorTypes] = None,
        maxresults: int = 50,
        offset: int = 0,
    ) -> Optional[EVChargingStationsResponse]:
        """Makes a search request for charging stations with in given corridor.
           Maximum corridor area is 5000 km2.
        Args:
          points (List):
            List contains latitude and longitude pairs in order.
          connectortypes (List[EVStationConnectorTypes]):
            Optional, to identify the connector types.
          maxresults (int):
            The maximum number of results a response can contain.
            This parameter can be used with the offset parameter in the query and HasMore in the response for pagination.
          offset (int):
            A value specifying the index of the first result. The offset together with the "maxresults" value can be used to support a paging mechanism on search results.
            This parameter can be used with the maxresults parameter in the query and HasMore in the response for pagination.
        Returns:
          EVChargingStationsResponse
        Raises:
          HEREError
        """

        if connectortypes:
            connector_types_str = self.__connector_types_str(connectortypes)
            data = {
                "apiKey": self._api_key,
                "corridor": self.__corridor_str(points),
                "connectortype": connector_types_str,
                "maxresults": maxresults,
                "offset": offset,
            }
        else:
            data = {
                "apiKey": self._api_key,
                "corridor": self.__corridor_str(points),
                "maxresults": maxresults,
                "offset": offset,
            }
        response = self.__get(
            self._base_url + "stations.json", data, EVChargingStationsResponse
        )
        return response

    def get_station_details(
        self, station_id: str, maxresults: int = 50, offset: int = 0
    ) -> Optional[EVChargingStationsResponse]:
        """Based on the results of a search for charging stations, this method
        retrieves the full/updated information about a single charging station only.
        Args:
          station_id (str):
            station_id is an attribute of the evStation element with a unique value.
          maxresults (int):
            The maximum number of results a response can contain.
            This parameter can be used with the offset parameter in the query and HasMore in the response for pagination.
          offset (int):
            A value specifying the index of the first result. The offset together with the "maxresults" value can be used to support a paging mechanism on search results.
            This parameter can be used with the maxresults parameter in the query and HasMore in the response for pagination.
        Returns:
          EVChargingStationsResponse
        Raises:
          HEREError
        """

        data = {"apiKey": self._api_key, "maxresults": maxresults, "offset": offset}
        url = self._base_url + "stations/" + station_id + ".json"
        response = self.__get(url, data, EVChargingStationsResponse)
        return response


class UnauthorizedError(HEREError):

    """Unauthorized Error Type.

    This error is returned if the specified token was invalid or no contract
    could be found for this token.
    """


# pylint: disable=R0911
def error_from_ev_charging_service_error(json_data: dict):
    """Return the correct subclass for ev charging errors"""

    if "Type" in json_data:
        error_type = json_data["Type"]
        message = json_data["Message"]

        if error_type == "Unauthorized":
            return UnauthorizedError(message)
    elif "error" in json_data and "error_description" in json_data:
        return HEREError(
            "Error occurred: "
            + json_data["error"]
            + ", description: "
            + json_data["error_description"]
        )
    # pylint: disable=W0212
    return HEREError("Error occurred on " + sys._getframe(1).f_code.co_name)
