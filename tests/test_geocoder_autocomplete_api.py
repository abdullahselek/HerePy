#!/usr/bin/env python

import os
import time
import unittest
import json
import responses
import herepy

class GeocoderAutoCompleteApiTest(unittest.TestCase):

    def setUp(self):
        api = herepy.GeocoderAutoCompleteApi('app_id', 'app_code')
        self._api = api

    def testInitiation(self):
        self.assertIsInstance(self._api, herepy.GeocoderAutoCompleteApi)
        self.assertEqual(self._api._app_id, 'app_id')
        self.assertEqual(self._api._app_code, 'app_code')
        self.assertEqual(self._api._baseUrl, 'https://autocomplete.geocoder.cit.api.here.com/6.2/suggest.json')

    @responses.activate
    def testAddressSuggestion_whenSucceed(self):
        with open('testdata/models/geocoder_autocomplete.json', 'r') as f:
            expectedResponse = f.read()
        responses.add(responses.GET, 'https://autocomplete.geocoder.cit.api.here.com/6.2/suggest.json',
                  expectedResponse, status=200)
        response = self._api.AddressSuggestion([51.5035,-0.1616], 100)
        self.assertTrue(response)
        self.assertIsInstance(response, herepy.GeocoderAutoCompleteResponse)

    @responses.activate
    def testAddressSuggestion_whenErrorOccured(self):
        with open('testdata/models/geocoder_autocomplete_error.json', 'r') as f:
            expectedResponse = f.read()
        responses.add(responses.GET, 'https://autocomplete.geocoder.cit.api.here.com/6.2/suggest.json',
                  expectedResponse, status=200)
        response = self._api.AddressSuggestion([51.5035,-0.1616], 100)
        self.assertIsInstance(response, herepy.HEREError)
