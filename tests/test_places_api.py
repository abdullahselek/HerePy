#!/usr/bin/env python

import unittest

import responses
from async_test_helpers import assert_async_get_cases, assert_async_get_error_case

import herepy


class AsyncPlacesApiTest(unittest.IsolatedAsyncioTestCase):
    async def test_async_place_search_methods(self):
        api = herepy.PlacesApi("api_key")
        cases = [
            ("async_onebox_search", ([37.7905, -122.4107], "restaurant")),
            ("async_search_in_country", ([37.7905, -122.4107], "cafe", "USA")),
            ("async_places_in_circle", ([37.7905, -122.4107], 1000, "cafe")),
        ]
        await assert_async_get_cases(self, api, cases, herepy.PlacesResponse, fixture="places_api.json")

    async def test_async_search_maps_service_errors(self):
        await assert_async_get_error_case(
            self,
            herepy.PlacesApi("api_key"),
            "async_onebox_search",
            ([37.7905, -122.4107], ""),
            "places_api_error.json",
            herepy.HEREError,
        )


class PlacesApiTest(unittest.TestCase):
    def setUp(self):
        api = herepy.PlacesApi("api_key")
        self._api = api

    def test_initiation(self):
        self.assertIsInstance(self._api, herepy.PlacesApi)
        self.assertEqual(self._api._api_key, "api_key")
        self.assertEqual(self._api._base_url, "https://discover.search.hereapi.com/v1/discover")

    @responses.activate
    def test_onebox_search_whensucceed(self):
        with open("testdata/models/places_api.json") as f:
            expectedResponse = f.read()
        responses.add(
            responses.GET,
            "https://discover.search.hereapi.com/v1/discover",
            expectedResponse,
            status=200,
        )
        response = self._api.onebox_search([37.7905, -122.4107], "restaurant")
        self.assertTrue(response)
        self.assertIsInstance(response, herepy.PlacesResponse)

    @responses.activate
    def test_onebox_search_whenerroroccurred(self):
        with open("testdata/models/places_api_error.json") as f:
            expectedResponse = f.read()
        responses.add(
            responses.GET,
            "https://discover.search.hereapi.com/v1/discover",
            expectedResponse,
            status=200,
        )
        with self.assertRaises(herepy.HEREError):
            self._api.onebox_search([37.7905, -122.4107], "")

    @responses.activate
    def test_search_in_country_whensucceed(self):
        with open("testdata/models/places_api.json") as f:
            expectedResponse = f.read()
        responses.add(
            responses.GET,
            "https://discover.search.hereapi.com/v1/discover",
            expectedResponse,
            status=200,
        )
        response = self._api.search_in_country([37.7905, -122.4107], "cafe", "USA")
        self.assertTrue(response)
        self.assertIsInstance(response, herepy.PlacesResponse)

    @responses.activate
    def test_search_in_country_whenerroroccurred(self):
        with open("testdata/models/places_api_error.json") as f:
            expectedResponse = f.read()
        responses.add(
            responses.GET,
            "https://discover.search.hereapi.com/v1/discover",
            expectedResponse,
            status=200,
        )
        with self.assertRaises(herepy.HEREError):
            self._api.search_in_country([-9999.0, -9999.0], "", "")

    @responses.activate
    def test_places_in_circle_whensucceed(self):
        with open("testdata/models/places_api.json") as f:
            expectedResponse = f.read()
        responses.add(
            responses.GET,
            "https://discover.search.hereapi.com/v1/discover",
            expectedResponse,
            status=200,
        )
        response = self._api.places_in_circle([37.7905, -122.4107], 1000, "cafe")
        self.assertTrue(response)
        self.assertIsInstance(response, herepy.PlacesResponse)

    @responses.activate
    def test_places_in_circle_whenerroroccurred(self):
        with open("testdata/models/places_api_error.json") as f:
            expectedResponse = f.read()
        responses.add(
            responses.GET,
            "https://discover.search.hereapi.com/v1/discover",
            expectedResponse,
            status=200,
        )
        with self.assertRaises(herepy.HEREError):
            self._api.places_in_circle([-9999.0, -9999.0], 1000, "")
