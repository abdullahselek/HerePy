#!/usr/bin/env python

import os
import sys
import unittest
import responses
import codecs
import herepy

class PlacesApiTest(unittest.TestCase):

    def setUp(self):
        api = herepy.PlacesApi('app_id', 'app_code')
        self._api = api

    def test_initiation(self):
        self.assertIsInstance(self._api, herepy.PlacesApi)
        self.assertEqual(self._api._app_id, 'app_id')
        self.assertEqual(self._api._app_code, 'app_code')
        self.assertEqual(self._api._base_url, 'https://places.cit.api.here.com/places/v1/discover/search')
