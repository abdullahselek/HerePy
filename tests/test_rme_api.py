#!/usr/bin/env python

import os
import time
import unittest
import json
import responses
import herepy
import io

class RmeApiTest(unittest.TestCase):

    def setUp(self):
        api = herepy.RmeApi('app_id', 'app_code')
        self._api = api

    def test_initiation(self):
        self.assertIsInstance(self._api, herepy.RmeApi)
        self.assertEqual(self._api._app_id, 'app_id')
        self.assertEqual(self._api._app_code, 'app_code')
        self.assertEqual(self._api._base_url, 'https://rme.api.here.com/2/matchroute.json')

    @responses.activate
    def test_match_route_whensucceed(self):
        with io.open('testdata/models/rme_match_route_api.json', 'r') as f:
            expectedResponse = f.read()
        responses.add(responses.GET, 'https://rme.api.here.com/2/matchroute.json',
                  expectedResponse, status=200)
        with io.open('testdata/routes/sample.gpx', encoding='utf-8') as gpx_file:
            gpx_content = gpx_file.read()
        response = self._api.match_route(gpx_content, ['ADAS_ATTRIB_FCn(SLOPES)'])
        self.assertTrue(response)
        self.assertIsInstance(response, herepy.RmeResponse)

    @responses.activate
    def test_match_route_whenerroroccured(self):
        with open('testdata/models/geocoder_error.json', 'r') as f:
            expectedResponse = f.read()
        responses.add(responses.GET, 'https://rme.api.here.com/2/matchroute.json',
                  expectedResponse, status=200)
        with self.assertRaises(herepy.HEREError):
            self._api.match_route('')

