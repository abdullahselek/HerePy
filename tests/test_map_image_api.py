#!/usr/bin/env python

import codecs
import io
import json
import os
import sys
import unittest
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
    def test_get_mapimage_with_boundingbox(self, mock_get):
        with open("testdata/images/new-delhi-uncertainty.jpg", "rb") as f:
            mock_get.return_value = Mock(ok=True)
            byte_im = f.read()
            mock_get.return_value.content = byte_im
        map_image = self._api.get_mapimage(
            top_left=[52.8, 11.37309],
            bottom_right=[52.31, 13.2],
            zoom=16,
        )
        self.assertIsNotNone(map_image)
        self.assertTrue(isinstance(map_image, bytes))

    @patch("herepy.map_image_api.requests.get")
    def test_get_mapimage_with_coordinates(self, mock_get):
        with open("testdata/images/new-delhi-uncertainty.jpg", "rb") as f:
            mock_get.return_value = Mock(ok=True)
            byte_im = f.read()
            mock_get.return_value.content = byte_im
        map_image = self._api.get_mapimage(
            coordinates=[28.371425, 77.387695],
            uncertainty="5m",
        )
        self.assertIsNotNone(map_image)
        self.assertTrue(isinstance(map_image, bytes))

    @patch("herepy.map_image_api.requests.get")
    def test_get_mapimage_when_fails(self, mock_get):
        mock_get.return_value = Mock(ok=True)
        mock_get.return_value.content = None
        map_image = self._api.get_mapimage(
            coordinates=[28.371425, 77.387695],
            uncertainty="5m",
        )
        self.assertIsNone(map_image)

    @patch("herepy.map_image_api.requests.get")
    def test_get_mapimage_hybrid_daylight_succeed(self, mock_get):
        with open("testdata/images/new-delhi-uncertainty.jpg", "rb") as f:
            mock_get.return_value = Mock(ok=True)
            byte_im = f.read()
            mock_get.return_value.content = byte_im
        map_image = self._api.get_mapimage(
            coordinates=[28.371425, 77.387695], uncertainty="5m", map_scheme=3
        )
        self.assertIsNotNone(map_image)
        self.assertTrue(isinstance(map_image, bytes))

    @patch("herepy.map_image_api.requests.get")
    def test_get_mapimage_nodot_succeed(self, mock_get):
        with open("testdata/images/new-delhi-uncertainty.jpg", "rb") as f:
            mock_get.return_value = Mock(ok=True)
            byte_im = f.read()
            mock_get.return_value.content = byte_im
        map_image = self._api.get_mapimage(
            coordinates=[28.371425, 77.387695], uncertainty="5m", nodot=True
        )
        self.assertIsNotNone(map_image)
        self.assertTrue(isinstance(map_image, bytes))

    @patch("herepy.map_image_api.requests.get")
    def test_get_mapimage_city_name(self, mock_get):
        with open("testdata/images/new-delhi-uncertainty.jpg", "rb") as f:
            mock_get.return_value = Mock(ok=True)
            byte_im = f.read()
            mock_get.return_value.content = byte_im
        map_image = self._api.get_mapimage(
            coordinates=[60.17675, 24.929974],
            city_name="Helsinki",
            image_height=400,
            show_position=True,
            zoom=15,
        )
        self.assertIsNotNone(map_image)
        self.assertTrue(isinstance(map_image, bytes))

    @patch("herepy.map_image_api.requests.get")
    def test_get_mapimage_country_name(self, mock_get):
        with open("testdata/images/new-delhi-uncertainty.jpg", "rb") as f:
            mock_get.return_value = Mock(ok=True)
            byte_im = f.read()
            mock_get.return_value.content = byte_im
        map_image = self._api.get_mapimage(
            coordinates=[60.17675, 24.929974], country_name="Finland", zoom=15
        )
        self.assertIsNotNone(map_image)
        self.assertTrue(isinstance(map_image, bytes))

    @patch("herepy.map_image_api.requests.get")
    def test_get_mapimage_country_name_and_center(self, mock_get):
        with open("testdata/images/new-delhi-uncertainty.jpg", "rb") as f:
            mock_get.return_value = Mock(ok=True)
            byte_im = f.read()
            mock_get.return_value.content = byte_im
        map_image = self._api.get_mapimage(
            coordinates=[60.17675, 24.929974],
            country_name="Finland",
            center=[60.17, 24.90],
            zoom=15,
        )
        self.assertIsNotNone(map_image)
        self.assertTrue(isinstance(map_image, bytes))

    @patch("herepy.map_image_api.requests.get")
    def test_get_mapimage_encoded_geo_coordinate(self, mock_get):
        with open("testdata/images/new-delhi-uncertainty.jpg", "rb") as f:
            mock_get.return_value = Mock(ok=True)
            byte_im = f.read()
            mock_get.return_value.content = byte_im
        map_image = self._api.get_mapimage(
            encoded_geo_coordinate="QeL4rkKaxoA", zoom=10
        )
        self.assertIsNotNone(map_image)
        self.assertTrue(isinstance(map_image, bytes))

    @patch("herepy.map_image_api.requests.get")
    def test_get_mapimage_label_languages(self, mock_get):
        with open("testdata/images/new-delhi-uncertainty.jpg", "rb") as f:
            mock_get.return_value = Mock(ok=True)
            byte_im = f.read()
            mock_get.return_value.content = byte_im
        map_image = self._api.get_mapimage(
            coordinates=[28.371425, 77.387695],
            label_language="ger",
            second_label_language="tur",
        )
        self.assertIsNotNone(map_image)
        self.assertTrue(isinstance(map_image, bytes))
