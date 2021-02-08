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
        self.assertEqual(
            self._api._base_url, "https://image.maps.ls.hereapi.com/mia/1.6/mapview"
        )

    @patch("herepy.map_image_api.requests.get")
    def test_get_mapimage_when_succeed(self, mock_get):
        with open("testdata/images/new-delhi-uncertainty.jpg", "rb") as f:
            mock_get.return_value = Mock(ok=True)
            byte_im = f.read()
            mock_get.return_value.content = byte_im
        vector_tile = self._api.get_mapimage(
            coordinates=[28.371425, 77.387695],
            uncertainty="5m",
        )
        self.assertIsNotNone(vector_tile)
        self.assertTrue(isinstance(vector_tile, bytes))

    @patch("herepy.map_image_api.requests.get")
    def test_get_mapimage_when_fails(self, mock_get):
        mock_get.return_value = Mock(ok=True)
        mock_get.return_value.content = None
        vector_tile = self._api.get_mapimage(
            coordinates=[28.371425, 77.387695],
            uncertainty="5m",
        )
        self.assertIsNone(vector_tile)
