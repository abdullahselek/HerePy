#!/usr/bin/env python

import unittest
from unittest.mock import AsyncMock, Mock, patch

import httpx2

from herepy import HEREError, UnauthorizedError, VectorMapTileLayer, VectorTileApi


class AsyncVectorTileApiTest(unittest.IsolatedAsyncioTestCase):
    async def test_async_get_vectortile_returns_binary_content(self):
        tile_bytes = b"\xff\x00vector-tile"
        api = VectorTileApi("api_key")
        async with api:
            client = api._get_async_client()
            with patch.object(client, "get", new=AsyncMock(return_value=httpx2.Response(200, content=tile_bytes))) as get:
                result = await api.async_get_vectortile(52.525439, 13.38727, 12)

        self.assertEqual(result, tile_bytes)
        get.assert_awaited_once()

    async def test_async_get_vectortile_raises_unauthorized_error(self):
        with open("testdata/models/unauthorized_error.json", "rb") as file:
            error_content = file.read()
        api = VectorTileApi("api_key")
        async with api:
            client = api._get_async_client()
            with patch.object(client, "get", new=AsyncMock(return_value=httpx2.Response(200, content=error_content))):
                with self.assertRaises(UnauthorizedError):
                    await api.async_get_vectortile(52.525439, 13.38727, 12)

    async def test_async_get_vectortile_preserves_non_error_json_and_request_options(self):
        payload = b'{"status": "ok"}'
        api = VectorTileApi("api_key")
        async with api:
            client = api._get_async_client()
            with patch.object(client, "get", new=AsyncMock(return_value=httpx2.Response(200, content=payload))) as get:
                result = await api.async_get_vectortile(
                    52.525439,
                    13.38727,
                    12,
                    layer=VectorMapTileLayer.core,
                    query_parameters={"mode": "test"},
                    headers={"X-Test": "value"},
                )

        self.assertEqual(result, payload)
        get.assert_awaited_once()
        self.assertIn("mode=test", get.await_args.args[0])
        self.assertEqual(get.await_args.kwargs["headers"], {"X-Test": "value"})


class VectorTileApiTest(unittest.TestCase):
    def setUp(self):
        api = VectorTileApi(api_key="api_key")
        self._api = api

    def test_initiation(self):
        self.assertIsInstance(self._api, VectorTileApi)
        self.assertEqual(self._api._api_key, "api_key")
        self.assertEqual(self._api._base_url, "https://vector.hereapi.com/v2/vectortiles/")

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

    @patch("herepy.vector_tile_api.requests.get")
    def test_get_vector_tile_when_receives_unauthorized_error(self, mock_get):
        with open("testdata/models/unauthorized_error.json", "rb") as f:
            mock_get.return_value = Mock(ok=True)
            mock_get.return_value.content = f.read()
        with self.assertRaises(UnauthorizedError) as cm:
            vector_tile = self._api.get_vectortile(latitude=52.525439, longitude=13.38727, zoom=12)
        self.assertEqual("apiKey invalid. apiKey not found.", str(cm.exception))

    @patch("herepy.vector_tile_api.requests.get")
    def test_get_vector_tile_when_receives_not_authorize_access_error(self, mock_get):
        with open("testdata/models/not_authorize_access.json", "rb") as f:
            mock_get.return_value = Mock(ok=True)
            mock_get.return_value.content = f.read()
        with self.assertRaises(HEREError) as cm:
            vector_tile = self._api.get_vectortile(
                latitude=52.525439,
                longitude=13.38727,
                zoom=12,
                layer=VectorMapTileLayer.core,
            )
        self.assertEqual(
            "These credentials do not authorize access, error occurred on get_vectortile",
            str(cm.exception),
        )
