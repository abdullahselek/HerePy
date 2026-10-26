#!/usr/bin/env python

import json
import unittest
from unittest.mock import AsyncMock, Mock, patch

import httpx2

from herepy import HEREError, InvalidRequestError, MapImageApi, UnauthorizedError


class AsyncMapImageApiTest(unittest.IsolatedAsyncioTestCase):
    async def test_async_get_mapimage_returns_binary_content(self):
        image = b"\xff\x00image-data"
        api = MapImageApi("api_key")
        async with api:
            client = api._get_async_client()
            with patch.object(client, "get", new=AsyncMock(return_value=httpx2.Response(200, content=image))) as get:
                result = await api.async_get_mapimage(coordinates=[28.371425, 77.387695], uncertainty="5m")

        self.assertEqual(result, image)
        get.assert_awaited_once()

    async def test_async_get_mapimage_builds_optional_parameters(self):
        image = b"\xff\x00image-data"
        api = MapImageApi("api_key")
        async with api:
            client = api._get_async_client()
            with patch.object(client, "get", new=AsyncMock(return_value=httpx2.Response(200, content=image))) as get:
                result = await api.async_get_mapimage(
                    top_left=[52.8, 11.37309],
                    bottom_right=[52.31, 13.2],
                    coordinates=[28.371425, 77.387695],
                    city_name="Helsinki",
                    country_name="Finland",
                    center=[60.17, 24.90],
                    encoded_geo_coordinate="QeL4rkKaxoA",
                    encoded_geo_center_coordinate="QeL4rkKaxoB",
                    image_height=400,
                    show_position=True,
                    map_scheme=3,
                    uncertainty="5m",
                    nodot=True,
                    house_number="42",
                    second_label_language="deu",
                )

        self.assertEqual(result, image)
        get.assert_awaited_once()

    async def test_async_get_mapimage_raises_service_errors(self):
        api = MapImageApi("api_key")
        error_payload = json.dumps(
            {
                "error": "BadRequest",
                "error_description": "invalid map request",
                "Type": "Invalid Request",
                "Message": "invalid map request",
            }
        )
        async with api:
            client = api._get_async_client()
            with patch.object(client, "get", new=AsyncMock(return_value=httpx2.Response(200, content=error_payload))):
                with self.assertRaises(InvalidRequestError):
                    await api.async_get_mapimage(coordinates=[28.371425, 77.387695])


class MapImageApiTest(unittest.TestCase):
    def setUp(self):
        api = MapImageApi(api_key="api_key")
        self._api = api

    def test_initiation(self):
        self.assertIsInstance(self._api, MapImageApi)
        self.assertEqual(self._api._api_key, "api_key")
        self.assertEqual(self._api._base_url, "https://image.maps.ls.hereapi.com/mia/1.6/mapview")

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
        map_image = self._api.get_mapimage(coordinates=[28.371425, 77.387695], uncertainty="5m", map_scheme=3)
        self.assertIsNotNone(map_image)
        self.assertTrue(isinstance(map_image, bytes))

    @patch("herepy.map_image_api.requests.get")
    def test_get_mapimage_nodot_succeed(self, mock_get):
        with open("testdata/images/new-delhi-uncertainty.jpg", "rb") as f:
            mock_get.return_value = Mock(ok=True)
            byte_im = f.read()
            mock_get.return_value.content = byte_im
        map_image = self._api.get_mapimage(coordinates=[28.371425, 77.387695], uncertainty="5m", nodot=True)
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
        map_image = self._api.get_mapimage(coordinates=[60.17675, 24.929974], country_name="Finland", zoom=15)
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
        map_image = self._api.get_mapimage(encoded_geo_coordinate="QeL4rkKaxoA", zoom=10)
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

    @patch("herepy.map_image_api.requests.get")
    def test_get_mapimage_encoded_center_and_house_number(self, mock_get):
        mock_get.return_value.content = b"{}"

        image = self._api.get_mapimage(
            encoded_geo_center_coordinate="center-code",
            house_number="42",
        )

        self.assertEqual(image, b"{}")
        request_url = mock_get.call_args.args[0]
        self.assertIn("ectr=center-code", request_url)
        self.assertIn("n=42", request_url)

    @patch("herepy.map_image_api.requests.get")
    def test_get_mapimage_maps_service_errors(self, mock_get):
        cases = [
            ({"error": "Unauthorized", "error_description": "invalid key"}, UnauthorizedError),
            (
                {"error": "BadRequest", "error_description": "bad input", "Type": "Invalid Request", "Message": "bad input"},
                InvalidRequestError,
            ),
            ({"error": "Unavailable", "error_description": "service unavailable"}, HEREError),
        ]
        for payload, expected_error in cases:
            with self.subTest(payload=payload):
                mock_get.return_value.content = json.dumps(payload).encode()
                with self.assertRaises(expected_error):
                    self._api.get_mapimage(coordinates=[52.5, 13.4])
