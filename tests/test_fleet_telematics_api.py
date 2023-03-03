#!/usr/bin/env python

import json
import os
import time
import unittest

import responses

import herepy


class FleetTelematicsApiTest(unittest.TestCase):
    def setUp(self):
        api = herepy.FleetTelematicsApi("api_key")
        self._api = api

    def test_initiation(self):
        self.assertIsInstance(self._api, herepy.FleetTelematicsApi)
        self.assertEqual(self._api._api_key, "api_key")
        self.assertEqual(self._api._base_url, "https://wse.ls.hereapi.com/2/")

    @responses.activate
    def test_find_sequence_whensucceed(self):
        with open("testdata/models/fleet_telematics_find_sequence.json", "r") as f:
            expected_response = f.read()
        responses.add(
            responses.GET,
            "https://wse.ls.hereapi.com/2/findsequence.json",
            expected_response,
            status=200,
        )
        start = str.format("{0};{1},{2}", "WiesbadenCentralStation", 50.0715, 8.2434)
        intermediate_destinations = [
            str.format("{0};{1},{2}", "FranfurtCentralStation", 50.1073, 8.6647),
            str.format("{0};{1},{2}", "DarmstadtCentralStation", 49.8728, 8.6326),
            str.format("{0};{1},{2}", "FrankfurtAirport", 50.0505, 8.5698),
        ]
        end = str.format("{0};{1},{2}", "MainzCentralStation", 50.0021, 8.259)
        modes = [
            herepy.RouteMode.fastest,
            herepy.RouteMode.car,
            herepy.RouteMode.traffic_enabled,
        ]
        response = self._api.find_sequence(
            start=start,
            departure="2014-12-09T09:30:00%2b01:00",
            intermediate_destinations=intermediate_destinations,
            end=end,
            modes=modes,
        )
        self.assertTrue(response)
        self.assertIsInstance(response, herepy.WaypointSequenceResponse)

    @responses.activate
    def test_find_sequence_whenerroroccurred(self):
        with open("testdata/models/fleet_telematics_unauthorized_error.json", "r") as f:
            expected_response = f.read()
        responses.add(
            responses.GET,
            "https://wse.ls.hereapi.com/2/findsequence.json",
            expected_response,
            status=200,
        )

        start = str.format("{0};{1},{2}", "WiesbadenCentralStation", 50.0715, 8.2434)
        intermediate_destinations = [
            str.format("{0};{1},{2}", "FranfurtCentralStation", 50.1073, 8.6647),
            str.format("{0};{1},{2}", "DarmstadtCentralStation", 49.8728, 8.6326),
            str.format("{0};{1},{2}", "FrankfurtAirport", 50.0505, 8.5698),
        ]
        end = str.format("{0};{1},{2}", "MainzCentralStation", 50.0021, 8.259)
        modes = [
            herepy.RouteMode.fastest,
            herepy.RouteMode.car,
            herepy.RouteMode.traffic_enabled,
        ]

        with self.assertRaises(herepy.HEREError):
            self._api.find_sequence(
                start=start,
                departure="2014-12-09T09:30:00%2b01:00",
                intermediate_destinations=intermediate_destinations,
                end=end,
                modes=modes,
            )

    @responses.activate
    def test_find_pickups_whensucceed(self):
        with open("testdata/models/fleet_telematics_find_pickups.json", "r") as f:
            expected_response = f.read()
        responses.add(
            responses.GET,
            "https://wse.ls.hereapi.com/2/findpickups.json",
            expected_response,
            status=200,
        )

        modes = [
            herepy.RouteMode.fastest,
            herepy.RouteMode.car,
            herepy.RouteMode.traffic_enabled,
        ]
        start = str.format(
            "{0},{1};{2}:{3},value:{4}",
            50.115620,
            8.631210,
            herepy.MultiplePickupOfferType.pickup.__str__(),
            "GRAPEFRUITS",
            1000,
        )
        departure = "2016-10-14T07:30:00+02:00"
        capacity = 10000
        vehicle_cost = 0.29
        driver_cost = 20
        max_detour = 60
        rest_times = "disabled"
        intermediate_destinations = [
            str.format(
                "{0},{1};{2}:{3},value:{4}",
                50.118578,
                8.636551,
                herepy.MultiplePickupOfferType.drop.__str__(),
                "APPLES",
                30,
            ),
            str.format(
                "{0},{1};{2}:{3}",
                50.122540,
                8.631070,
                herepy.MultiplePickupOfferType.pickup.__str__(),
                "BANANAS",
            ),
        ]
        end = str.format("{1},{2}", "MainzCentralStation", 50.132540, 8.649280)
        response = self._api.find_pickups(
            modes=modes,
            start=start,
            departure=departure,
            capacity=capacity,
            vehicle_cost=vehicle_cost,
            driver_cost=driver_cost,
            max_detour=max_detour,
            rest_times=rest_times,
            intermediate_destinations=intermediate_destinations,
            end=end,
        )
        self.assertTrue(response)
        self.assertIsInstance(response, herepy.WaypointSequenceResponse)

    @responses.activate
    def test_find_pickups_whenerroroccurred(self):
        with open("testdata/models/fleet_telematics_unauthorized_error.json", "r") as f:
            expected_response = f.read()
        responses.add(
            responses.GET,
            "https://wse.ls.hereapi.com/2/findpickups.json",
            expected_response,
            status=200,
        )

        modes = [
            herepy.RouteMode.fastest,
            herepy.RouteMode.car,
            herepy.RouteMode.traffic_enabled,
        ]
        start = str.format(
            "{0},{1};{2}:{3},value:{4}",
            50.115620,
            8.631210,
            herepy.MultiplePickupOfferType.pickup.__str__(),
            "GRAPEFRUITS",
            1000,
        )
        departure = "2016-10-14T07:30:00+02:00"
        capacity = 10000
        vehicle_cost = 0.29
        driver_cost = 20
        max_detour = 60
        rest_times = "disabled"
        intermediate_destinations = [
            str.format(
                "{0},{1};{2}:{3},value:{4}",
                50.118578,
                8.636551,
                herepy.MultiplePickupOfferType.drop.__str__(),
                "APPLES",
                30,
            ),
            str.format(
                "{0},{1};{2}:{3}",
                50.122540,
                8.631070,
                herepy.MultiplePickupOfferType.pickup.__str__(),
                "BANANAS",
            ),
        ]
        end = str.format("{1},{2}", "MainzCentralStation", 50.132540, 8.649280)

        with self.assertRaises(herepy.HEREError):
            self._api.find_pickups(
                modes=modes,
                start=start,
                departure=departure,
                capacity=capacity,
                vehicle_cost=vehicle_cost,
                driver_cost=driver_cost,
                max_detour=max_detour,
                rest_times=rest_times,
                intermediate_destinations=intermediate_destinations,
                end=end,
            )
