#!/usr/bin/env python

"""Module for the HERE Destination Weather API."""

import json
import sys

import requests

from herepy.error import HEREError, InvalidRequestError, UnauthorizedError
from herepy.here_api import HEREApi
from herepy.here_enum import WeatherProductType
from herepy.models import DestinationWeatherResponse
from herepy.utils import Utils


class DestinationWeatherApi(HEREApi):
    """A python interface into the HERE Destination Weather API."""

    def __init__(self, api_key: str = None, timeout: int = None):
        """
        Initialize a DestinationWeatherApi instance.

        Args:
          api_key (str):
            API key taken from HERE Developer Portal.
          timeout (int):
            Timeout limit for requests.

        """
        super().__init__(api_key, timeout)
        self._base_url = "https://weather.cc.api.here.com/weather/1.0/report.json"

    def _get(self, data, product):
        url = Utils.build_url(self._base_url, extra_params=data)
        response = requests.get(url, timeout=self._timeout)
        json_data = json.loads(response.content.decode("utf8"))
        if json_data.get(self._product_node(product)) is not None:
            return DestinationWeatherResponse.new_from_jsondict(json_data, param_defaults={self._product_node(product): None})
        else:
            error = self._get_error_from_response(json_data)
            raise error

    def _get_error_from_response(self, json_data):
        if "error" in json_data:
            if json_data["error"] == "Unauthorized":
                return UnauthorizedError(json_data["error_description"])
        error_type = json_data.get("Type")
        error_message = json_data.get("Message", "Error occurred on " + sys._getframe(1).f_code.co_name)
        if error_type == "Invalid Request":
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
        self,
        location_name: str,
        product: WeatherProductType,
        one_observation: bool = True,
        metric: bool = True,
    ) -> DestinationWeatherResponse | None:
        """
        Request the product for given location name.

        Args:
          location_name (str):
            Location name.
          product (WeatherProductType):
            A WeatherProductType identifying the type of report to obtain.
          one_observation (bool):
            Limit the result to the best mapped weather station.
          metric (bool):
            Use the metric system.

        Returns:
          DestinationWeatherResponse
        Raises:
          HEREError

        """
        data = {
            "apiKey": self._api_key,
            "product": product.__str__(),
            "oneobservation": "true" if one_observation else "false",
            "metric": "true" if metric else "false",
            "name": location_name,
        }
        return self._get(data, product)

    def weather_for_zip_code(
        self,
        zip_code: int,
        product: WeatherProductType,
        one_observation: bool = True,
        metric: bool = True,
    ) -> DestinationWeatherResponse | None:
        """
        Request the product for given zip code.

        Args:
          zip_code (int):
            U.S. zip code.
          product (WeatherProductType):
            A WeatherProductType identifying the type of report to obtain.
          one_observation (bool):
            Limit the result to the best mapped weather station.
          metric (bool):
            Use the metric system.

        Returns:
          DestinationWeatherResponse
        Raises:
          HEREError

        """
        data = {
            "apiKey": self._api_key,
            "product": product.__str__(),
            "oneobservation": "true" if one_observation else "false",
            "metric": "true" if metric else "false",
            "zipcode": zip_code,
        }
        return self._get(data, product)

    def weather_for_coordinates(
        self,
        latitude: float,
        longitude: float,
        product: WeatherProductType,
        one_observation: bool = True,
        metric: bool = True,
    ) -> DestinationWeatherResponse | None:
        """
        Request the product for given coordinates.

        Args:
          latitude (float):
            Latitude.
          longitude (float):
            Longitude.
          product (WeatherProductType):
            A WeatherProductType identifying the type of report to obtain.
          one_observation (bool):
            Limit the result to the best mapped weather station.
          metric (bool):
            Use the metric system.

        Returns:
          DestinationWeatherResponse
        Raises:
          HEREError

        """
        data = {
            "apiKey": self._api_key,
            "product": product.__str__(),
            "oneobservation": "true" if one_observation else "false",
            "metric": "true" if metric else "false",
            "latitude": latitude,
            "longitude": longitude,
        }
        return self._get(data, product)

    async def _get_async(self, data, product):
        url = Utils.build_url(self._base_url, extra_params=data)
        response = await self._get_async_client().get(url, timeout=self._timeout)
        json_data = json.loads(response.content.decode("utf8"))
        if json_data.get(self._product_node(product)) is not None:
            return DestinationWeatherResponse.new_from_jsondict(json_data, param_defaults={self._product_node(product): None})
        else:
            error = self._get_error_from_response(json_data)
            raise error

    async def async_weather_for_location_name(
        self,
        location_name: str,
        product: WeatherProductType,
        one_observation: bool = True,
        metric: bool = True,
    ) -> DestinationWeatherResponse | None:
        """
        Request the product for given location name.

        Args:
          location_name (str):
            Location name.
          product (WeatherProductType):
            A WeatherProductType identifying the type of report to obtain.
          one_observation (bool):
            Limit the result to the best mapped weather station.
          metric (bool):
            Use the metric system.

        Returns:
          DestinationWeatherResponse
        Raises:
          HEREError

        """
        data = {
            "apiKey": self._api_key,
            "product": product.__str__(),
            "oneobservation": "true" if one_observation else "false",
            "metric": "true" if metric else "false",
            "name": location_name,
        }
        return await self._get_async(data, product)

    async def async_weather_for_zip_code(
        self,
        zip_code: int,
        product: WeatherProductType,
        one_observation: bool = True,
        metric: bool = True,
    ) -> DestinationWeatherResponse | None:
        """
        Request the product for given zip code.

        Args:
          zip_code (int):
            U.S. zip code.
          product (WeatherProductType):
            A WeatherProductType identifying the type of report to obtain.
          one_observation (bool):
            Limit the result to the best mapped weather station.
          metric (bool):
            Use the metric system.

        Returns:
          DestinationWeatherResponse
        Raises:
          HEREError

        """
        data = {
            "apiKey": self._api_key,
            "product": product.__str__(),
            "oneobservation": "true" if one_observation else "false",
            "metric": "true" if metric else "false",
            "zipcode": zip_code,
        }
        return await self._get_async(data, product)

    async def async_weather_for_coordinates(
        self,
        latitude: float,
        longitude: float,
        product: WeatherProductType,
        one_observation: bool = True,
        metric: bool = True,
    ) -> DestinationWeatherResponse | None:
        """
        Request the product for given coordinates.

        Args:
          latitude (float):
            Latitude.
          longitude (float):
            Longitude.
          product (WeatherProductType):
            A WeatherProductType identifying the type of report to obtain.
          one_observation (bool):
            Limit the result to the best mapped weather station.
          metric (bool):
            Use the metric system.

        Returns:
          DestinationWeatherResponse
        Raises:
          HEREError

        """
        data = {
            "apiKey": self._api_key,
            "product": product.__str__(),
            "oneobservation": "true" if one_observation else "false",
            "metric": "true" if metric else "false",
            "latitude": latitude,
            "longitude": longitude,
        }
        return await self._get_async(data, product)
