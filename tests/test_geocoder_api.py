#!/usr/bin/env python

import os
import time
import unittest
import json
import responses
import herepy

class GeocoderApiTest(unittest.TestCase):

    def setUp(self):
        api = herepy.GeocoderApi('app_id', 'app_code')
        self._api = api

    def test_initiation(self):
        self.assertIsInstance(self._api, herepy.GeocoderApi)
        self.assertEqual(self._api._app_id, 'app_id')
        self.assertEqual(self._api._app_code, 'app_code')
        self.assertEqual(self._api._base_url, 'https://geocoder.cit.api.here.com/6.2/geocode.json')

    @responses.activate
    def test_freeform_whensucceed(self):
        with open('testdata/models/geocoder.json', 'r') as f:
            expectedResponse = f.read()
        responses.add(responses.GET, 'https://geocoder.cit.api.here.com/6.2/geocode.json',
                  expectedResponse, status=200)
        response = self._api.free_form('200 S Mathilda Sunnyvale CA')
        self.assertTrue(response)
        self.assertIsInstance(response, herepy.GeocoderResponse)

    @responses.activate
    def test_freeform_whenerroroccured(self):
        with open('testdata/models/geocoder_error.json', 'r') as f:
            expectedResponse = f.read()
        responses.add(responses.GET, 'https://geocoder.cit.api.here.com/6.2/geocode.json',
                  expectedResponse, status=200)
        response = self._api.free_form('')
        self.assertIsInstance(response, herepy.HEREError)

    @responses.activate
    def test_address_withboundingbox_whensucceed(self):
        with open('testdata/models/geocoder.json', 'r') as f:
            expectedResponse = f.read()
        responses.add(responses.GET, 'https://geocoder.cit.api.here.com/6.2/geocode.json',
                  expectedResponse, status=200)
        response = self._api.address_with_boundingbox('200 S Mathilda Sunnyvale CA', [42.3952, -71.1056], [42.3312, -71.0228])
        self.assertTrue(response)
        self.assertIsInstance(response, herepy.GeocoderResponse)

    @responses.activate
    def test_address_withboundingbox_whenerroroccured(self):
        with open('testdata/models/geocoder_error.json', 'r') as f:
            expectedResponse = f.read()
        responses.add(responses.GET, 'https://geocoder.cit.api.here.com/6.2/geocode.json',
                  expectedResponse, status=200)
        response = self._api.address_with_boundingbox('', [-42.3952, -71.1056], [-42.3312, -71.0228])
        self.assertIsInstance(response, herepy.HEREError)

    @responses.activate
    def test_addresswithdetails_whensucceed(self):
        with open('testdata/models/geocoder.json', 'r') as f:
            expectedResponse = f.read()
        responses.add(responses.GET, 'https://geocoder.cit.api.here.com/6.2/geocode.json',
                  expectedResponse, status=200)
        response = self._api.address_with_details(34, 'Barbaros', 'Istanbul', 'Turkey')
        self.assertTrue(response)
        self.assertIsInstance(response, herepy.GeocoderResponse)

    @responses.activate
    def test_addresswithdetails_whenerroroccured(self):
        with open('testdata/models/geocoder_error.json', 'r') as f:
            expectedResponse = f.read()
        responses.add(responses.GET, 'https://geocoder.cit.api.here.com/6.2/geocode.json',
                  expectedResponse, status=200)
        response = self._api.address_with_details(-34, '', '', '')
        self.assertIsInstance(response, herepy.HEREError)

    @responses.activate
    def test_streetintersection_whensucceed(self):
        with open('testdata/models/geocoder.json', 'r') as f:
            expectedResponse = f.read()
        responses.add(responses.GET, 'https://geocoder.cit.api.here.com/6.2/geocode.json',
                  expectedResponse, status=200)
        response = self._api.street_intersection('Barbaros', 'Istanbul')
        self.assertTrue(response)
        self.assertIsInstance(response, herepy.GeocoderResponse)

    @responses.activate
    def test_streetintersection__whenerroroccured(self):
        with open('testdata/models/geocoder_error.json', 'r') as f:
            expectedResponse = f.read()
        responses.add(responses.GET, 'https://geocoder.cit.api.here.com/6.2/geocode.json',
                  expectedResponse, status=200)
        response = self._api.street_intersection('', '')
        self.assertIsInstance(response, herepy.HEREError)
