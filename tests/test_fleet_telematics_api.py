#!/usr/bin/env python

import os
import time
import unittest
import json
import responses
import herepy

class FleetTelematicsApiTest(unittest.TestCase):

    def setUp(self):
        api = herepy.FleetTelematicsApi('api_key')
        self._api = api


    def test_initiation(self):
        self.assertIsInstance(self._api, herepy.FleetTelematicsApi)
        self.assertEqual(self._api._api_key, 'api_key')
        self.assertEqual(self._api._base_url, 'https://wse.ls.hereapi.com/2/')

