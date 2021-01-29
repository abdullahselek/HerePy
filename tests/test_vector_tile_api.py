#!/usr/bin/env python

import os
import sys
import io
import unittest
import codecs
import json

from herepy import VectorTileApi


class VectorTileApiTest(unittest.TestCase):
    def setUp(self):
        api = VectorTileApi(api_key="api_key")
        self._api = api

    def test_initiation(self):
        self.assertIsInstance(self._api, VectorTileApi)
        self.assertEqual(self._api._api_key, "api_key")
        self.assertEqual(self._api._base_url, "https://vector.hereapi.com/v2/vectortiles/")
