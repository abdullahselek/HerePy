#!/usr/bin/env python

import os
import sys
import io
import unittest
import responses
import codecs
import herepy


class MapTileApiTest(unittest.TestCase):
    def setUp(self):
        api = herepy.MapTileApi("api_key")
        self._api = api

    def test_initiation(self):
        self.assertIsInstance(self._api, herepy.MapTileApi)
        self.assertEqual(self._api._api_key, "api_key")
        self.assertEqual(
            self._api._base_url, "https://2.base.maps.ls.hereapi.com/maptile/2.1/"
        )
