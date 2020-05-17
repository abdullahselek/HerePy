#!/usr/bin/env python

import os
import time
import unittest
import json
import responses
import herepy

from herepy.here_enum import EVStationConnectorTypes


class EVChargingStationsApi(unittest.TestCase):

    def setUp(self):
        api = herepy.EVChargingStationsApi(app_id='app_id', app_code='app_code')
        self._api = api


    def test_initiation(self):
        self.assertIsInstance(self._api, herepy.EVChargingStationsApi)
        self.assertEqual(self._api._app_id, 'app_id')
        self.assertEqual(self._api._app_code, 'app_code')
        self.assertEqual(self._api._base_url, 'https://ev-v2.cit.cc.api.here.com/ev/')


    @responses.activate
    def test_get_stations_circular_search_whensucceed(self):
        with open('testdata/models/ev_charging_stations_circular.json', 'r') as f:
            expected_response = f.read()
        responses.add(responses.GET, 'https://ev-v2.cit.cc.api.here.com/ev/stations.json',
                  expected_response, status=200)
        response = self._api.get_stations_circular_search(latitude=52.516667,
                                                          longitude=13.383333,
                                                          radius=5000,
                                                          connectortypes=[EVStationConnectorTypes.small_paddle_inductive,
                                                    EVStationConnectorTypes.large_paddle_inductive])
        self.assertTrue(response)
        self.assertIsInstance(response, herepy.EVChargingStationsResponse)
