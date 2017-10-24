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
    

