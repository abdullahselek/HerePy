#!/usr/bin/env python

import os
import datetime
import sys
import json
import requests

from herepy.geocoder_api import GeocoderApi
from herepy.here_api import HEREApi
from herepy.utils import Utils
from herepy.error import HEREError
from herepy.models import RoutingResponse, RoutingMatrixResponse, RoutingResponseV8
from herepy.here_enum import (
    RouteMode,
    RoutingMode,
    RoutingTransportMode,
    RoutingMetric,
    RoutingApiReturnField,
    RoutingApiSpanField,
    MatrixSummaryAttribute,
    MatrixRoutingType,
    MatrixRoutingMode,
    MatrixRoutingProfile,
    MatrixRoutingTransportMode,
)
from herepy.objects import Avoid, Truck
from herepy import polling
from typing import List, Dict, Union, Optional


class RoutingApi(HEREApi):
    """A python interface into the HERE Routing API"""

    URL_CALCULATE_ROUTE = "https://route.ls.hereapi.com/routing/7.2/calculateroute.json"
    URL_CALCULATE_ROUTE_V8 = "https://router.hereapi.com/v8/routes"
    URL_CALCULATE_MATRIX = "https://matrix.router.hereapi.com/v8/matrix"

    def __init__(self, api_key: str = None, timeout: int = None):
        """Returns a RoutingApi instance.
        Args:
          api_key (str):
            API key taken from HERE Developer Portal.
          timeout (int):
            Timeout limit for requests.
        """

        super(RoutingApi, self).__init__(api_key, timeout)

    def __get(
        self,
        base_url,
        data,
        key,
        response_cls,
        manipulation_key: str = None,
        keys_for_manipulation: List = None,
    ):
        url = Utils.build_url(base_url, extra_params=data)
        if manipulation_key and keys_for_manipulation:
            for k in keys_for_manipulation:
                url = url.replace(k, manipulation_key)
        response = requests.get(url, timeout=self._timeout)
        json_data = json.loads(response.content.decode("utf8"))
        if response.status_code == requests.codes.OK:
            if json_data.get(key) is not None:
                return response_cls.new_from_jsondict(json_data)
            else:
                raise error_from_routing_service_error(json_data)
        else:
            raise HEREError(
                "Error occurred on routing_api __get "
                + sys._getframe(1).f_code.co_name
                + " response status code "
                + str(response.status_code)
            )

    @classmethod
    def __prepare_mode_values(cls, modes):
        mode_values = ""
        for mode in modes:
            mode_values += mode.__str__() + ";"
        mode_values = mode_values[:-1]
        return mode_values

    @classmethod
    def __list_to_waypoint(cls, waypoint_a):
        return str.format("geo!{0},{1}", waypoint_a[0], waypoint_a[1])

    def _route(self, waypoint_a, waypoint_b, modes=None, departure=None, arrival=None):
        if isinstance(waypoint_a, str):
            waypoint_a = self._get_coordinates_for_location_name(waypoint_a)
        if isinstance(waypoint_b, str):
            waypoint_b = self._get_coordinates_for_location_name(waypoint_b)
        data = {
            "waypoint0": self.__list_to_waypoint(waypoint_a),
            "waypoint1": self.__list_to_waypoint(waypoint_b),
            "mode": self.__prepare_mode_values(modes),
            "apikey": self._api_key,
        }
        if departure is not None and arrival is not None:
            raise HEREError("Specify either departure or arrival, not both.")
        if departure is not None:
            departure = self._convert_datetime_to_isoformat(departure)
            data["departure"] = departure
        if arrival is not None:
            arrival = self._convert_datetime_to_isoformat(arrival)
            data["arrival"] = arrival
        response = self.__get(
            self.URL_CALCULATE_ROUTE, data, "response", RoutingResponse
        )
        route = response.response["route"]
        maneuver = route[0]["leg"][0]["maneuver"]

        if any(mode in modes for mode in [RouteMode.car, RouteMode.truck]):
            # Get Route for Car and Truck
            response.route_short = self._get_route_from_vehicle_maneuver(maneuver)
        elif any(
            mode in modes
            for mode in [RouteMode.publicTransport, RouteMode.publicTransportTimeTable]
        ):
            # Get Route for Public Transport
            public_transport_line = route[0]["publicTransportLine"]
            response.route_short = self._get_route_from_public_transport_line(
                public_transport_line
            )
        elif any(mode in modes for mode in [RouteMode.pedestrian, RouteMode.bicycle]):
            # Get Route for Pedestrian and Biyclce
            response.route_short = self._get_route_from_non_vehicle_maneuver(maneuver)
        return response

    def bicycle_route(
        self,
        waypoint_a: Union[List[float], str],
        waypoint_b: Union[List[float], str],
        modes: List[RouteMode] = None,
        departure: str = "now",
    ) -> Optional[RoutingResponse]:
        """Request a bicycle route between two points
        Args:
          waypoint_a:
            List contains latitude and longitude in order
            or string with the location name
          waypoint_b:
            List contains latitude and longitude in order
            or string with the location name.
          modes (List):
            List contains RouteMode enums.
          departure (str):
            Date time str in format `yyyy-mm-ddThh:mm:ss`. Default `now`.
        Returns:
          RoutingResponse
        Raises:
          HEREError"""

        if modes is None:
            modes = [RouteMode.bicycle, RouteMode.fastest]
        return self._route(waypoint_a, waypoint_b, modes, departure)

    def car_route(
        self,
        waypoint_a: Union[List[float], str],
        waypoint_b: Union[List[float], str],
        modes: List[RouteMode] = None,
        departure: str = "now",
    ) -> Optional[RoutingResponse]:
        """Request a driving route between two points
        Args:
          waypoint_a (List):
            List contains latitude and longitude in order
            or string with the location name.
          waypoint_b (List):
            List contains latitude and longitude in order
            or string with the location name.
          modes (List):
            List contains RouteMode enums.
          departure (str):
            Date time str in format `yyyy-mm-ddThh:mm:ss`. Default `now`.
        Returns:
          RoutingResponse
        Raises:
          HEREError"""

        if modes is None:
            modes = [RouteMode.car, RouteMode.fastest]
        return self._route(waypoint_a, waypoint_b, modes, departure)

    def pedestrian_route(
        self,
        waypoint_a: Union[List[float], str],
        waypoint_b: Union[List[float], str],
        modes: List[RouteMode] = None,
        departure: str = "now",
    ) -> Optional[RoutingResponse]:
        """Request a pedestrian route between two points
        Args:
          waypoint_a (List):
            List contains latitude and longitude in order
            or string with the location name.
          waypoint_b (List):
            List contains latitude and longitude in order
            or string with the location name.
          modes (List):
            List contains RouteMode enums.
          departure (str):
            Date time str in format `yyyy-mm-ddThh:mm:ss`. Default `now`.
        Returns:
          RoutingResponse
        Raises:
          HEREError"""

        if modes is None:
            modes = [RouteMode.pedestrian, RouteMode.fastest]
        return self._route(waypoint_a, waypoint_b, modes, departure)

    def intermediate_route(
        self,
        waypoint_a: Union[List[float], str],
        waypoint_b: Union[List[float], str],
        waypoint_c: Union[List[float], str],
        modes: List[RouteMode] = None,
        departure: str = "now",
    ) -> Optional[RoutingResponse]:
        """Request a intermediate route from three points
        Args:
          waypoint_a (List):
            Starting List contains latitude and longitude in order
            or string with the location name.
          waypoint_b (List):
            Intermediate List contains latitude and longitude in order
            or string with the location name.
          waypoint_c (List):
            Last List contains latitude and longitude in order
            or string with the location name.
          modes (List):
            List contains RouteMode enums.
          departure (str):
            Date time str in format `yyyy-mm-ddThh:mm:ss`. Default `now`.
        Returns:
          RoutingResponse
        Raises:
          HEREError"""

        if modes is None:
            modes = [RouteMode.car, RouteMode.fastest]
        return self._route(waypoint_a, waypoint_b, modes, departure)

    def public_transport(
        self,
        waypoint_a: Union[List[float], str],
        waypoint_b: Union[List[float], str],
        combine_change: bool,
        modes: List[RouteMode] = None,
        departure="now",
    ) -> Optional[RoutingResponse]:
        """Request a public transport route between two points
        Args:
          waypoint_a (List):
            Starting List contains latitude and longitude in order
            or string with the location name.
          waypoint_b (List):
            Intermediate List contains latitude and longitude in order
            or string with the location name.
          combine_change (bool):
            Enables the change manuever in the route response, which
            indicates a public transit line change.
          modes (List):
            List contains RouteMode enums.
          departure (str):
            Date time str in format `yyyy-mm-ddThh:mm:ss`. Default `now`.
        Returns:
          RoutingResponse
        Raises:
          HEREError"""

        if modes is None:
            modes = [RouteMode.publicTransport, RouteMode.fastest]
        return self._route(waypoint_a, waypoint_b, modes, departure)

    def public_transport_timetable(
        self,
        waypoint_a: Union[List[float], str],
        waypoint_b: Union[List[float], str],
        combine_change: bool,
        modes: List[RouteMode] = None,
        departure: str = None,
        arrival: str = None,
    ) -> Optional[RoutingResponse]:
        """Request a public transport route between two points based on timetables
        Args:
          waypoint_a (List):
            Starting List contains latitude and longitude in order
            or string with the location name.
          waypoint_b (List):
            Intermediate List contains latitude and longitude in order
            or string with the location name.
          combine_change (bool):
            Enables the change manuever in the route response, which
            indicates a public transit line change.
          modes (List):
            List contains RouteMode enums.
          departure (str):
            Date time str in format `yyyy-mm-ddThh:mm:ss`. Default `None`.
          arrival (str):
            Date time str in format `yyyy-mm-ddThh:mm:ss`. Default `None`.
        Returns:
          RoutingResponse
        Raises:
          HEREError"""

        if modes is None:
            modes = [RouteMode.publicTransportTimeTable, RouteMode.fastest]
        return self._route(waypoint_a, waypoint_b, modes, departure, arrival)

    def location_near_motorway(
        self,
        waypoint_a: Union[List[float], str],
        waypoint_b: Union[List[float], str],
        modes: List[RouteMode] = None,
        departure: str = "now",
    ) -> Optional[RoutingResponse]:
        """Calculates the fastest car route between two location
        Args:
          waypoint_a (List):
            List contains latitude and longitude in order
            or string with the location name.
          waypoint_b (List):
            List contains latitude and longitude in order
            or string with the location name.
          modes (List):
            List contains RouteMode enums.
          departure (str):
            Date time str in format `yyyy-mm-ddThh:mm:ss`. Default `now`.
        Returns:
          RoutingResponse
        Raises:
          HEREError"""

        if modes is None:
            modes = [RouteMode.car, RouteMode.fastest]
        return self._route(waypoint_a, waypoint_b, modes, departure)

    def truck_route(
        self,
        waypoint_a: Union[List[float], str],
        waypoint_b: Union[List[float], str],
        modes: List[RouteMode] = None,
        departure: str = "now",
    ) -> Optional[RoutingResponse]:
        """Calculates the fastest truck route between two location
        Args:
          waypoint_a (List):
            List contains latitude and longitude in order
            or string with the location name.
          waypoint_b (List):
            List contains latitude and longitude in order
            or string with the location name.
          modes (List):
            List contains RouteMode enums.
          departure (str):
            Date time str in format `yyyy-mm-ddThh:mm:ss`. Default `now`.
        Returns:
          RoutingResponse
        Raises:
          HEREError"""

        if modes is None:
            modes = [RouteMode.truck, RouteMode.fastest]
        return self._route(waypoint_a, waypoint_b, modes, departure)

    def route_v8(
        self,
        transport_mode: RoutingTransportMode,
        origin: Union[List[float], str],
        destination: Union[List[float], str],
        via: Optional[List[List[float]]] = None,
        departure_time: Optional[str] = None,
        routing_mode: RoutingMode = RoutingMode.fast,
        alternatives: Optional[int] = None,
        avoid: Optional[Dict[str, List[str]]] = None,
        exclude: Optional[Dict[str, List[str]]] = None,
        units: Optional[RoutingMetric] = None,
        lang: Optional[str] = None,
        return_fields: List[RoutingApiReturnField] = [RoutingApiReturnField.polyline],
        span_fields: Optional[List[RoutingApiSpanField]] = None,
        truck: Optional[Dict[str, List[str]]] = None,
        scooter: Optional[Dict[str, str]] = None,
        headers: Optional[dict] = None,
    ) -> Optional[RoutingResponseV8]:
        """Calculates the route between given origin and destination.
        Args:
          transport_mode (RoutingTransportMode):
            Mode of transport to be used for the calculation of the route.
          origin (Union[List[float], str]):
            List contains latitude and longitude in order
            or string with the location name.
          destination (Union[List[float], str]):
            List contains latitude and longitude in order
            or string with the location name.
          via (Optional[List[List[float]]]):
            Locations defining via waypoints.
            Locations between origin and destination.
          departure_time (Optional[str]):
            Specifies the time of departure as defined by
            either date-time or full-date T partial-time in RFC 3339,
            section 5.6 (for example, 2019-06-24T01:23:45).
          routing_mode (RoutingMode):
            Specifies which optimization is applied during route calculation,
            fast as default value.
          alternatives (Optional[int]):
            Number of alternative routes to return aside from the optimal route.
          avoid (Optional[Dict[str, List[str]]]):
            Avoid routes that violate certain features of road network or
            that go through user-specified geographical bounding boxes.
            Sample use of parameter: `{"features": [controlledAccessHighway, tunnel]}`
          exclude (Optional[Dict[str, List[str]]]):
            Defines properties which will be strictly excluded from route calculation.
            Sample use of parameter:
            `{"countries": [A comma separated list of three-letter country codes (ISO-3166-1 alpha-3 code)]}`
          units (Optional[RoutingMetric]):
            Units of measurement used in guidance instructions. The default is metric.
          lang (Optional[str]):
            Default: "en-US"
            Specifies the preferred language of the response.
            The value should comply with the IETF BCP 47.
          return_fields (List[RoutingApiReturnField]):
            Defines which attributes are included in the response as part of data
            representation of a Route or Section.
          span_fields (Optional[List[RoutingApiSpanField]]):
            Defines which attributes are included in the response spans.
            For example, attributes,length will enable the fields attributes and length in the route response.
            This parameter also requires that the polyline option is set within the return parameter.
          truck (Optional[Dict[str, List[str]]]):
            Comma-separated list of shipped hazardous goods in the vehicle.
            Sample use of parameter: `{"shippedHazardousGoods": [explosive, gas, flammable]}`
          scooter (Optional[Dict[str, str]]):
            Scooter specific parameters.
            Sample use of parameter: `{"allowHighway": "true"}`
          headers (Optional[dict]):
            HTTP headers for requests.
            Sample:
            X-Request-ID
            User-provided token that can be used to trace a request or
            a group of requests sent to the service.
        Returns:
          RoutingResponseV8
        Raises:
          HEREError
        """

        if isinstance(origin, str):
            origin = self._get_coordinates_for_location_name(origin)
        if isinstance(destination, str):
            destination = self._get_coordinates_for_location_name(destination)
        data = {
            "transportMode": transport_mode.__str__(),
            "origin": str.format("{0},{1}", origin[0], origin[1]),
            "destination": str.format("{0},{1}", destination[0], destination[1]),
            "apiKey": self._api_key,
        }

        via_keys = []
        if via:
            for i, v in enumerate(via):
                key = str.format("{0}{1}", "via", i)
                via_keys.append(key)
                data[key] = str.format("{0},{1}", v[0], v[1])
        if departure_time:
            data["departureTime"] = departure_time
        data["routingMode"] = routing_mode.__str__()
        if alternatives:
            data["alternatives"] = alternatives
        if avoid:
            key = list(avoid.keys())[0]
            values = list(avoid.values())[0]
            data["avoid"] = {
                key: ",".join(values),
            }
        if exclude:
            key = list(avoid.keys())[0]
            values = list(avoid.values())[0]
            data["exclude"] = {
                key: ",".join(values),
            }
        if units:
            data["units"] = units.__str__()
        if lang:
            data["lang"] = lang
        if return_fields:
            data["return"] = ",".join([field.__str__() for field in return_fields])
        if span_fields:
            data["spans"] = ",".join([field.__str__() for field in span_fields])
        if truck:
            key = list(avoid.keys())[0]
            values = list(avoid.values())[0]
            data["truck"] = {
                key: ",".join(values),
            }
        if scooter:
            data["scooter"] = scooter

        response = self.__get(
            self.URL_CALCULATE_ROUTE_V8,
            data,
            "routes",
            RoutingResponseV8,
            manipulation_key="via",
            keys_for_manipulation=via_keys,
        )
        return response

    def __prepare_matrix_request_body(
        self,
        origins: Union[List[float], str],
        destinations: Union[List[float], str],
        matrix_type: MatrixRoutingType = MatrixRoutingType.world,
        center: Optional[List[float]] = None,
        radius: Optional[int] = None,
        profile: Optional[MatrixRoutingProfile] = None,
        departure: str = None,
        routing_mode: Optional[MatrixRoutingMode] = None,
        transport_mode: Optional[MatrixRoutingTransportMode] = None,
        avoid: Optional[Avoid] = None,
        truck: Optional[Truck] = None,
        matrix_attributes: Optional[List[MatrixSummaryAttribute]] = None,
    ) -> Dict:
        region_definition = {
            "type": matrix_type.__str__(),
        }
        if center:
            region_definition["center"] = {"lat": center[0], "lng": center[1]}
        if radius:
            region_definition["radius"] = radius
        request_body = {"regionDefinition": region_definition}

        if profile:
            request_body["profile"] = profile.__str__()
        if departure:
            request_body["departureTime"] = departure
        if routing_mode:
            request_body["routingMode"] = routing_mode.__str__()
        if transport_mode:
            request_body["transportMode"] = transport_mode.__str__()
        if matrix_attributes:
            request_body["matrixAttributes"] = [
                attribute.__str__() for attribute in matrix_attributes
            ]
        if avoid:
            request_body["avoid"] = {"features": avoid.features, "areas": avoid.areas}
        if truck:
            request_body["truck"] = {
                "shippedHazardousGoods": truck.shipped_hazardous_goods,
                "grossWeight": truck.gross_weight,
                "weightPerAxle": truck.weight_per_axle,
                "height": truck.height,
                "width": truck.width,
                "length": truck.length,
                "tunnelCategory": truck.tunnel_category,
                "axleCount": truck.axle_count,
                "type": truck.truck_type,
                "trailerCount": truck.trailer_count,
            }

        origin_list = []
        for i, origin in enumerate(origins):
            if isinstance(origin, str):
                origin_waypoint = self._get_coordinates_for_location_name(origin)
            else:
                origin_waypoint = origin
            lat_long = {"lat": origin_waypoint[0], "lng": origin_waypoint[1]}
            origin_list.append(lat_long)
        request_body["origins"] = origin_list

        destination_list = []
        for i, destination in enumerate(destinations):
            if isinstance(destination, str):
                destination_waypoint = self._get_coordinates_for_location_name(
                    destination
                )
            else:
                destination_waypoint = destination
            lat_long = {"lat": destination_waypoint[0], "lng": destination_waypoint[1]}
            destination_list.append(lat_long)
        request_body["destinations"] = destination_list

        return request_body

    def sync_matrix(
        self,
        origins: Union[List[float], str],
        destinations: Union[List[float], str],
        matrix_type: MatrixRoutingType = MatrixRoutingType.world,
        center: Optional[List[float]] = None,
        radius: Optional[int] = None,
        profile: Optional[MatrixRoutingProfile] = None,
        departure: str = None,
        routing_mode: Optional[MatrixRoutingMode] = None,
        transport_mode: Optional[MatrixRoutingTransportMode] = None,
        avoid: Optional[Avoid] = None,
        truck: Optional[Truck] = None,
        matrix_attributes: Optional[List[MatrixSummaryAttribute]] = None,
    ) -> Optional[RoutingMatrixResponse]:
        """Sync request a matrix of route summaries between M starts and N destinations.
        Args:
          origins (List):
            List of lists of coordinates [lat,long] of start waypoints.
            or list of string with the location names.
          destinations (List):
            List of lists of coordinates [lat,long] of destination waypoints.
            or list of string with the location names.
          matrix_type (MatrixRoutingType):
            Routing type used in definition of a region in which the matrix will be calculated.
          center (Optional[List]):
            Center of region definition, latitude and longitude.
          radius (Optional[int]):
            Center  of region definition.
          profile (Optional[MatrixRoutingProfile]):
            A profile ID enables the calculation of matrices with routes of arbitrary length.
          departure (str):
            time when travel is expected to start, e.g.: '2013-07-04T17:00:00+02'
          routing_mode (Optional[MatrixRoutingMode]):
            Route mode used in optimization of route calculation.
          transport_mode (Optional[MatrixRoutingTransportMode]):
            Depending on the transport mode special constraints, speed attributes and weights
            are taken into account during route calculation.
          avoid (Optional[Avoid]):
            Avoid routes that violate these properties.
          truck (Optional[Truck]):
            Different truck options to use during route calculation when transportMode = truck.
          matrix_attributes (List):
            List of MatrixSummaryAttribute enums.
        Returns:
          RoutingMatrixResponse
        Raises:
          HEREError: If an error is received from the server.
        """

        query_params = {
            "apiKey": self._api_key,
            "async": "false",
        }

        request_body = self.__prepare_matrix_request_body(
            origins=origins,
            destinations=destinations,
            matrix_type=matrix_type,
            center=center,
            radius=radius,
            profile=profile,
            departure=departure,
            routing_mode=routing_mode,
            transport_mode=transport_mode,
            avoid=avoid,
            truck=truck,
            matrix_attributes=matrix_attributes,
        )

        url = Utils.build_url(self.URL_CALCULATE_MATRIX, extra_params=query_params)
        headers = {"Content-Type": "application/json"}
        response = requests.post(
            url, json=request_body, headers=headers, timeout=self._timeout
        )
        json_data = json.loads(response.content.decode("utf8"))
        if response.status_code == requests.codes.OK:
            if json_data.get("matrix") is not None:
                return RoutingMatrixResponse.new_from_jsondict(json_data)
            else:
                raise HEREError(
                    "Error occurred on routing_api sync_matrix "
                    + sys._getframe(1).f_code.co_name
                    + " response status code "
                    + str(response.status_code)
                )
        else:
            if "title" in json_data and "cause" in json_data:
                raise HEREError(
                    str.format(
                        "routing_api sync_matrix failed! title: {0}, cause: {1}",
                        json_data["title"],
                        json_data["cause"],
                    )
                )
            else:
                raise HEREError(
                    "Error occurred on routing_api sync_matrix "
                    + sys._getframe(1).f_code.co_name
                )

    def __download_file(self, fileurl: str):
        filename = os.path.basename(fileurl)
        with requests.get(fileurl, stream=True) as r:
            r.raise_for_status()
            with open(filename, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        print("{} file saved!".format(filename))
        return filename

    def __is_correct_response(self, response):
        status_code = response.status_code
        json_data = response.json()
        if json_data.get("matrix") is not None:
            return json_data
        elif json_data.get("status") is not None:
            print(
                "Matrix {} calculation {}".format(
                    json_data["matrixId"], json_data["status"]
                )
            )
            return False
        elif json_data.get("error") is not None and json_data.get("error_description"):
            raise HEREError(
                "Error occurred on __is_correct_response: "
                + json_data["error"]
                + ", description: "
                + json_data["error_description"]
            )
        elif json_data.get("title") is not None and json_data.get("status"):
            raise HEREError(
                "Error occurred on __is_correct_response: "
                + json_data["title"]
                + ", status: "
                + json_data["status"]
            )

    def async_matrix(
        self,
        token: str,
        origins: Union[List[float], str],
        destinations: Union[List[float], str],
        matrix_type: MatrixRoutingType = MatrixRoutingType.world,
        center: Optional[List[float]] = None,
        radius: Optional[int] = None,
        profile: Optional[MatrixRoutingProfile] = None,
        departure: str = None,
        routing_mode: Optional[MatrixRoutingMode] = None,
        transport_mode: Optional[MatrixRoutingTransportMode] = None,
        avoid: Optional[Avoid] = None,
        truck: Optional[Truck] = None,
        matrix_attributes: Optional[List[MatrixSummaryAttribute]] = None,
    ) -> Optional[RoutingMatrixResponse]:
        """Async request a matrix of route summaries between M starts and N destinations.
        Args:
          token (str):
            Bearer token required for async calls. This is the only working solution for now.
            How to create a bearer token:
            https://developer.here.com/documentation/identity-access-management/dev_guide/topics/sdk.html#step-1-register-your-application
            https://developer.here.com/documentation/identity-access-management/dev_guide/topics/postman.html
          origins (List):
            List of lists of coordinates [lat,long] of start waypoints.
            or list of string with the location names.
          destinations (List):
            List of lists of coordinates [lat,long] of destination waypoints.
            or list of string with the location names.
          matrix_type (MatrixRoutingType):
            Routing type used in definition of a region in which the matrix will be calculated.
          center (Optional[List]):
            Center of region definition, latitude and longitude.
          radius (Optional[int]):
            Center  of region definition.
          profile (Optional[MatrixRoutingProfile]):
            A profile ID enables the calculation of matrices with routes of arbitrary length.
          departure (str):
            time when travel is expected to start, e.g.: '2013-07-04T17:00:00+02'
          routing_mode (Optional[MatrixRoutingMode]):
            Route mode used in optimization of route calculation.
          transport_mode (Optional[MatrixRoutingTransportMode]):
            Depending on the transport mode special constraints, speed attributes and weights
            are taken into account during route calculation.
          avoid (Optional[Avoid]):
            Avoid routes that violate these properties.
          truck (Optional[Truck]):
            Different truck options to use during route calculation when transportMode = truck.
          matrix_attributes (List):
            List of MatrixSummaryAttribute enums.
        Returns:
          RoutingMatrixResponse.
        Raises:
          HEREError: If an error is received from the server.
        """

        query_params = {}

        request_body = self.__prepare_matrix_request_body(
            origins=origins,
            destinations=destinations,
            matrix_type=matrix_type,
            center=center,
            radius=radius,
            profile=profile,
            departure=departure,
            routing_mode=routing_mode,
            transport_mode=transport_mode,
            avoid=avoid,
            truck=truck,
            matrix_attributes=matrix_attributes,
        )

        url = Utils.build_url(self.URL_CALCULATE_MATRIX, extra_params=query_params)
        headers = {
            "Content-Type": "application/json",
            "Authorization": str.format("Bearer {0}", token),
        }
        json_data = json.dumps(request_body)
        response = requests.post(
            url, json=request_body, headers=headers, timeout=self._timeout
        )
        if response.status_code == requests.codes.ACCEPTED:
            json_data = response.json()
            print(
                "Matrix {} calculation {}".format(
                    json_data["matrixId"], json_data["status"]
                )
            )
            poll_url = json_data["statusUrl"]
            headers = {"Authorization": str.format("Bearer {0}", token)}
            print("Polling matrix calculation started!")
            result = polling.poll(
                lambda: requests.get(poll_url, headers=headers),
                check_success=self.__is_correct_response,
                step=5,
                poll_forever=True,
            )
            print("Polling matrix calculation completed!")
            poll_data = result.json()
            return RoutingMatrixResponse.new_from_jsondict(poll_data)
        else:
            json_data = response.json()
            if (
                json_data.get("error") is not None
                and json_data.get("error_description") is not None
            ):
                raise HEREError(
                    "Error occurred on async_matrix: "
                    + json_data["error"]
                    + ", description: "
                    + json_data["error_description"]
                )
            elif (
                json_data.get("title") is not None
                and json_data.get("cause") is not None
            ):
                raise HEREError(
                    "Error occurred on async_matrix: "
                    + json_data["title"]
                    + ", cause: "
                    + json_data["cause"]
                )
            else:
                raise HEREError(
                    "Error occurred on async_matrix " + sys._getframe(1).f_code.co_name
                )

    def _get_coordinates_for_location_name(self, location_name: str) -> List[float]:
        """Use the Geocoder API to resolve a location name to a set of coordinates."""

        geocoder_api = GeocoderApi(self._api_key)
        try:
            geocoder_response = geocoder_api.free_form(location_name)
            coordinates = geocoder_response.items[0]["position"]
            return [coordinates["lat"], coordinates["lng"]]
        except (HEREError) as here_error:
            raise WaypointNotFoundError(here_error.message)

    @staticmethod
    def _convert_datetime_to_isoformat(datetime_object):
        """Convert a datetime.datetime object to an ISO8601 string."""

        if isinstance(datetime_object, datetime.datetime):
            datetime_object = datetime_object.isoformat()
        return datetime_object

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
    def _get_route_from_public_transport_line(public_transport_line_segment):
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

    if "error" in json_data:
        if json_data["error"] == "Unauthorized":
            return InvalidCredentialsError(json_data["error_description"])

    if "subtype" in json_data:
        subtype = json_data["subtype"]
        details = json_data["details"]

        if subtype == "InvalidInputData":
            return InvalidInputDataError(details)
        if subtype == "WaypointNotFound":
            return WaypointNotFoundError(details)
        if subtype == "NoRouteFound":
            return NoRouteFoundError(details)
        if subtype == "LinkIdNotFound":
            return LinkIdNotFoundError(details)
        if subtype == "RouteNotReconstructed":
            return RouteNotReconstructedError(details)
    # pylint: disable=W0212
    return HEREError("Error occurred on " + sys._getframe(1).f_code.co_name)
