#!/usr/bin/env python

import os
import sys
import io
import unittest
import codecs

from unittest.mock import Mock, patch
from herepy import MapTileApi, MapTileApiType


class MapTileApiTest(unittest.TestCase):
    def setUp(self):
        api = MapTileApi(api_key="api_key")
        self._api = api

    def test_initiation(self):
        self.assertIsInstance(self._api, MapTileApi)
        self.assertEqual(self._api._api_key, "api_key")
        self.assertIsNone(self._api._base_url)

    @patch("herepy.map_tile_api.requests.get")
    def test_get_map_tile_with_default_parameters_succeed(self, mock_get):
        with open("testdata/tiles/berlin.png", "rb") as tile:
            mock_get.return_value = Mock(ok=True)
            mock_get.return_value.content = tile.read
        map_tile = self._api.get_maptile()
        self.assertIsNotNone(map_tile)

    @patch("herepy.map_tile_api.requests.get")
    def test_get_map_tile_with_default_parameters_fails(self, mock_get):
        mock_get.return_value = Mock(ok=True)
        mock_get.return_value.content = None
        map_tile = self._api.get_maptile()
        self.assertIsNone(map_tile)
