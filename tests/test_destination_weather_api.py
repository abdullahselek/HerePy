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
