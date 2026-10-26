#!/usr/bin/env python

import unittest
from unittest.mock import AsyncMock, patch

import httpx2
import responses
from async_test_helpers import assert_async_get_cases

import herepy


class AsyncRmeApiTest(unittest.IsolatedAsyncioTestCase):
    async def test_async_match_route(self):
        with open("testdata/routes/sample.gpx", encoding="utf-8") as gpx_file:
            gpx_content = gpx_file.read()
        await assert_async_get_cases(
            self,
            herepy.RmeApi("api_key"),
            [("async_match_route", (gpx_content, "car", ["ADAS_ATTRIB_FCn(SLOPES)"]))],
            herepy.RmeResponse,
            fixture="rme_match_route_api.json",
        )

    async def test_async_match_route_maps_service_errors(self):
        api = herepy.RmeApi("api_key")
        async with api:
            client = api._get_async_client()
            with patch.object(client, "get", new=AsyncMock(return_value=httpx2.Response(200, json={"Details": "invalid route"}))):
                with self.assertRaisesRegex(herepy.HEREError, "invalid route"):
                    await api.async_match_route("")


class RmeApiTest(unittest.TestCase):
    def setUp(self):
        api = herepy.RmeApi("api_key")
        self._api = api

    def test_initiation(self):
        self.assertIsInstance(self._api, herepy.RmeApi)
        self.assertEqual(self._api._api_key, "api_key")
        self.assertEqual(self._api._base_url, "https://m.fleet.ls.hereapi.com/2/matchroute.json")

    @responses.activate
    def test_match_route_whensucceed(self):
        with open("testdata/models/rme_match_route_api.json") as f:
            expectedResponse = f.read()
        responses.add(
            responses.GET,
            "https://m.fleet.ls.hereapi.com/2/matchroute.json",
            expectedResponse,
            status=200,
        )
        with open("testdata/routes/sample.gpx", encoding="utf-8") as gpx_file:
            gpx_content = gpx_file.read()
        response = self._api.match_route(gpx_content, ["ADAS_ATTRIB_FCn(SLOPES)"])
        self.assertTrue(response)
        self.assertIsInstance(response, herepy.RmeResponse)

    @responses.activate
    def test_match_route_whenerroroccurred(self):
        with open("testdata/models/geocoder_error.json") as f:
            expectedResponse = f.read()
        responses.add(
            responses.GET,
            "https://m.fleet.ls.hereapi.com/2/matchroute.json",
            expectedResponse,
            status=200,
        )
        with self.assertRaises(herepy.HEREError):
            self._api.match_route("")
