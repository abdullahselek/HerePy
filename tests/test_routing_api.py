#!/usr/bin/env python

import os
import time
import unittest
import json
import responses
import herepy

class RoutingApiTest(unittest.TestCase):

    def setUp(self):
        api = herepy.RoutingApi('app_id', 'app_code')
        self._api = api

    def testInitiation(self):
        self.assertIsInstance(self._api, herepy.RoutingApi)
        self.assertEqual(self._api._app_id, 'app_id')
        self.assertEqual(self._api._app_code, 'app_code')
        self.assertEqual(self._api._baseUrl, 'https://route.cit.api.here.com/routing/7.2/calculateroute.json')
