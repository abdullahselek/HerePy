#!/usr/bin/env python

import os
import sys
import io
import unittest
import codecs
import json

from unittest.mock import Mock, patch
from herepy import VectorTileApi


class VectorTileApiTest(unittest.TestCase):
    def setUp(self):
        api = VectorTileApi(api_key="api_key")
        self._api = api

    def test_initiation(self):
        self.assertIsInstance(self._api, VectorTileApi)
        self.assertEqual(self._api._api_key, "api_key")
        self.assertEqual(
            self._api._base_url, "https://vector.hereapi.com/v2/vectortiles/"
        )

    @patch("herepy.vector_tile_api.requests.get")
    def test_get_vector_tile_succeed(self, mock_get):
        with open("testdata/tiles/omv", "rb") as tile:
            mock_get.return_value = Mock(ok=True)
            mock_get.return_value.content = tile.read
        vector_tile = self._api.get_vectortile(latitude=52.525439, longitude=13.38727, zoom=12)
        self.assertIsNotNone(vector_tile)

    @patch("herepy.vector_tile_api.requests.get")
    def test_get_vector_tile_fails(self, mock_get):
        mock_get.return_value = Mock(ok=True)
        mock_get.return_value.content = None
        vector_tile = self._api.get_vectortile(latitude=52.525439, longitude=13.38727, zoom=12)
        self.assertIsNone(vector_tile)
