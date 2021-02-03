#!/usr/bin/env python

import os
import sys
import io
import unittest
import codecs
import json

from unittest.mock import Mock, patch
from herepy import MapImageApi


class MapImageApiTest(unittest.TestCase):
    def setUp(self):
        api = MapImageApi(api_key="api_key")
        self._api = api

    def test_initiation(self):
        self.assertIsInstance(self._api, MapImageApi)
        self.assertEqual(self._api._api_key, "api_key")
        self.assertEqual(self._api._base_url, "https://image.maps.ls.hereapi.com/mia/1.6/mapview")
