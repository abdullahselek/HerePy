#!/usr/bin/env python

import os
import time
import unittest
import json
import responses
import herepy

class DestinationWeatherApiTest(unittest.TestCase):

    def setUp(self):
        api = herepy.DestinationWeatherApi('app_id', 'app_code')
        self._api = api

    def test_initiation(self):
        self.assertIsInstance(self._api, herepy.DestinationWeatherApi)
        self.assertEqual(self._api._app_id, 'app_id')
        self.assertEqual(self._api._app_code, 'app_code')
        self.assertEqual(self._api._base_url, 'https://weather.api.here.com/weather/1.0/report.json')

    @responses.activate
    def test_forecast_astronomy_whensucceed(self):
        with open('testdata/models/destination_weather.json', 'r') as f:
            expectedResponse = f.read()
        responses.add(responses.GET, 'https://weather.api.here.com/weather/1.0/report.json',
                  expectedResponse, status=200)
        response = self._api.forecast_astronomy('London')
        self.assertTrue(response)
        self.assertIsInstance(response, herepy.DestinationWeatherResponse)

    @responses.activate
    def test_forecast_astronomy_whenerroroccured(self):
        with open('testdata/models/destination_weather_error.json', 'r') as f:
            expectedResponse = f.read()
        responses.add(responses.GET, 'https://weather.api.here.com/weather/1.0/report.json',
                  expectedResponse, status=200)
        response = self._api.forecast_astronomy('London')
        self.assertIsInstance(response, herepy.HEREError)
