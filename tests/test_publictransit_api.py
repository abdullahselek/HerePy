#!/usr/bin/env python

import os
import sys
import io
import unittest
import responses
import codecs
import herepy

class PublicTransitApiTest(unittest.TestCase):

    def setUp(self):
        api = herepy.PublicTransitApi('app_id', 'app_code')
        self._api = api

    def test_initiation(self):
        self.assertIsInstance(self._api, herepy.PublicTransitApi)
        self.assertEqual(self._api._app_id, 'app_id')
        self.assertEqual(self._api._app_code, 'app_code')
        self.assertEqual(self._api._base_url, 'https://cit.transit.api.here.com/v3/stations/')

    @responses.activate
    def test_find_stations_by_name_whensucceed(self):
        with open('testdata/models/public_transit_api.json', 'r') as f:
            expectedResponse = f.read()
        responses.add(responses.GET, 'https://cit.transit.api.here.com/v3/stations/by_name.json',
                  expectedResponse, status=200)
        response = self._api.find_stations_by_name([40.7505, -73.9910],
                                                   'union',
                                                   10,
                                                   herepy.PublicTransitSearchMethod.fuzzy,
                                                   5000)
        self.assertTrue(response)
        self.assertIsInstance(response, herepy.PublicTransitResponse)

    @responses.activate
    def test_find_stations_by_name_whenerroroccured(self):
        with open('testdata/models/public_transit_api_error.json', 'r') as f:
            expectedResponse = f.read()
        responses.add(responses.GET, 'https://cit.transit.api.here.com/v3/stations/by_name.json',
                  expectedResponse, status=200)
        response = self._api.find_stations_by_name([40.7505, -73.9910],
                                                   '')
        self.assertIsInstance(response, herepy.HEREError)

    @responses.activate
    def test_find_stations_nearby_whensucceed(self):
        with io.open('testdata/models/public_transit_api_nearby.json', 'r', encoding='utf-8') as f:
            expectedResponse = f.read()
        responses.add(responses.GET, 'https://cit.transit.api.here.com/v3/stations/by_geocoord.json',
                  expectedResponse, status=200)
        response = self._api.find_stations_nearby([55.7541, 37.6200], 350, 3)
        self.assertTrue(response)
        self.assertIsInstance(response, herepy.PublicTransitResponse)

    @responses.activate
    def test_find_stations_nearby_whenerroroccured(self):
        with open('testdata/models/public_transit_api_error.json', 'r') as f:
            expectedResponse = f.read()
        responses.add(responses.GET, 'https://cit.transit.api.here.com/v3/stations/by_geocoord.json',
                  expectedResponse, status=200)
        response = self._api.find_stations_nearby([-9999, -9999])
        self.assertIsInstance(response, herepy.HEREError)
