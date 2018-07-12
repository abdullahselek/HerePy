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

    def test_initiation(self):
        self.assertIsInstance(self._api, herepy.GeocoderAutoCompleteApi)
        self.assertEqual(self._api._app_id, 'app_id')
        self.assertEqual(self._api._app_code, 'app_code')
        self.assertEqual(self._api._base_url, 'https://autocomplete.geocoder.cit.api.here.com/6.2/suggest.json')

    @responses.activate
    def test_addresssuggestion_whensucceed(self):
        with open('testdata/models/geocoder_autocomplete.json', 'r') as f:
            expectedResponse = f.read()
        responses.add(responses.GET, 'https://autocomplete.geocoder.cit.api.here.com/6.2/suggest.json',
                  expectedResponse, status=200)
        response = self._api.address_suggestion('High', [51.5035, -0.1616], 100)
        self.assertTrue(response)
        self.assertIsInstance(response, herepy.GeocoderAutoCompleteResponse)

    @responses.activate
    def test_addresssuggestion_whenerroroccured(self):
        with open('testdata/models/geocoder_autocomplete_error.json', 'r') as f:
            expectedResponse = f.read()
        responses.add(responses.GET, 'https://autocomplete.geocoder.cit.api.here.com/6.2/suggest.json',
                  expectedResponse, status=200)
        response = self._api.address_suggestion('', [51.5035, -0.1616], 100)
        self.assertIsInstance(response, herepy.HEREError)

    @responses.activate
    def test_limitresultsbyaddress_whensucceed(self):
        with open('testdata/models/geocoder_autocomplete.json', 'r') as f:
            expectedResponse = f.read()
        responses.add(responses.GET, 'https://autocomplete.geocoder.cit.api.here.com/6.2/suggest.json',
                  expectedResponse, status=200)
        response = self._api.limit_results_byaddress('Nis', 'USA')
        self.assertTrue(response)
        self.assertIsInstance(response, herepy.GeocoderAutoCompleteResponse)

    @responses.activate
    def test_limitresultsbyaddress_whenerroroccured(self):
        with open('testdata/models/geocoder_autocomplete_error.json', 'r') as f:
            expectedResponse = f.read()
        responses.add(responses.GET, 'https://autocomplete.geocoder.cit.api.here.com/6.2/suggest.json',
                  expectedResponse, status=200)
        response = self._api.limit_results_byaddress('', '')
        self.assertIsInstance(response, herepy.HEREError)

    @responses.activate
    def test_highlightingmatches_whensucceed(self):
        with open('testdata/models/geocoder_autocomplete.json', 'r') as f:
            expectedResponse = f.read()
        responses.add(responses.GET, 'https://autocomplete.geocoder.cit.api.here.com/6.2/suggest.json',
                  expectedResponse, status=200)
        response = self._api.highlighting_matches('Wacker Chic', '**', '**')
        self.assertTrue(response)
        self.assertIsInstance(response, herepy.GeocoderAutoCompleteResponse)

    @responses.activate
    def test_highlightingmatches_whenerroroccured(self):
        with open('testdata/models/geocoder_autocomplete_error.json', 'r') as f:
            expectedResponse = f.read()
        responses.add(responses.GET, 'https://autocomplete.geocoder.cit.api.here.com/6.2/suggest.json',
                  expectedResponse, status=200)
        response = self._api.highlighting_matches('', '**', '**')
        self.assertIsInstance(response, herepy.HEREError)
