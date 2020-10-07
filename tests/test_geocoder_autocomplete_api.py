#!/usr/bin/env python

import os
import time
import unittest
import json
import responses
import herepy


class GeocoderAutoCompleteApiTest(unittest.TestCase):
    def setUp(self):
        api = herepy.GeocoderAutoCompleteApi("api_key")
        self._api = api

    def test_initiation(self):
        self.assertIsInstance(self._api, herepy.GeocoderAutoCompleteApi)
        self.assertEqual(self._api._api_key, "api_key")
        self.assertEqual(
            self._api._base_url, "https://autosuggest.search.hereapi.com/v1/autosuggest"
        )

    @responses.activate
    def test_addresssuggestion_whensucceed(self):
        with open("testdata/models/geocoder_autocomplete.json", "r") as f:
            expectedResponse = f.read()
        responses.add(
            responses.GET,
            "https://autosuggest.search.hereapi.com/v1/autosuggest",
            expectedResponse,
            status=200,
        )
        response = self._api.address_suggestion("High", [51.5035, -0.1616], 100)
        self.assertTrue(response)
        self.assertIsInstance(response, herepy.GeocoderAutoCompleteResponse)

    @responses.activate
    def test_addresssuggestion_whenerroroccured(self):
        with open("testdata/models/geocoder_autocomplete_error.json", "r") as f:
            expectedResponse = f.read()
        responses.add(
            responses.GET,
            "https://autosuggest.search.hereapi.com/v1/autosuggest",
            expectedResponse,
            status=200,
        )
        with self.assertRaises(herepy.HEREError):
            self._api.address_suggestion("", [51.5035, -0.1616], 100)

    @responses.activate
    def test_limitresultsbyaddress_whensucceed(self):
        with open("testdata/models/geocoder_autocomplete.json", "r") as f:
            expectedResponse = f.read()
        responses.add(
            responses.GET,
            "https://autosuggest.search.hereapi.com/v1/autosuggest",
            expectedResponse,
            status=200,
        )
        response = self._api.limit_results_byaddress("Nis", "USA")
        self.assertTrue(response)
        self.assertIsInstance(response, herepy.GeocoderAutoCompleteResponse)

    @responses.activate
    def test_limitresultsbyaddress_whenerroroccured(self):
        with open("testdata/models/geocoder_autocomplete_error.json", "r") as f:
            expectedResponse = f.read()
        responses.add(
            responses.GET,
            "https://autosuggest.search.hereapi.com/v1/autosuggest",
            expectedResponse,
            status=200,
        )
        with self.assertRaises(herepy.HEREError):
            self._api.limit_results_byaddress("", "")
