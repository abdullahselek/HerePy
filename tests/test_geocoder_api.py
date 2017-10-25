#!/usr/bin/env python

import os
import time
import unittest
import requests_mock
import json
import herepy

class GeocoderApiTest(unittest.TestCase):

    def setUp(self):
        api = herepy.GeocoderApi('app_id', 'app_code')
        self._api = api

    def testInitiation(self):
        self.assertIsInstance(self._api, herepy.GeocoderApi)
        self.assertEqual(self._api._app_id, 'app_id')
        self.assertEqual(self._api._app_code, 'app_code')
        self.assertEqual(self._api._baseUrl, 'https://geocoder.cit.api.here.com/6.2/geocode.json')

    def testEncodeParameters(self):
        data = None
        encodedParameters = self._api.EncodeParameters(data)
        self.assertEqual(encodedParameters, None)
        data = {'searchtext': '200 S Mathilda Sunnyvale CA'}
        encodedParameters = self._api.EncodeParameters(data)
        self.assertTrue(encodedParameters)
        data = {'searchtext': '200 S Mathilda Sunnyvale CA', 'gen': '8'}
        encodedParameters = self._api.EncodeParameters(data)
        self.assertTrue(encodedParameters)

    def testBuildUrl(self):
        data = {'searchtext': '200 S Mathilda Sunnyvale CA', 'app_id': 'app_id', 'app_code': 'app_code'}
        url = self._api.BuildUrl(self._api._baseUrl, data)
        self.assertTrue(url)

    @requests_mock.mock()
    def testFreeForm(self, m):
        with open('testdata/models/geocoder.json', 'rb') as f:
            sampleResponse = f.read()
        url = 'https://geocoder.cit.api.here.com/6.2/geocode.json?searchtext=200+S+Mathilda+Sunnyvale+CA&app_code=app_code&app_id=app_id'
        with requests_mock.Mocker() as m:
            m.get(url, text=sampleResponse)
            response = self._api.FreeForm('200 S Mathilda Sunnyvale CA')
            self.assertTrue(response)
            self.assertIsInstance(response, herepy.GeocoderResponse)
