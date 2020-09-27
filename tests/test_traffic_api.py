#!/usr/bin/env python

import datetime
import os
import sys
import unittest
import responses
import codecs
import herepy

class TrafficApiTest(unittest.TestCase):

    def setUp(self):
        api = herepy.TrafficApi('api_key')
        self._api = api

    def test_initiation(self):
        self.assertIsInstance(self._api, herepy.TrafficApi)
        self.assertEqual(self._api._api_key, 'api_key')
