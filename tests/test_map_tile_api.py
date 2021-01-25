#!/usr/bin/env python

import os
import sys
import io
import unittest
import responses
import codecs

from herepy import MapTileApi, MapTileApiType


class MapTileApiTest(unittest.TestCase):
    def setUp(self):
        api = MapTileApi(api_key="api_key", api_type=MapTileApiType.base)
        self._api = api

    def test_initiation(self):
        self.assertIsInstance(self._api, MapTileApi)
        self.assertEqual(self._api._api_key, "api_key")
        self.assertIsNotNone(self._api._base_url)
