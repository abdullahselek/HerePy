#!/usr/bin/env python

import os
import time
import unittest
import json
import responses
import codecs

from herepy import (
    IsolineRoutingApi,
    IsolineRoutingResponse,
    IsolineRoutingTransportMode,
    IsolineRoutingMode,
    UnauthorizedError,
)


class IsolineRoutingApiTest(unittest.TestCase):
    def setUp(self):
        api = IsolineRoutingApi("api_key")
        self._api = api

    def test_initiation(self):
        self.assertIsInstance(self._api, IsolineRoutingApi)
        self.assertEqual(self._api._api_key, "api_key")
        self.assertEqual(
            self._api._base_url, "https://isoline.router.hereapi.com/v8/isolines"
        )

    @responses.activate
    def test_distance_based_isoline_success(self):
        with codecs.open(
            "testdata/models/isoline_routing_distance_response.json",
            mode="r",
            encoding="utf-8",
        ) as f:
            expectedResponse = f.read()
        responses.add(
            responses.GET,
            "https://isoline.router.hereapi.com/v8/isolines",
            expectedResponse,
            status=200,
        )
        response = self._api.distance_based_isoline(
            transport_mode=IsolineRoutingTransportMode.car,
            origin=[52.51578, 13.37749],
            range=4000,
            routing_mode=IsolineRoutingMode.short,
        )
        self.assertTrue(response)
        self.assertIsInstance(response, IsolineRoutingResponse)
        self.assertIsNotNone(response.as_dict())

    @responses.activate
    def test_distance_based_isoline_fails(self):
        with codecs.open(
            "testdata/models/unauthorized_error.json", mode="r", encoding="utf-8"
        ) as f:
            expectedResponse = f.read()
        responses.add(
            responses.GET,
            "https://isoline.router.hereapi.com/v8/isolines",
            expectedResponse,
            status=200,
        )
        with self.assertRaises(UnauthorizedError):
            self._api.distance_based_isoline(
                transport_mode=IsolineRoutingTransportMode.car,
                origin=[52.51578, 13.37749],
                range=4000,
                routing_mode=IsolineRoutingMode.short,
            )

    @responses.activate
    def test_time_isoline_success(self):
        with codecs.open(
            "testdata/models/isoline_routing_distance_response.json",
            mode="r",
            encoding="utf-8",
        ) as f:
            expectedResponse = f.read()
        responses.add(
            responses.GET,
            "https://isoline.router.hereapi.com/v8/isolines",
            expectedResponse,
            status=200,
        )
        response = self._api.time_isoline(
            transport_mode=IsolineRoutingTransportMode.car,
            origin=[52.51578, 13.37749],
            range=300,
        )
        self.assertTrue(response)
        self.assertIsInstance(response, IsolineRoutingResponse)
        self.assertIsNotNone(response.as_dict())

    @responses.activate
    def test_time_isoline_fails(self):
        with codecs.open(
            "testdata/models/unauthorized_error.json", mode="r", encoding="utf-8"
        ) as f:
            expectedResponse = f.read()
        responses.add(
            responses.GET,
            "https://isoline.router.hereapi.com/v8/isolines",
            expectedResponse,
            status=200,
        )
        with self.assertRaises(UnauthorizedError):
            self._api.time_isoline(
                transport_mode=IsolineRoutingTransportMode.car,
                origin=[52.51578, 13.37749],
                range=300,
            )
