#!/usr/bin/env python

import json
import os
import time
import unittest

import responses

import herepy


class GeocoderApiTest(unittest.TestCase):
    def setUp(self):
        api = herepy.GeocoderApi("api_key")
        self._api = api

    def test_initiation(self):
        self.assertIsInstance(self._api, herepy.GeocoderApi)
        self.assertEqual(self._api._api_key, "api_key")
        self.assertEqual(
            self._api._base_url, "https://geocode.search.hereapi.com/v1/geocode"
        )

    @responses.activate
    def test_freeform_whensucceed(self):
        with open("testdata/models/geocoder.json", "r") as f:
            expectedResponse = f.read()
        responses.add(
            responses.GET,
            "https://geocode.search.hereapi.com/v1/geocode",
            expectedResponse,
            status=200,
        )
        response = self._api.free_form("200 S Mathilda Sunnyvale CA")
        self.assertTrue(response)
        self.assertIsInstance(response, herepy.GeocoderResponse)

    @responses.activate
    def test_freeform_whenerroroccurred(self):
        with open("testdata/models/geocoder_error.json", "r") as f:
            expectedResponse = f.read()
        responses.add(
            responses.GET,
            "https://geocode.search.hereapi.com/v1/geocode",
            expectedResponse,
            status=200,
        )
        with self.assertRaises(herepy.HEREError):
            self._api.free_form("")

    @responses.activate
    def test_address_withboundingbox_whensucceed(self):
        with open("testdata/models/geocoder.json", "r") as f:
            expectedResponse = f.read()
        responses.add(
            responses.GET,
            "https://geocode.search.hereapi.com/v1/geocode",
            expectedResponse,
            status=200,
        )
        response = self._api.address_with_boundingbox(
            "200 S Mathilda Sunnyvale CA", [42.3952, -71.1056], [42.3312, -71.0228]
        )
        self.assertTrue(response)
        self.assertIsInstance(response, herepy.GeocoderResponse)

    @responses.activate
    def test_address_withboundingbox_whenerroroccurred(self):
        with open("testdata/models/geocoder_error.json", "r") as f:
            expectedResponse = f.read()
        responses.add(
            responses.GET,
            "https://geocode.search.hereapi.com/v1/geocode",
            expectedResponse,
            status=200,
        )
        with self.assertRaises(herepy.HEREError):
            self._api.address_with_boundingbox(
                "", [-42.3952, -71.1056], [-42.3312, -71.0228]
            )

    @responses.activate
    def test_addresswithdetails_whensucceed(self):
        with open("testdata/models/geocoder.json", "r") as f:
            expectedResponse = f.read()
        responses.add(
            responses.GET,
            "https://geocode.search.hereapi.com/v1/geocode",
            expectedResponse,
            status=200,
        )
        response = self._api.address_with_details(34, "Barbaros", "Istanbul", "Turkey")
        self.assertTrue(response)
        self.assertIsInstance(response, herepy.GeocoderResponse)

    @responses.activate
    def test_addresswithdetails_whenerroroccurred(self):
        with open("testdata/models/geocoder_error.json", "r") as f:
            expectedResponse = f.read()
        responses.add(
            responses.GET,
            "https://geocode.search.hereapi.com/v1/geocode",
            expectedResponse,
            status=200,
        )
        with self.assertRaises(herepy.HEREError):
            self._api.address_with_details(-34, "", "", "")

    @responses.activate
    def test_streetintersection_whensucceed(self):
        with open("testdata/models/geocoder.json", "r") as f:
            expectedResponse = f.read()
        responses.add(
            responses.GET,
            "https://geocode.search.hereapi.com/v1/geocode",
            expectedResponse,
            status=200,
        )
        response = self._api.street_intersection("Barbaros", "Istanbul")
        self.assertTrue(response)
        self.assertIsInstance(response, herepy.GeocoderResponse)

    @responses.activate
    def test_streetintersection_whenerroroccurred(self):
        with open("testdata/models/geocoder_error.json", "r") as f:
            expectedResponse = f.read()
        responses.add(
            responses.GET,
            "https://geocode.search.hereapi.com/v1/geocode",
            expectedResponse,
            status=200,
        )
        with self.assertRaises(herepy.HEREError):
            self._api.street_intersection("", "")
