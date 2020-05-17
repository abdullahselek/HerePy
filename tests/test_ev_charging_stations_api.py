#!/usr/bin/env python

import os
import time
import unittest
import json
import responses
import herepy

class EVChargingStationsApi(unittest.TestCase):

    def setUp(self):
        api = herepy.EVChargingStationsApi(app_id='app_id', app_code='app_code')
        self._api = api


    def test_initiation(self):
        self.assertIsInstance(self._api, herepy.EVChargingStationsApi)
        self.assertEqual(self._api._app_id, 'app_id')
        self.assertEqual(self._api._app_code, 'app_code')
        self.assertEqual(self._api._base_url, 'https://ev-v2.cit.cc.api.here.com/ev/')
