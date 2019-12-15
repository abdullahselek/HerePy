#!/usr/bin/env python

import os
import time
import unittest
import json
import responses
import herepy

class GeocoderReverseApiTest(unittest.TestCase):

    def setUp(self):
        api = herepy.GeocoderReverseApi('api_key')
        self._api = api

    def test_initiation(self):
        self.assertIsInstance(self._api, herepy.GeocoderReverseApi)
        self.assertEqual(self._api._api_key, 'api_key')
        self.assertEqual(self._api._base_url, 'https://reverse.geocoder.ls.hereapi.com/6.2/reversegeocode.json')

    @responses.activate
    def test_retrieve_addresses_whensucceed(self):
        with open('testdata/models/geocoder_reverse.json', 'r') as f:
            expectedResponse = f.read()
        responses.add(responses.GET, 'https://reverse.geocoder.ls.hereapi.com/6.2/reversegeocode.json',
                  expectedResponse, status=200)
        response = self._api.retrieve_addresses([41.8842,-87.6388], 250)
        self.assertTrue(response)
        self.assertIsInstance(response, herepy.GeocoderReverseResponse)

    @responses.activate
    def test_retrieve_addresses_whenerroroccured(self):
        with open('testdata/models/geocoder_error.json', 'r') as f:
            expectedResponse = f.read()
        responses.add(responses.GET, 'https://reverse.geocoder.ls.hereapi.com/6.2/reversegeocode.json',
                  expectedResponse, status=200)
        with self.assertRaises(herepy.HEREError):
            self._api.retrieve_addresses([None,None],0)

