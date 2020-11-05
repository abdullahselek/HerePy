#!/usr/bin/env python

import sys
import json
import requests

from herepy.here_api import HEREApi
from herepy.utils import Utils
from herepy.error import HEREError, UnauthorizedError
from herepy.models import PublicTransitResponse
from herepy.here_enum import (
    PublicTransitSearchMethod,
    PublicTransitRoutingMode,
    PublicTransitModeType,
)
from typing import List, Optional


class PublicTransitApi(HEREApi):
    """A python interface into the HERE Public Transit API"""

    def __init__(self, api_key: str = None, timeout: int = None):
        """Returns a PublicTransitApi instance.
        Args:
          api_key (str):
            API key taken from HERE Developer Portal.
          timeout (int):
            Timeout limit for requests.
        """

        super(PublicTransitApi, self).__init__(api_key, timeout)
        self._base_url = "https://transit.ls.hereapi.com/v3/"

    def __get(self, data, path, json_node):
        url = Utils.build_url(self._base_url + path, extra_params=data)
        response = requests.get(url, timeout=self._timeout)
        json_data = json.loads(response.content.decode("utf8"))
        if json_node in json_data.get("Res", {}):
            return PublicTransitResponse.new_from_jsondict(json_data)
        elif "text" in json_data.get("Res", {}).get("Message", {}):
            raise HEREError(
                json_data["Res"]["Message"]["text"],
                "Error occured on " + sys._getframe(1).f_code.co_name,
            )
        elif "error" in json_data:
            if json_data["error"] == "Unauthorized":
                raise UnauthorizedError(json_data["error_description"])
        else:
            raise HEREError("Error occured on " + sys._getframe(1).f_code.co_name)

    def find_stations_by_name(
        self,
        center: List[float],
        name: str,
        max_count: int = 5,
        method: PublicTransitSearchMethod = PublicTransitSearchMethod.fuzzy,
        radius: int = 20000,
    ) -> Optional[PublicTransitResponse]:
        """Request a list of public transit stations based on name.
        Args:
          center (List):
            List contains latitude and longitude in order.
          name (str):
            station name.
          max_count (int):
            maximum number of stations  (Default is 5).
          method (enum):
            Matching method from PublicTransitSearchMethod (Default is fuzzy).
          radius (int):
            specifies radius in kilometers (Default is 20000km).
        Returns:
          PublicTransitResponse
        Raises:
          HEREError
        """

        data = {
            "center": str.format("{0},{1}", center[0], center[1]),
            "name": name,
            "apikey": self._api_key,
            "max": max_count,
            "method": method.__str__(),
            "radius": radius,
        }
        return self.__get(data, "stations/by_name.json", "Stations")

    def find_stations_nearby(
        self, center: List[float], radius: int = 500, max_count: int = 5
    ) -> Optional[PublicTransitResponse]:
        """Request a list of public transit stations within a given geo-location.
        Args:
          center (List):
            List contains latitude and longitude in order.
          radius (int):
            specifies radius in meters (Default is 500m).
          max_count (int):
            maximum number of stations  (Default is 5).
        Returns:
          PublicTransitResponse
        Raises:
          HEREError
        """

        data = {
            "center": str.format("{0},{1}", center[0], center[1]),
            "radius": radius,
            "apikey": self._api_key,
            "max": max_count,
        }
        return self.__get(data, "stations/by_geocoord.json", "Stations")

    @classmethod
    def __prepare_station_ids(cls, ids):
        station_ids = ""
        for stn_id in ids:
            station_ids += str.format("{0},", stn_id)
        station_ids = station_ids[:-1]
        return station_ids

    def find_stations_by_id(
        self, ids: List[int], lang: str
    ) -> Optional[PublicTransitResponse]:
        """Request details of a specific transit station based on a previous request.
        Args:
          ids (List):
            List contains station ids.
          lang (str):
            language code for response like `en`.
        Returns:
          PublicTransitResponse
        Raises:
          HEREError
        """

        data = {
            "stnIds": self.__prepare_station_ids(ids),
            "lang": lang,
            "apikey": self._api_key,
        }
        return self.__get(data, "stations/by_ids.json", "Stations")

    def find_transit_coverage_in_cities(
        self, center: List[float], political_view: str, radius: int
    ) -> Optional[PublicTransitResponse]:
        """Request a list of transit operators available in cities nearby.
        Args:
          center (List):
            List contains latitude and longitude in order.
          political_view (str):
            switch for grouping results like `CHN`.
          radius (int):
            specifies radius in meters.
        Returns:
          PublicTransitResponse
        Raises:
          HEREError
        """

        data = {
            "center": str.format("{0},{1}", center[0], center[1]),
            "politicalview": political_view,
            "radius": radius,
            "apikey": self._api_key,
        }
        return self.__get(data, "coverage/city.json", "Coverage")

    def next_nearby_departures_of_station(
        self, station_id: int, time: str, lang: str = "en"
    ) -> Optional[PublicTransitResponse]:
        """Request a list of next departure times and destinations of a particular station.
        Args:
          lang (str):
            language code for response like `en` Default is `en`.
          station_id (int):
            station id for departures.
          time (str):
            time formattes in yyyy-mm-ddThh:mm:ss.
        Returns:
          PublicTransitResponse
        Raises:
          HEREError
        """

        data = {
            "lang": lang,
            "stnId": station_id,
            "time": time,
            "apikey": self._api_key,
        }
        return self.__get(data, "board.json", "NextDepartures")

    def next_departures_from_location(
        self,
        center: List[float],
        time: str,
        lang: str = "en",
        max: int = 40,
        max_station: int = 40,
    ) -> Optional[PublicTransitResponse]:
        """Request a list of all next departure times and destinations from a given location.
        Args:
          center (List):
            List contains latitude and longitude in order.
          time (str):
            time formattes in yyyy-mm-ddThh:mm:ss.
          lang (str):
            language code for response like `en`. Default is `en`.
          max (int):
            maximum number of next departures per station. Default is 40.
          max_station (int):
            maximum number of stations for which departures are required. Default is 40.
        Returns:
          PublicTransitResponse
        Raises:
          HEREError
        """

        data = {
            "lang": lang,
            "center": str.format("{0},{1}", center[0], center[1]),
            "time": time,
            "apikey": self._api_key,
            "max": max,
            "maxStn": max_station,
        }
        return self.__get(data, "multiboard/by_geocoord.json", "MultiNextDepartures")

    def next_departures_for_stations(
        self,
        station_ids: List[int],
        time: str,
        lang: str = "en",
        max: int = 40,
        max_station: int = 40,
    ) -> Optional[PublicTransitResponse]:
        """Request a list of all next departure times and destinations for a give list of stations.
        Args:
          station_ids (List):
            a list of stop ids.
          time (str):
            time formattes in yyyy-mm-ddThh:mm:ss.
          lang (str):
            language code for response like `en`. Default is `en`.
          max (int):
            maximum number of next departures per station. Default is 40.
          max_station (int):
            maximum number of stations for which departures are required. Default is 40.
        Returns:
          PublicTransitResponse
        Raises:
          HEREError
        """

        data = {
            "lang": lang,
            "time": time,
            "apikey": self._api_key,
            "max": max,
            "maxStn": max_station,
            "stnIds": self.__prepare_station_ids(station_ids),
        }
        return self.__get(data, "multiboard/by_stn_ids.json", "MultiNextDepartures")

    def calculate_route(
        self,
        departure: List[float],
        arrival: List[float],
        time: str,
        max_connections: int = 3,
        changes: int = -1,
        lang: str = "en",
        include_modes: List[PublicTransitModeType] = None,
        exclude_modes: List[PublicTransitModeType] = None,
        units: str = "metric",
        max_walking_distance: int = 2000,
        walking_speed: int = 100,
        show_arrival_times: bool = True,
        graph: bool = False,
        routing_mode: PublicTransitRoutingMode = PublicTransitRoutingMode.schedule,
    ) -> Optional[PublicTransitResponse]:
        """Request a public transit route between any two places.
        Args:
          departure (List):
            List contains latitude and longitude in order.
          arrival (List):
            List contains latitude and longitude in order.
          time (str):
            time formatted in yyyy-mm-ddThh:mm:ss.
          max_connections (int):
            Specifies the number of following departure/arrivals the response should include.
            The possible values are: 1-6.
          changes (int):
            Specifies the maximum number of changes or transfers allowed in a route.
            0-6 or -1.
            The default is -1 (which disables the filter, or unlimited no of changes permitted).
          lang (str):
            Specifies the language of the response.
          include_modes (List[PublicTransitModeType]):
            Specifies the transit type filter used to determine which types of transit to include in the response.
          exclude_modes (List[PublicTransitModeType]):
            Specifies the transit type filter used to determine which types of transit to exclude in the response.
          units (str):
            Units of measurement used. metric oder imperial.
          max_walking_distance (int):
            Specifies a maximum walking distance in meters. Allowed values are 0-6000.
          walking_speed (int):
            Specifies the walking speed in percent of normal walking speed. Allowed values are 50-200.
          show_arrival_times (boolean):
            flag to indicate if response should show arrival times or departure times.
          graph (boolean):
            flag to indicate if response should contain coordinate pairs to allow the drawing of a polyline for the route.
          routing_type (PublicTransitRoutingType):
            type of routing. Default is time_tabled.
        Returns:
          PublicTransitResponse
        Raises:
          HEREError
        """

        data = {
            "dep": str.format("{0},{1}", departure[0], departure[1]),
            "arr": str.format("{0},{1}", arrival[0], arrival[1]),
            "max": max_connections,
            "time": time,
            "changes": changes,
            "lang": lang,
            "units": units,
            "walk": ",".join([str(max_walking_distance), str(walking_speed)]),
            "arrival": 1 if show_arrival_times == True else 0,
            "apikey": self._api_key,
            "graph": 1 if graph == True else 0,
            "routingMode": routing_mode.__str__(),
        }

        modes = None
        if include_modes is not None and exclude_modes is not None:
            raise HEREError("Specify either include_modes or exclude_modes, not both.")
        if include_modes is not None:
            modes = ",".join(mode.__str__() for mode in include_modes)
        if exclude_modes is not None:
            modes = ",".join("-" + mode.__str__() for mode in exclude_modes)
        if modes is not None:
            data["modes"] = modes

        response = self.__get(data, "route.json", "Connections")
        response_with_short_route = self._get_response_with_short_route(response)
        return response_with_short_route

    def coverage_witin_a_city(
        self,
        city_name: str,
        political_view: int,
        max: int = None,
        details: int = 1,
        lang: str = "en",
    ) -> Optional[PublicTransitResponse]:
        """Request a list of transit operator coverage within a specified city.
        Args:
          city_name (str):
            the name or part of the name of the search city.
          political_view (int):
            1 enables, 0 disables grouping results.
          max (int):
            maximum number of results.
          details (int):
            with 1 supported list of operators and population added to response.
            Set to 0 just return the matching city names.
          lang (str):
            the language of the response, default `en`.
        Returns:
          PublicTransitResponse
        Raises:
          HEREError
        """

        data = {
            "name": city_name,
            "apikey": self._api_key,
            "max": max,
            "details": details,
            "politicalview": political_view,
            "lang": lang,
        }
        if max is None:
            del data["max"]
        return self.__get(data, "coverage/search.json", "Coverage")

    def coverage_nearby(
        self, details: int, center: List[float]
    ) -> Optional[PublicTransitResponse]:
        """Request a list of transit operators and station coverage nearby.
        Args:
          details (int):
            0 disables showing line info, 1 enables showing line info.abs
          center (List):
            List contains latitude and longitude in order.
        Returns:
          PublicTransitResponse
        Raises:
          HEREError
        """
        data = {
            "details": details,
            "center": str.format("{0},{1}", center[0], center[1]),
            "apikey": self._api_key,
        }
        return self.__get(data, "coverage/nearby.json", "LocalCoverage")

    def _get_response_with_short_route(self, public_transit_response):
        response = public_transit_response
        connections = response.Res["Connections"]["Connection"]

        for connection in connections:
            connection["short_route"] = self._get_route_from_public_transit_connection(
                connection
            )
        return response

    def _get_route_from_public_transit_connection(self, public_transit_connection):
        sections = public_transit_connection["Sections"]["Sec"]
        lines = []
        for section in sections:
            if str(section["mode"]) != str(PublicTransitModeType["walk"]):
                transport = section["Dep"]["Transport"]
                lines.append(transport["name"] + " - " + transport["dir"])
        route = "; ".join(list(map(str, lines)))
        return route
