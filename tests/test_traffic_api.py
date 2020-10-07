#!/usr/bin/env python

import datetime
import os
import sys
import unittest
import responses
import codecs
import herepy


class TrafficApiTest(unittest.TestCase):
    def setUp(self):
        api = herepy.TrafficApi("api_key")
        self._api = api

    def test_initiation(self):
        self.assertIsInstance(self._api, herepy.TrafficApi)
        self.assertEqual(self._api._api_key, "api_key")

    @responses.activate
    def test_incidents_in_bounding_box_success(self):
        with codecs.open(
            "testdata/models/traffic_incidents_bounding_box.json",
            mode="r",
            encoding="utf-8",
        ) as f:
            expectedResponse = f.read()
        responses.add(
            responses.GET,
            "https://traffic.ls.hereapi.com/traffic/6.0/incidents.json",
            expectedResponse,
            status=200,
        )
        response = self._api.incidents_in_bounding_box(
            top_left=[52.5311, 13.3644],
            bottom_right=[52.5114, 13.4035],
            criticality=[
                herepy.IncidentsCriticalityStr.minor,
                herepy.IncidentsCriticalityStr.major,
                herepy.IncidentsCriticalityStr.critical,
            ],
        )
        self.assertTrue(response)
        self.assertIsInstance(response, herepy.TrafficIncidentResponse)
        self.assertIsNotNone(response.as_dict())

    @responses.activate
    def test_incidents_in_bounding_box_fails(self):
        with codecs.open(
            "testdata/models/traffic_incidents_error.json", mode="r", encoding="utf-8"
        ) as f:
            expectedResponse = f.read()
        responses.add(
            responses.GET,
            "https://traffic.ls.hereapi.com/traffic/6.0/incidents.json",
            expectedResponse,
            status=200,
        )
        with self.assertRaises(herepy.UnauthorizedError):
            self._api.incidents_in_bounding_box(
                top_left=[52.5311, 13.3644],
                bottom_right=[52.5114, 13.4035],
                criticality=[herepy.IncidentsCriticalityStr.minor],
            )

    @responses.activate
    def test_incidents_in_corridor_success(self):
        with codecs.open(
            "testdata/models/traffic_incidents_corridor.json",
            mode="r",
            encoding="utf-8",
        ) as f:
            expectedResponse = f.read()
        responses.add(
            responses.GET,
            "https://traffic.ls.hereapi.com/traffic/6.0/incidents.json",
            expectedResponse,
            status=200,
        )
        response = self._api.incidents_in_corridor(
            points=[[51.5072, -0.1275], [51.50781, -0.13112], [51.51006, -0.1346]],
            width=1000,
        )
        self.assertTrue(response)
        self.assertIsInstance(response, herepy.TrafficIncidentResponse)
        self.assertIsNotNone(response.as_dict())

    @responses.activate
    def test_incidents_in_corridor_fails(self):
        with codecs.open(
            "testdata/models/traffic_incidents_error.json", mode="r", encoding="utf-8"
        ) as f:
            expectedResponse = f.read()
        responses.add(
            responses.GET,
            "https://traffic.ls.hereapi.com/traffic/6.0/incidents.json",
            expectedResponse,
            status=200,
        )
        with self.assertRaises(herepy.UnauthorizedError):
            self._api.incidents_in_corridor(
                points=[[51.5072, -0.1275], [51.50781, -0.13112]], width=1000
            )

    @responses.activate
    def test_incidents_via_proximity_success(self):
        with codecs.open(
            "testdata/models/traffic_incidents_proximity.json",
            mode="r",
            encoding="utf-8",
        ) as f:
            expectedResponse = f.read()
        responses.add(
            responses.GET,
            "https://traffic.ls.hereapi.com/traffic/6.0/incidents.json",
            expectedResponse,
            status=200,
        )
        response = self._api.incidents_via_proximity(
            latitude=52.5311,
            longitude=13.3644,
            radius=15000,
            criticality=[
                herepy.IncidentsCriticalityInt.critical,
                herepy.IncidentsCriticalityInt.major,
            ],
        )
        self.assertTrue(response)
        self.assertIsInstance(response, herepy.TrafficIncidentResponse)
        self.assertIsNotNone(response.as_dict())

    @responses.activate
    def test_incidents_via_proximity_fails(self):
        with codecs.open(
            "testdata/models/traffic_incidents_error.json", mode="r", encoding="utf-8"
        ) as f:
            expectedResponse = f.read()
        responses.add(
            responses.GET,
            "https://traffic.ls.hereapi.com/traffic/6.0/incidents.json",
            expectedResponse,
            status=200,
        )
        with self.assertRaises(herepy.UnauthorizedError):
            self._api.incidents_via_proximity(
                latitude=52.5311,
                longitude=13.3644,
                radius=15000,
                criticality=[
                    herepy.IncidentsCriticalityInt.critical,
                    herepy.IncidentsCriticalityInt.major,
                ],
            )
