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
