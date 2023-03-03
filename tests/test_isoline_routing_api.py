#!/usr/bin/env python

import codecs
import json
import os
import time
import unittest

import responses

from herepy import (HEREError, IsolineRoutingApi, IsolineRoutingMode,
                    IsolineRoutingResponse, IsolineRoutingTransportMode,
                    UnauthorizedError)


class IsolineRoutingApiTest(unittest.TestCase):
    def setUp(self):
        api = IsolineRoutingApi(api_key="api_key")
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
            ranges=[3000, 4000],
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
                ranges=[3000, 4000],
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
            ranges=[300, 400],
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
                ranges=[300, 400],
            )

    @responses.activate
    def test_isoline_based_on_consumption_succeed(self):
        with codecs.open(
            "testdata/models/isoline_based_on_consumption.json",
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
        response = self._api.isoline_based_on_consumption(
            origin=[52.532988, 13.352852],
            ranges=[20000, 30000],
            transport_mode=IsolineRoutingTransportMode.car,
            free_flow_speed_table=[
                0.239,
                27,
                0.239,
                45,
                0.259,
                60,
                0.196,
                75,
                0.207,
                90,
                0.238,
                100,
                0.26,
                110,
                0.296,
                120,
                0.337,
                130,
                0.351,
                250,
                0.351,
            ],
            traffic_speed_table=[
                0.349,
                27,
                0.319,
                45,
                0.329,
                60,
                0.266,
                75,
                0.287,
                90,
                0.318,
                100,
                0.33,
                110,
                0.335,
                120,
                0.35,
                130,
                0.36,
                250,
                0.36,
            ],
            ascent=9,
            descent=4.3,
            auxiliary_consumption=1.8,
        )
        self.assertTrue(response)
        self.assertIsInstance(response, IsolineRoutingResponse)
        self.assertIsNotNone(response.as_dict())

    @responses.activate
    def test_isoline_based_on_consumption_fails(self):
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
            self._api.isoline_based_on_consumption(
                origin=[52.532988, 13.352852],
                ranges=[20000, 30000],
                transport_mode=IsolineRoutingTransportMode.car,
                free_flow_speed_table=[
                    0.239,
                    27,
                    0.239,
                    45,
                    0.259,
                    60,
                    0.196,
                    75,
                    0.207,
                    90,
                    0.238,
                    100,
                    0.26,
                    110,
                    0.296,
                    120,
                    0.337,
                    130,
                    0.351,
                    250,
                    0.351,
                ],
                traffic_speed_table=[
                    0.349,
                    27,
                    0.319,
                    45,
                    0.329,
                    60,
                    0.266,
                    75,
                    0.287,
                    90,
                    0.318,
                    100,
                    0.33,
                    110,
                    0.335,
                    120,
                    0.35,
                    130,
                    0.36,
                    250,
                    0.36,
                ],
                ascent=9,
                descent=4.3,
                auxiliary_consumption=1.8,
            )

    @responses.activate
    def test_isoline_routing_at_specific_time_with_origin_succeed(self):
        with codecs.open(
            "testdata/models/isoline_routing_api_specific_time_departure.json",
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
        response = self._api.isoline_routing_at_specific_time(
            transport_mode=IsolineRoutingTransportMode.car,
            ranges=[300, 400],
            origin=[52.51578, 13.37749],
            departure_time="2020-05-10T09:30:00",
        )
        self.assertTrue(response)
        self.assertIsInstance(response, IsolineRoutingResponse)
        self.assertIsNotNone(response.as_dict())

    @responses.activate
    def test_isoline_routing_at_specific_time_succeed_with_destination_succeed(self):
        with codecs.open(
            "testdata/models/isoline_routing_api_specific_time_arrival.json",
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
        response = self._api.isoline_routing_at_specific_time(
            transport_mode=IsolineRoutingTransportMode.car,
            ranges=[300, 400],
            destination=[52.51578, 13.37749],
            arrival_time="2020-05-10T09:30:00",
        )
        self.assertTrue(response)
        self.assertIsInstance(response, IsolineRoutingResponse)
        self.assertIsNotNone(response.as_dict())

    @responses.activate
    def test_isoline_routing_at_specific_time_fails(self):
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
            self._api.isoline_routing_at_specific_time(
                transport_mode=IsolineRoutingTransportMode.car,
                ranges=[300, 400],
                origin=[52.51578, 13.37749],
                departure_time="2020-05-10T09:30:00",
            )

    @responses.activate
    def test_isoline_routing_at_specific_time_fails_with_missing_parameters(self):
        with self.assertRaises(HEREError):
            self._api.isoline_routing_at_specific_time(
                transport_mode=IsolineRoutingTransportMode.car,
                ranges=[300, 400],
            )

    @responses.activate
    def test_multi_range_routing_with_origin_succeed(self):
        with codecs.open(
            "testdata/models/isoline_routing_api_multi_range_departure.json",
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
        response = self._api.multi_range_routing(
            transport_mode=IsolineRoutingTransportMode.car,
            ranges=[1000, 2000, 3000],
            origin=[52.51578, 13.37749],
        )
        self.assertTrue(response)
        self.assertIsInstance(response, IsolineRoutingResponse)
        self.assertIsNotNone(response.as_dict())

    @responses.activate
    def test_multi_range_routing_with_destination_succeed(self):
        with codecs.open(
            "testdata/models/isoline_routing_api_multi_range_arrival.json",
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
        response = self._api.multi_range_routing(
            transport_mode=IsolineRoutingTransportMode.car,
            ranges=[1000, 2000, 3000],
            destination=[52.51578, 13.37749],
        )
        self.assertTrue(response)
        self.assertIsInstance(response, IsolineRoutingResponse)
        self.assertIsNotNone(response.as_dict())

    @responses.activate
    def test_multi_range_routing_with_missing_parameters_fails(self):
        with self.assertRaises(HEREError):
            self._api.multi_range_routing(
                transport_mode=IsolineRoutingTransportMode.car,
                ranges=[1000, 2000, 3000],
            )

    @responses.activate
    def test_reverse_direction_isoline_with_origin_succeed(self):
        with codecs.open(
            "testdata/models/isoline_routing_api_multi_range_departure.json",
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
        response = self._api.reverse_direction_isoline(
            transport_mode=IsolineRoutingTransportMode.car,
            ranges=[1000, 2000],
            origin=[52.51578, 13.37749],
        )
        self.assertTrue(response)
        self.assertIsInstance(response, IsolineRoutingResponse)
        self.assertIsNotNone(response.as_dict())

    @responses.activate
    def test_reverse_direction_isoline_with_destination_succeed(self):
        with codecs.open(
            "testdata/models/isoline_routing_api_multi_range_arrival.json",
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
        response = self._api.reverse_direction_isoline(
            transport_mode=IsolineRoutingTransportMode.car,
            ranges=[1000, 2000],
            destination=[52.51578, 13.37749],
        )
        self.assertTrue(response)
        self.assertIsInstance(response, IsolineRoutingResponse)
        self.assertIsNotNone(response.as_dict())

    @responses.activate
    def test_reverse_direction_isoline_with_missing_parameters_fails(self):
        with self.assertRaises(HEREError):
            self._api.reverse_direction_isoline(
                transport_mode=IsolineRoutingTransportMode.car,
                ranges=[1000, 2000],
            )
