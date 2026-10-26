#!/usr/bin/env python

import unittest

import responses
from async_test_helpers import assert_async_get_cases, assert_async_get_error_case

import herepy


class AsyncGeocoderReverseApiTest(unittest.IsolatedAsyncioTestCase):
    async def test_async_retrieve_addresses(self):
        await assert_async_get_cases(
            self,
            herepy.GeocoderReverseApi("api_key"),
            [("async_retrieve_addresses", ([41.8842, -87.6388], 3))],
            herepy.GeocoderReverseResponse,
            fixture="geocoder_reverse.json",
        )

    async def test_async_retrieve_addresses_maps_service_errors(self):
        await assert_async_get_error_case(
            self,
            herepy.GeocoderReverseApi("api_key"),
            "async_retrieve_addresses",
            ([None, None], 0),
            "geocoder_error.json",
            herepy.HEREError,
        )


class GeocoderReverseApiTest(unittest.TestCase):
    def setUp(self):
        api = herepy.GeocoderReverseApi("api_key")
        self._api = api

    def test_initiation(self):
        self.assertIsInstance(self._api, herepy.GeocoderReverseApi)
        self.assertEqual(self._api._api_key, "api_key")
        self.assertEqual(self._api._base_url, "https://revgeocode.search.hereapi.com/v1/revgeocode")

    @responses.activate
    def test_retrieve_addresses_whensucceed(self):
        with open("testdata/models/geocoder_reverse.json") as f:
            expectedResponse = f.read()
        responses.add(
            responses.GET,
            "https://revgeocode.search.hereapi.com/v1/revgeocode",
            expectedResponse,
            status=200,
        )
        response = self._api.retrieve_addresses([41.8842, -87.6388], 3)
        self.assertTrue(response)
        self.assertIsInstance(response, herepy.GeocoderReverseResponse)

    @responses.activate
    def test_retrieve_addresses_whenerroroccurred(self):
        with open("testdata/models/geocoder_error.json") as f:
            expectedResponse = f.read()
        responses.add(
            responses.GET,
            "https://revgeocode.search.hereapi.com/v1/revgeocode",
            expectedResponse,
            status=200,
        )
        with self.assertRaises(herepy.HEREError):
            self._api.retrieve_addresses([None, None], 0)
