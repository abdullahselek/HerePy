#!/usr/bin/env python

import os
import time
import urllib
import unittest
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
    

