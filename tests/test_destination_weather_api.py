#!/usr/bin/env python

import json
import os
import time
import unittest

import responses

from herepy import (DestinationWeatherApi, DestinationWeatherResponse,
                    InvalidRequestError, UnauthorizedError, WeatherProductType)


class DestinationWeatherApiTest(unittest.TestCase):
    def setUp(self):
        api = DestinationWeatherApi("api_key")
        self._api = api

    def test_initiation(self):
        self.assertIsInstance(self._api, DestinationWeatherApi)
        self.assertEqual(self._api._api_key, "api_key")
        self.assertEqual(
            self._api._base_url,
            "https://weather.cc.api.here.com/weather/1.0/report.json",
        )

    @responses.activate
    def test_invalid_request_is_thrown(self):
        with open(
            "testdata/models/destination_weather_error_invalid_request.json", "r"
        ) as f:
            expectedResponse = f.read()
        responses.add(
            responses.GET,
            "https://weather.cc.api.here.com/weather/1.0/report.json",
            expectedResponse,
            status=200,
        )
        product = WeatherProductType.forecast_7days
        name = "Berlin"
        with self.assertRaises(InvalidRequestError):
            self._api.weather_for_location_name(name, product)

    @responses.activate
    def test_unauthorized_is_thrown(self):
        with open(
            "testdata/models/destination_weather_error_unauthorized.json", "r"
        ) as f:
            expectedResponse = f.read()
        responses.add(
            responses.GET,
            "https://weather.cc.api.here.com/weather/1.0/report.json",
            expectedResponse,
            status=200,
        )
        product = WeatherProductType.forecast_7days
        name = "Berlin"
        with self.assertRaises(UnauthorizedError):
            self._api.weather_for_location_name(name, product)

    @responses.activate
    def test_weather_for_location_name(self):
        with open("testdata/models/destination_weather_forecasts.json", "r") as f:
            expectedResponse = f.read()
        responses.add(
            responses.GET,
            "https://weather.cc.api.here.com/weather/1.0/report.json",
            expectedResponse,
            status=200,
        )
        product = WeatherProductType.forecast_7days
        name = "Berlin"
        response = self._api.weather_for_location_name(name, product)
        self.assertTrue(response)
        self.assertIsInstance(response, DestinationWeatherResponse)

    @responses.activate
    def test_weather_for_coordinates(self):
        with open("testdata/models/destination_weather_forecasts.json", "r") as f:
            expectedResponse = f.read()
        responses.add(
            responses.GET,
            "https://weather.cc.api.here.com/weather/1.0/report.json",
            expectedResponse,
            status=200,
        )
        product = WeatherProductType.forecast_7days
        latitude = 52.51784
        longitude = 13.38736
        response = self._api.weather_for_coordinates(latitude, longitude, product)
        self.assertTrue(response)
        self.assertIsInstance(response, DestinationWeatherResponse)

    @responses.activate
    def test_weather_for_zip_code(self):
        with open("testdata/models/destination_weather_forecasts.json", "r") as f:
            expectedResponse = f.read()
        responses.add(
            responses.GET,
            "https://weather.cc.api.here.com/weather/1.0/report.json",
            expectedResponse,
            status=200,
        )
        product = WeatherProductType.forecast_7days
        zip_code = "10025"
        response = self._api.weather_for_zip_code(zip_code, product)
        self.assertTrue(response)
        self.assertIsInstance(response, DestinationWeatherResponse)

    @responses.activate
    def test_weather_product_type_alerts(self):
        with open("testdata/models/destination_weather_alerts.json", "r") as f:
            expectedResponse = f.read()
        responses.add(
            responses.GET,
            "https://weather.cc.api.here.com/weather/1.0/report.json",
            expectedResponse,
            status=200,
        )
        product = WeatherProductType.alerts
        zip_code = "10025"
        response = self._api.weather_for_zip_code(zip_code, product)
        self.assertTrue(response)
        self.assertIsInstance(response, DestinationWeatherResponse)

    @responses.activate
    def test_weather_product_type_forecast_7days(self):
        with open("testdata/models/destination_weather_forecasts.json", "r") as f:
            expectedResponse = f.read()
        responses.add(
            responses.GET,
            "https://weather.cc.api.here.com/weather/1.0/report.json",
            expectedResponse,
            status=200,
        )
        product = WeatherProductType.forecast_7days
        zip_code = "10025"
        response = self._api.weather_for_zip_code(zip_code, product)
        self.assertTrue(response)
        self.assertIsInstance(response, DestinationWeatherResponse)

    @responses.activate
    def test_weather_product_type_forecast_7days_simple(self):
        with open(
            "testdata/models/destination_weather_forecasts_simple.json", "r"
        ) as f:
            expectedResponse = f.read()
        responses.add(
            responses.GET,
            "https://weather.cc.api.here.com/weather/1.0/report.json",
            expectedResponse,
            status=200,
        )
        product = WeatherProductType.forecast_7days_simple
        zip_code = "10025"
        response = self._api.weather_for_zip_code(zip_code, product)
        self.assertTrue(response)
        self.assertIsInstance(response, DestinationWeatherResponse)

    @responses.activate
    def test_weather_product_type_forecast_astronomy(self):
        with open(
            "testdata/models/destination_weather_forecasts_astronomy.json", "r"
        ) as f:
            expectedResponse = f.read()
        responses.add(
            responses.GET,
            "https://weather.cc.api.here.com/weather/1.0/report.json",
            expectedResponse,
            status=200,
        )
        product = WeatherProductType.forecast_astronomy
        zip_code = "10025"
        response = self._api.weather_for_zip_code(zip_code, product)
        self.assertTrue(response)
        self.assertIsInstance(response, DestinationWeatherResponse)

    @responses.activate
    def test_weather_product_type_forecast_hourly(self):
        with open(
            "testdata/models/destination_weather_forecasts_hourly.json", "r"
        ) as f:
            expectedResponse = f.read()
        responses.add(
            responses.GET,
            "https://weather.cc.api.here.com/weather/1.0/report.json",
            expectedResponse,
            status=200,
        )
        product = WeatherProductType.forecast_hourly
        zip_code = "10025"
        response = self._api.weather_for_zip_code(zip_code, product)
        self.assertTrue(response)
        self.assertIsInstance(response, DestinationWeatherResponse)

    @responses.activate
    def test_weather_product_type_nws_alerts(self):
        with open(
            "testdata/models/destination_weather_forecasts_nsw_alerts.json", "r"
        ) as f:
            expectedResponse = f.read()
        responses.add(
            responses.GET,
            "https://weather.cc.api.here.com/weather/1.0/report.json",
            expectedResponse,
            status=200,
        )
        product = WeatherProductType.nws_alerts
        zip_code = "10025"
        response = self._api.weather_for_zip_code(zip_code, product)
        self.assertTrue(response)
        self.assertIsInstance(response, DestinationWeatherResponse)
