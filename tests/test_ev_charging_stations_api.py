#!/usr/bin/env python

import json
import os
import time
import unittest

import responses

import herepy
from herepy.here_enum import EVStationConnectorTypes


class EVChargingStationsApiTest(unittest.TestCase):
    def setUp(self):
        api = herepy.EVChargingStationsApi(api_key="api_key")
        self._api = api

    def test_initiation(self):
        self.assertIsInstance(self._api, herepy.EVChargingStationsApi)
        self.assertEqual(self._api._api_key, "api_key")
        self.assertEqual(self._api._base_url, "https://ev-v2.cit.cc.api.here.com/ev/")

    @responses.activate
    def test_get_stations_circular_search_whensucceed(self):
        with open("testdata/models/ev_charging_stations_circular.json", "r") as f:
            expected_response = f.read()
        responses.add(
            responses.GET,
            "https://ev-v2.cit.cc.api.here.com/ev/stations.json",
            expected_response,
            status=200,
        )
        response = self._api.get_stations_circular_search(
            latitude=52.516667,
            longitude=13.383333,
            radius=5000,
            connectortypes=[
                EVStationConnectorTypes.small_paddle_inductive,
                EVStationConnectorTypes.large_paddle_inductive,
            ],
        )
        self.assertTrue(response)
        self.assertIsInstance(response, herepy.EVChargingStationsResponse)

    @responses.activate
    def test_get_stations_circular_search_whenerroroccurred(self):
        with open(
            "testdata/models/ev_charging_stations_error_unauthorized.json", "r"
        ) as f:
            expected_response = f.read()
        responses.add(
            responses.GET,
            "https://ev-v2.cit.cc.api.here.com/ev/stations.json",
            expected_response,
            status=200,
        )
        with self.assertRaises(herepy.HEREError):
            self._api.get_stations_circular_search(
                latitude=52.516667, longitude=13.383333, radius=5000
            )

    @responses.activate
    def test_get_stations_bounding_box_whensucceed(self):
        with open("testdata/models/ev_charging_stations_circular.json", "r") as f:
            expected_response = f.read()
        responses.add(
            responses.GET,
            "https://ev-v2.cit.cc.api.here.com/ev/stations.json",
            expected_response,
            status=200,
        )
        response = self._api.get_stations_bounding_box(
            top_left=[52.8, 11.37309],
            bottom_right=[52.31, 13.2],
            connectortypes=[
                EVStationConnectorTypes.small_paddle_inductive,
                EVStationConnectorTypes.large_paddle_inductive,
            ],
        )
        self.assertTrue(response)
        self.assertIsInstance(response, herepy.EVChargingStationsResponse)

    @responses.activate
    def test_get_stations_bounding_box_whenerroroccurred(self):
        with open(
            "testdata/models/ev_charging_stations_error_unauthorized.json", "r"
        ) as f:
            expected_response = f.read()
        responses.add(
            responses.GET,
            "https://ev-v2.cit.cc.api.here.com/ev/stations.json",
            expected_response,
            status=200,
        )
        with self.assertRaises(herepy.HEREError):
            self._api.get_stations_bounding_box(
                top_left=[52.8, 11.37309], bottom_right=[52.31, 13.2]
            )

    @responses.activate
    def test_get_stations_corridor_whensucceed(self):
        with open("testdata/models/ev_charging_stations_circular.json", "r") as f:
            expected_response = f.read()
        responses.add(
            responses.GET,
            "https://ev-v2.cit.cc.api.here.com/ev/stations.json",
            expected_response,
            status=200,
        )
        response = self._api.get_stations_corridor(
            points=[52.51666, 13.38333, 52.13333, 11.61666, 53.56527, 10.00138],
            connectortypes=[
                EVStationConnectorTypes.small_paddle_inductive,
                EVStationConnectorTypes.large_paddle_inductive,
            ],
        )
        self.assertTrue(response)
        self.assertIsInstance(response, herepy.EVChargingStationsResponse)

    @responses.activate
    def test_get_stations_corridor_whenerroroccurred(self):
        with open(
            "testdata/models/ev_charging_stations_error_unauthorized.json", "r"
        ) as f:
            expected_response = f.read()
        responses.add(
            responses.GET,
            "https://ev-v2.cit.cc.api.here.com/ev/stations.json",
            expected_response,
            status=200,
        )
        with self.assertRaises(herepy.HEREError):
            self._api.get_stations_corridor(
                points=[
                    52.51666,
                    13.38333,
                    52.13333,
                    11.61666,
                    53.56527,
                    10.00138,
                    11.0,
                ]
            )

    @responses.activate
    def test_get_station_details_whensucceed(self):
        station_id = "276u33db-b2c840878cfc409fa5a0aef858419037"
        with open("testdata/models/ev_charging_station_details.json", "r") as f:
            expected_response = f.read()
        responses.add(
            responses.GET,
            "https://ev-v2.cit.cc.api.here.com/ev/stations/" + station_id + ".json",
            expected_response,
            status=200,
        )
        response = self._api.get_station_details(station_id=station_id)
        self.assertTrue(response)
        self.assertIsInstance(response, herepy.EVChargingStationsResponse)

    @responses.activate
    def test_get_station_details_whenerroroccurred(self):
        station_id = "276u33db-b2c840878cfc409fa5a0aef858419037"
        with open(
            "testdata/models/ev_charging_stations_error_unauthorized.json", "r"
        ) as f:
            expected_response = f.read()
        responses.add(
            responses.GET,
            "https://ev-v2.cit.cc.api.here.com/ev/stations/" + station_id + ".json",
            expected_response,
            status=200,
        )
        with self.assertRaises(herepy.HEREError):
            self._api.get_station_details(station_id=station_id)
