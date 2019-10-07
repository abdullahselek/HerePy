#!/usr/bin/env python

from __future__ import division

import sys
import json
import requests

from herepy.here_api import HEREApi
from herepy.utils import Utils
from herepy.error import HEREError
from herepy.models import DestinationWeatherResponse
from herepy.here_enum import WeatherProductType


class DestinationWeatherApi(HEREApi):
    """A python interface into the HERE Destination Weather API"""

    def __init__(self, app_id=None, app_code=None, timeout=None):
        """Returns a DestinationWeatherApi instance.
        Args:
          app_id (str):
            App Id taken from HERE Developer Portal.
          app_code (str):
            App Code taken from HERE Developer Portal.
          timeout (int):
            Timeout limit for requests.
        """

        super(DestinationWeatherApi, self).__init__(app_id, app_code, timeout)
        self._base_url = "https://weather.api.here.com/weather/1.0/report.json"

    def _get(self, data, product):
        url = Utils.build_url(self._base_url, extra_params=data)
        response = requests.get(url, timeout=self._timeout)
        json_data = json.loads(response.content.decode("utf8"))
        if json_data.get(self._product_node(product)) != None:
            return DestinationWeatherResponse.new_from_jsondict(
                json_data, param_defaults={self._product_node(product): None}
            )
        else:
            error = self._get_error_from_response(json_data)
            raise error

    def _get_error_from_response(self, json_data):
        error_type = json_data.get("Type")
        error_message = json_data.get(
            "Message", "Error occured on " + sys._getframe(1).f_code.co_name
        )
        if error_type == "Unauthorized":
            return UnauthorizedError(error_message)
        elif error_type == "Invalid Request":
            return InvalidRequestError(error_message)
        else:
            return HEREError(error_message)

    def _product_node(self, product):
        if product == WeatherProductType.observation:
            return "observations"
        elif product == WeatherProductType.forecast_7days:
            return "forecasts"
        elif product == WeatherProductType.forecast_7days_simple:
            return "dailyForecasts"
        elif product == WeatherProductType.forecast_hourly:
            return "hourlyForecasts"
        elif product == WeatherProductType.forecast_astronomy:
            return "astronomy"
        elif product == WeatherProductType.alerts:
            return "alerts"
        else:
            return "nwsAlerts"

    def weather_for_location_name(
        self, location_name, product, one_observation=True, metric=True
    ):
        """Request the product for given location name.
        Args:
          location_name (str):
            Location name.
          one_observation (bool):
            Limit the result to the best mapped weather station.
          metric (bool):
            Use the metric system.
          product (WeatherProductType):
            A WeatherProductType identifying the type of report to obtain.
        Returns:
          DestinationWeatherResponse
        Raises:
          HEREError
        """

        data = {
            "app_id": self._app_id,
            "app_code": self._app_code,
            "product": product.__str__(),
            "oneobservation": one_observation,
            "metric": metric,
            "name": location_name,
        }
        return self._get(data, product)

    def weather_for_zip_code(
        self, zip_code, product, one_observation=True, metric=True
    ):
        """Request the product for given location name.
        Args:
          zip_code (int):
            U.S. zip code.
          one_observation (bool):
            Limit the result to the best mapped weather station.
          metric (bool):
            Use the metric system.
          product (WeatherProductType):
            A WeatherProductType identifying the type of report to obtain.
        Returns:
          DestinationWeatherResponse
        Raises:
          HEREError
        """

        data = {
            "app_id": self._app_id,
            "app_code": self._app_code,
            "product": product.__str__(),
            "oneobservation": one_observation,
            "metric": metric,
            "zipcode": zip_code,
        }
        return self._get(data, product)

    def weather_for_coordinates(
        self, latitude, longitude, product, one_observation=True, metric=True
    ):
        """Request the product for given location name.
        Args:
          latitude (float):
            Latitude.
          longitude (float):
            Longitude.
          one_observation (bool):
            Limit the result to the best mapped weather station.
          metric (bool):
            Use the metric system.
          product (WeatherProductType):
            A WeatherProductType identifying the type of report to obtain.
        Returns:
          DestinationWeatherResponse
        Raises:
          HEREError
        """

        data = {
            "app_id": self._app_id,
            "app_code": self._app_code,
            "product": product.__str__(),
            "oneobservation": one_observation,
            "metric": metric,
            "latitude": latitude,
            "longitude": longitude,
        }
        return self._get(data, product)


class UnauthorizedError(HEREError):

    """Unauthorized Error Type.

    Indicates authentication failure, invalid credentials were supplied.
    """


class InvalidRequestError(HEREError):

    """Invalid Request Error Type.

    Indicates an invalid or missing parameter value in the request, for example value given for the product parameter does not exist.
    """
