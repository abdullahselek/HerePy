#!/usr/bin/env python

import codecs
import datetime
import json
import unittest
from contextlib import asynccontextmanager
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock, mock_open, patch, sentinel

import httpx2
import pytest
import responses

import herepy
from herepy import (
    Avoid,
    AvoidArea,
    AvoidFeature,
    ShippedHazardousGood,
    Truck,
    TruckType,
    TunnelCategory,
)
from herepy.routing_api import error_from_routing_service_error


class AsyncRoutingApiTest(unittest.IsolatedAsyncioTestCase):
    async def test_async_route_method_wrappers(self):
        api = herepy.RoutingApi("api_key")
        point_a, point_b, point_c = [41.9798, -87.8801], [41.9043, -87.9216], [41.88, -87.90]
        cases = [
            ("async_bicycle_route", (point_a, point_b)),
            ("async_car_route", (point_a, point_b)),
            ("async_pedestrian_route", (point_a, point_b)),
            ("async_intermediate_route", (point_a, point_b, point_c)),
            ("async_public_transport", (point_a, point_b, True)),
            ("async_public_transport_timetable", (point_a, point_b, True)),
            ("async_location_near_motorway", (point_a, point_b)),
            ("async_truck_route", (point_a, point_b)),
        ]
        async with api:
            with patch.object(api, "_route_async", new=AsyncMock(return_value=sentinel.response)) as route:
                for method_name, arguments in cases:
                    with self.subTest(method=method_name):
                        self.assertIs(await getattr(api, method_name)(*arguments), sentinel.response)
                        route.assert_awaited()
                        route.reset_mock()

    async def test_async_route_v8(self):
        with open("testdata/models/routing_v8_response.json", encoding="utf-8") as file:
            payload = json.load(file)
        api = herepy.RoutingApi("api_key")
        async with api:
            client = api._get_async_client()
            with (
                patch.object(client, "get", new=AsyncMock(return_value=httpx2.Response(200, json=payload))) as get,
                patch.object(herepy.RoutingResponseV8, "new_from_jsondict", return_value=sentinel.response),
            ):
                result = await api.async_route_v8(
                    herepy.RoutingTransportMode.car,
                    [52.5, 13.4],
                    [52.6, 13.5],
                    via=[[52.55, 13.45]],
                    departure_time="2024-01-01T12:00:00",
                    routing_mode=herepy.RoutingMode.fast,
                    alternatives=2,
                    avoid={"features": ["tollRoad"]},
                    exclude={"countries": ["USA"]},
                    units=herepy.RoutingMetric.metric,
                    lang="en",
                    span_fields=[herepy.RoutingApiSpanField.length],
                    vehicle={"shippedHazardousGoods": ["flammable"]},
                    scooter={"allowHighway": "true"},
                    headers={"X-Test": "value"},
                )

        self.assertIs(result, sentinel.response)
        get.assert_awaited_once()

    async def test_async_matrix_sync_method(self):
        with open("testdata/models/routing_matrix.json", encoding="utf-8") as file:
            payload = json.load(file)
        api = herepy.RoutingApi("api_key")
        async with api:
            client = api._get_async_client()
            with (
                patch.object(client, "post", new=AsyncMock(return_value=httpx2.Response(200, json=payload))) as post,
                patch.object(herepy.RoutingMatrixResponse, "new_from_jsondict", return_value=sentinel.response),
            ):
                avoid = Avoid(features=[AvoidFeature.toll_road], areas=[AvoidArea(north=30, south=45, west=30, east=45)])
                truck = Truck(
                    shipped_hazardous_goods=[ShippedHazardousGood.flammable],
                    gross_weight=750,
                    weight_per_axle=100,
                    height=2000,
                    width=350,
                    length=10000,
                    tunnel_category=TunnelCategory.c,
                    axle_count=5,
                    truck_type=TruckType.tractor,
                    trailer_count=5,
                )
                result = await api.async_sync_matrix(
                    [[1.0, 2.0]],
                    [[3.0, 4.0]],
                    matrix_type=herepy.MatrixRoutingType.circle,
                    center=[2.0, 3.0],
                    radius=10000,
                    profile=herepy.MatrixRoutingProfile.car_fast,
                    departure="2024-01-01T12:00:00",
                    routing_mode=herepy.MatrixRoutingMode.fast,
                    transport_mode=herepy.MatrixRoutingTransportMode.car,
                    avoid=avoid,
                    truck=truck,
                    matrix_attributes=[herepy.MatrixSummaryAttribute.travel_times],
                )

        self.assertIs(result, sentinel.response)
        post.assert_awaited_once()

    async def test_async_matrix_async_polls_until_complete(self):
        with open("testdata/models/routing_async_matrix_calculation.json", encoding="utf-8") as file:
            accepted = json.load(file)
        with open("testdata/models/routing_async_matrix_completed.json", encoding="utf-8") as file:
            completed = json.load(file)
        api = herepy.RoutingApi("api_key")
        async with api:
            client = api._get_async_client()
            with (
                patch.object(client, "post", new=AsyncMock(return_value=httpx2.Response(202, json=accepted))) as post,
                patch.object(
                    client,
                    "get",
                    new=AsyncMock(
                        side_effect=[
                            httpx2.Response(200, json={"matrixId": "matrix", "status": "processing"}),
                            httpx2.Response(200, json=completed),
                        ]
                    ),
                ) as get,
                patch("herepy.routing_api.asyncio.sleep", new=AsyncMock()) as sleep,
                patch.object(herepy.RoutingMatrixResponse, "new_from_jsondict", return_value=sentinel.response),
            ):
                result = await api.async_matrix_async("token", [[1.0, 2.0]], [[3.0, 4.0]])

        self.assertIs(result, sentinel.response)
        post.assert_awaited_once()
        self.assertEqual(get.await_count, 2)
        sleep.assert_awaited_once_with(5)

    async def test_async_route_geocodes_named_waypoints(self):
        with open("testdata/models/routing_car_route_short.json", encoding="utf-8") as file:
            route_payload = json.load(file)
        api = herepy.RoutingApi("api_key")
        geocode = SimpleNamespace(
            items=[
                {"position": {"lat": 1.0, "lng": 2.0}},
                {"position": {"lat": 3.0, "lng": 4.0}},
            ]
        )
        async with api:
            with (
                patch.object(
                    api._get_async_client(),
                    "get",
                    new=AsyncMock(return_value=httpx2.Response(200, json=route_payload)),
                ),
                patch("herepy.routing_api.GeocoderApi.async_free_form", new=AsyncMock(return_value=geocode)) as geocoder,
            ):
                result = await api.async_car_route("Berlin", "Paris")

        self.assertIsInstance(result, herepy.RoutingResponse)
        self.assertEqual(geocoder.await_count, 2)

    async def test_async_matrix_file_download(self):
        api = herepy.RoutingApi("api_key")
        writer = mock_open()
        response = SimpleNamespace(raise_for_status=Mock())

        async def iter_bytes(chunk_size):
            self.assertEqual(chunk_size, 8192)
            yield b"matrix-data"

        response.aiter_bytes = iter_bytes

        @asynccontextmanager
        async def stream(method, url, timeout):
            self.assertEqual((method, url, timeout), ("GET", "https://example.com/matrix.csv", 20))
            yield response

        async with api:
            with patch.object(api._get_async_client(), "stream", new=stream), patch("builtins.open", writer):
                filename = await api._RoutingApi__download_file_async("https://example.com/matrix.csv")

        self.assertEqual(filename, "matrix.csv")
        writer().write.assert_called_once_with(b"matrix-data")


class RoutingApiTest(unittest.TestCase):
    def setUp(self):
        api = herepy.RoutingApi("api_key")
        self._api = api

    def test_initiation(self):
        self.assertIsInstance(self._api, herepy.RoutingApi)
        self.assertEqual(self._api._api_key, "api_key")

    def test_routing_service_error_categories(self):
        cases = [
            ({"status": 403, "cause": "forbidden", "action": "check access"}, herepy.AccessDeniedError),
            ({"subtype": "LinkIdNotFound", "details": "unknown link"}, herepy.LinkIdNotFoundError),
            ({"subtype": "RouteNotReconstructed", "details": "route unavailable"}, herepy.RouteNotReconstructedError),
            ({"subtype": "UnknownSubtype", "details": "unknown"}, herepy.HEREError),
            ({"error": "Other", "error_description": "server error"}, herepy.HEREError),
        ]
        for payload, expected_error in cases:
            with self.subTest(payload=payload):
                self.assertIsInstance(error_from_routing_service_error(payload), expected_error)

    @patch("herepy.routing_api.requests.post")
    def test_async_matrix_maps_service_error_responses(self, mock_post):
        cases = [
            ({"error": "Unauthorized", "error_description": "invalid token"}, "invalid token"),
            ({"title": "Bad request", "cause": "invalid matrix"}, "Bad request"),
            ({"message": "unexpected"}, "async_matrix"),
        ]
        for payload, expected_message in cases:
            with self.subTest(payload=payload):
                mock_post.return_value.status_code = 400
                mock_post.return_value.json.return_value = payload
                with self.assertRaisesRegex(herepy.HEREError, expected_message):
                    self._api.async_matrix(token="token", origins=[[1.0, 2.0]], destinations=[[3.0, 4.0]])

    @responses.activate
    def test_bicycleroute_withdefaultmodes_whensucceed(self):
        with codecs.open("testdata/models/routing_bicycle.json", mode="r", encoding="utf-8") as f:
            expectedResponse = f.read()
        responses.add(
            responses.GET,
            "https://route.ls.hereapi.com/routing/7.2/calculateroute.json",
            expectedResponse,
            status=200,
        )
        response = self._api.bicycle_route([41.9798, -87.8801], [41.9043, -87.9216])
        self.assertTrue(response)
        self.assertIsInstance(response, herepy.RoutingResponse)

    @responses.activate
    def test_bicycleroute_route_short(self):
        with codecs.open("testdata/models/routing_bicycle.json", mode="r", encoding="utf-8") as f:
            expectedResponse = f.read()
        responses.add(
            responses.GET,
            "https://route.ls.hereapi.com/routing/7.2/calculateroute.json",
            expectedResponse,
            status=200,
        )
        response = self._api.bicycle_route([41.9798, -87.8801], [41.9043, -87.9216])
        expected_short_route = (
            "Mannheim Rd; W Belmont Ave; Cullerton St; N Landen Dr; "
            "E Fullerton Ave; N Wolf Rd; W North Ave; N Clinton Ave; "
            "E Third St; N Caroline Ave"
        )
        self.assertEqual(response.route_short, expected_short_route)

    @responses.activate
    def test_carroute_whensucceed(self):
        with codecs.open("testdata/models/routing.json", mode="r", encoding="utf-8") as f:
            expectedResponse = f.read()
        responses.add(
            responses.GET,
            "https://route.ls.hereapi.com/routing/7.2/calculateroute.json",
            expectedResponse,
            status=200,
        )
        response = self._api.car_route([11.0, 12.0], [22.0, 23.0], [herepy.RouteMode.car, herepy.RouteMode.fastest])
        self.assertTrue(response)
        self.assertIsInstance(response, herepy.RoutingResponse)

    @responses.activate
    def test_carroute_route_short(self):
        with codecs.open("testdata/models/routing_car_route_short.json", mode="r", encoding="utf-8") as f:
            expectedResponse = f.read()
        responses.add(
            responses.GET,
            "https://route.ls.hereapi.com/routing/7.2/calculateroute.json",
            expectedResponse,
            status=200,
        )
        response = self._api.car_route([38.9, -77.04833], [39.0, -77.1])
        expected_short_route = "US-29 - K St NW; US-29 - Whitehurst Fwy; I-495 N - Capital Beltway; MD-187 S - Old Georgetown Rd"
        self.assertEqual(response.route_short, expected_short_route)

    @responses.activate
    def test_carroute_withdefaultmodes_whensucceed(self):
        with codecs.open("testdata/models/routing.json", mode="r", encoding="utf-8") as f:
            expectedResponse = f.read()
        responses.add(
            responses.GET,
            "https://route.ls.hereapi.com/routing/7.2/calculateroute.json",
            expectedResponse,
            status=200,
        )
        response = self._api.car_route([11.0, 12.0], [22.0, 23.0])
        self.assertTrue(response)
        self.assertIsInstance(response, herepy.RoutingResponse)

    @responses.activate
    def test_carroute_when_error_invalid_input_data_occurred(self):
        with open("testdata/models/routing_error_invalid_input_data.json") as f:
            expectedResponse = f.read()
        responses.add(
            responses.GET,
            "https://route.ls.hereapi.com/routing/7.2/calculateroute.json",
            expectedResponse,
            status=400,
        )
        with self.assertRaises(herepy.InvalidInputDataError):
            self._api.car_route(
                [11.0, 12.0],
                [22.0, 23.0],
                [herepy.RouteMode.bicycle, herepy.RouteMode.traffic_disabled],
            )

    @responses.activate
    def test_carroute_when_error_invalid_credentials_occurred(self):
        with open("testdata/models/routing_error_invalid_credentials.json") as f:
            expectedResponse = f.read()
        responses.add(
            responses.GET,
            "https://route.ls.hereapi.com/routing/7.2/calculateroute.json",
            expectedResponse,
            status=401,
        )
        api = herepy.RoutingApi("wrong_api_key", "wrong_app_code")
        with self.assertRaises(herepy.InvalidCredentialsError):
            api.car_route([11.0, 12.0], [22.0, 23.0])

    @responses.activate
    def test_carroute_when_error_forbidden_credentials_occurred(self):
        with open("testdata/models/routing_error_forbidden_credentials.json") as f:
            expectedResponse = f.read()
        responses.add(
            responses.GET,
            "https://route.ls.hereapi.com/routing/7.2/calculateroute.json",
            expectedResponse,
            status=401,
        )
        api = herepy.RoutingApi("forbidden_api_key", "forbidden_app_code")
        with self.assertRaises(herepy.InvalidCredentialsError):
            api.car_route([11.0, 12.0], [22.0, 23.0])

    @responses.activate
    def test_carroute_when_error_no_route_found_occurred(self):
        with open("testdata/models/routing_error_no_route_found.json") as f:
            expectedResponse = f.read()
        responses.add(
            responses.GET,
            "https://route.ls.hereapi.com/routing/7.2/calculateroute.json",
            expectedResponse,
            status=400,
        )
        with self.assertRaises(herepy.NoRouteFoundError):
            self._api.car_route([11.0, 12.0], [47.013399, -10.171986])

    @responses.activate
    def test_pedestrianroute_whensucceed(self):
        with codecs.open("testdata/models/routing_pedestrian.json", mode="r", encoding="utf-8") as f:
            expectedResponse = f.read()
        responses.add(
            responses.GET,
            "https://route.ls.hereapi.com/routing/7.2/calculateroute.json",
            expectedResponse,
            status=200,
        )
        response = self._api.pedestrian_route(
            [11.0, 12.0],
            [22.0, 23.0],
            [herepy.RouteMode.pedestrian, herepy.RouteMode.fastest],
        )
        self.assertTrue(response)
        self.assertIsInstance(response, herepy.RoutingResponse)

    @responses.activate
    def test_pedestrianroute_withdefaultmodes_whensucceed(self):
        with codecs.open("testdata/models/routing_pedestrian.json", mode="r", encoding="utf-8") as f:
            expectedResponse = f.read()
        responses.add(
            responses.GET,
            "https://route.ls.hereapi.com/routing/7.2/calculateroute.json",
            expectedResponse,
            status=200,
        )
        response = self._api.pedestrian_route([11.0, 12.0], [22.0, 23.0])
        self.assertTrue(response)
        self.assertIsInstance(response, herepy.RoutingResponse)

    @responses.activate
    def test_pedestrianroute_when_error_invalid_input_data_occurred(self):
        with open("testdata/models/routing_error_invalid_input_data.json") as f:
            expectedResponse = f.read()
        responses.add(
            responses.GET,
            "https://route.ls.hereapi.com/routing/7.2/calculateroute.json",
            expectedResponse,
            status=400,
        )
        with self.assertRaises(herepy.InvalidInputDataError):
            self._api.pedestrian_route(
                [11.0, 12.0],
                [22.0, 23.0],
                [herepy.RouteMode.bicycle, herepy.RouteMode.traffic_disabled],
            )

    @responses.activate
    def test_pedestrianroute_when_error_invalid_credentials_occurred(self):
        with open("testdata/models/routing_error_invalid_credentials.json") as f:
            expectedResponse = f.read()
        responses.add(
            responses.GET,
            "https://route.ls.hereapi.com/routing/7.2/calculateroute.json",
            expectedResponse,
            status=401,
        )
        api = herepy.RoutingApi("wrong_api_key", "wrong_app_code")
        with self.assertRaises(herepy.InvalidCredentialsError):
            api.pedestrian_route([11.0, 12.0], [22.0, 23.0])

    @responses.activate
    def test_pedestrianroute_when_error_no_route_found_occurred(self):
        with open("testdata/models/routing_error_no_route_found.json") as f:
            expectedResponse = f.read()
        responses.add(
            responses.GET,
            "https://route.ls.hereapi.com/routing/7.2/calculateroute.json",
            expectedResponse,
            status=400,
        )
        with self.assertRaises(herepy.NoRouteFoundError):
            self._api.pedestrian_route([11.0, 12.0], [47.013399, -10.171986])

    @responses.activate
    def test_pedestrianroute_route_short(self):
        with codecs.open("testdata/models/routing_pedestrian.json", mode="r", encoding="utf-8") as f:
            expectedResponse = f.read()
        responses.add(
            responses.GET,
            "https://route.ls.hereapi.com/routing/7.2/calculateroute.json",
            expectedResponse,
            status=200,
        )
        response = self._api.pedestrian_route(
            [11.0, 12.0],
            [22.0, 23.0],
            [herepy.RouteMode.pedestrian, herepy.RouteMode.fastest],
        )
        expected_short_route = (
            "Mannheim Rd; W Belmont Ave; Cullerton St; E Fullerton Ave; "
            "La Porte Ave; E Palmer Ave; N Railroad Ave; W North Ave; "
            "E North Ave; E Third St"
        )
        self.assertEqual(response.route_short, expected_short_route)

    @responses.activate
    def test_intermediateroute_whensucceed(self):
        with codecs.open("testdata/models/routing.json", mode="r", encoding="utf-8") as f:
            expectedResponse = f.read()
        responses.add(
            responses.GET,
            "https://route.ls.hereapi.com/routing/7.2/calculateroute.json",
            expectedResponse,
            status=200,
        )
        response = self._api.intermediate_route(
            [11.0, 12.0],
            [15.0, 16.0],
            [22.0, 23.0],
            [herepy.RouteMode.car, herepy.RouteMode.fastest],
        )
        self.assertTrue(response)
        self.assertIsInstance(response, herepy.RoutingResponse)

    @responses.activate
    def test_intermediateroute_withdefaultmodes_whensucceed(self):
        with codecs.open("testdata/models/routing.json", mode="r", encoding="utf-8") as f:
            expectedResponse = f.read()
        responses.add(
            responses.GET,
            "https://route.ls.hereapi.com/routing/7.2/calculateroute.json",
            expectedResponse,
            status=200,
        )
        response = self._api.intermediate_route([11.0, 12.0], [15.0, 16.0], [22.0, 23.0])
        self.assertTrue(response)
        self.assertIsInstance(response, herepy.RoutingResponse)

    @responses.activate
    def test_intermediateroute_when_error_invalid_input_data_occurred(self):
        with open("testdata/models/routing_error_invalid_input_data.json") as f:
            expectedResponse = f.read()
        responses.add(
            responses.GET,
            "https://route.ls.hereapi.com/routing/7.2/calculateroute.json",
            expectedResponse,
            status=400,
        )
        with self.assertRaises(herepy.InvalidInputDataError):
            self._api.intermediate_route(
                [11.0, 12.0],
                [15.0, 16.0],
                [22.0, 23.0],
                [herepy.RouteMode.car, herepy.RouteMode.fastest],
            )

    @responses.activate
    def test_intermediateroute_when_error_invalid_credentials_occurred(self):
        with open("testdata/models/routing_error_invalid_credentials.json") as f:
            expectedResponse = f.read()
        responses.add(
            responses.GET,
            "https://route.ls.hereapi.com/routing/7.2/calculateroute.json",
            expectedResponse,
            status=401,
        )
        api = herepy.RoutingApi("wrong_api_key", "wrong_app_code")
        with self.assertRaises(herepy.InvalidCredentialsError):
            api.intermediate_route([11.0, 12.0], [15.0, 16.0], [22.0, 23.0])

    @responses.activate
    def test_intermediateroute_when_error_no_route_found_occurred(self):
        with open("testdata/models/routing_error_no_route_found.json") as f:
            expectedResponse = f.read()
        responses.add(
            responses.GET,
            "https://route.ls.hereapi.com/routing/7.2/calculateroute.json",
            expectedResponse,
            status=400,
        )
        with self.assertRaises(herepy.NoRouteFoundError):
            self._api.intermediate_route([11.0, 12.0], [47.013399, -10.171986], [22.0, 23.0])

    @responses.activate
    def test_publictransport_whensucceed(self):
        with codecs.open("testdata/models/routing_public.json", mode="r", encoding="utf-8") as f:
            expectedResponse = f.read()
        responses.add(
            responses.GET,
            "https://route.ls.hereapi.com/routing/7.2/calculateroute.json",
            expectedResponse,
            status=200,
        )
        response = self._api.public_transport(
            [11.0, 12.0],
            [15.0, 16.0],
            True,
            [herepy.RouteMode.publicTransport, herepy.RouteMode.fastest],
        )
        self.assertTrue(response)
        self.assertIsInstance(response, herepy.RoutingResponse)

    @responses.activate
    def test_publictransport_route_short(self):
        with codecs.open("testdata/models/routing_public.json", mode="r", encoding="utf-8") as f:
            expectedResponse = f.read()
        responses.add(
            responses.GET,
            "https://route.ls.hereapi.com/routing/7.2/calculateroute.json",
            expectedResponse,
            status=200,
        )
        response = self._api.public_transport([11.0, 12.0], [15.0, 16.0], True)
        expected_short_route = "332 - Palmer/Schiller; 332 - Cargo Rd./Delta Cargo; 332 - Palmer/Schiller"
        self.assertEqual(response.route_short, expected_short_route)

    @responses.activate
    def test_publictransport_withdefaultmodes_whensucceed(self):
        with codecs.open("testdata/models/routing_public.json", mode="r", encoding="utf-8") as f:
            expectedResponse = f.read()
        responses.add(
            responses.GET,
            "https://route.ls.hereapi.com/routing/7.2/calculateroute.json",
            expectedResponse,
            status=200,
        )
        response = self._api.public_transport([11.0, 12.0], [15.0, 16.0], True)
        self.assertTrue(response)
        self.assertIsInstance(response, herepy.RoutingResponse)

    @responses.activate
    def test_publictransport_when_error_invalid_input_data_occurred(self):
        with open("testdata/models/routing_error_invalid_input_data.json") as f:
            expectedResponse = f.read()
        responses.add(
            responses.GET,
            "https://route.ls.hereapi.com/routing/7.2/calculateroute.json",
            expectedResponse,
            status=400,
        )
        with self.assertRaises(herepy.InvalidInputDataError):
            self._api.public_transport(
                [11.0, 12.0],
                [15.0, 16.0],
                True,
                [herepy.RouteMode.bicycle, herepy.RouteMode.traffic_disabled],
            )

    @responses.activate
    def test_publictransport_when_error_invalid_credentials_occurred(self):
        with open("testdata/models/routing_error_invalid_credentials.json") as f:
            expectedResponse = f.read()
        responses.add(
            responses.GET,
            "https://route.ls.hereapi.com/routing/7.2/calculateroute.json",
            expectedResponse,
            status=401,
        )
        api = herepy.RoutingApi("wrong_api_key", "wrong_app_code")
        with self.assertRaises(herepy.InvalidCredentialsError):
            api.public_transport([11.0, 12.0], [15.0, 16.0], True)

    @responses.activate
    def test_publictransport_when_error_no_route_found_occurred(self):
        with open("testdata/models/routing_error_no_route_found.json") as f:
            expectedResponse = f.read()
        responses.add(
            responses.GET,
            "https://route.ls.hereapi.com/routing/7.2/calculateroute.json",
            expectedResponse,
            status=400,
        )
        with self.assertRaises(herepy.NoRouteFoundError):
            self._api.public_transport([11.0, 12.0], [47.013399, -10.171986], True)

    @responses.activate
    def test_publictransporttimetable_withdefaultmodes_whensucceed(self):
        with codecs.open("testdata/models/routing_public_time_table.json", mode="r", encoding="utf-8") as f:
            expectedResponse = f.read()
        responses.add(
            responses.GET,
            "https://route.ls.hereapi.com/routing/7.2/calculateroute.json",
            expectedResponse,
            status=200,
        )
        response = self._api.public_transport_timetable([11.0, 12.0], [15.0, 16.0], True)
        self.assertTrue(response)
        self.assertIsInstance(response, herepy.RoutingResponse)

    @responses.activate
    def test_publictransporttimetable_route_short(self):
        with codecs.open("testdata/models/routing_public_time_table.json", mode="r", encoding="utf-8") as f:
            expectedResponse = f.read()
        responses.add(
            responses.GET,
            "https://route.ls.hereapi.com/routing/7.2/calculateroute.json",
            expectedResponse,
            status=200,
        )
        response = self._api.public_transport_timetable([11.0, 12.0], [15.0, 16.0], True)
        expected_short_route = "330 - Archer/Harlem (Terminal); 309 - Elmhurst Metra Station"
        self.assertEqual(response.route_short, expected_short_route)

    @responses.activate
    def test_locationnearmotorway_whensucceed(self):
        with codecs.open("testdata/models/routing.json", mode="r", encoding="utf-8") as f:
            expectedResponse = f.read()
        responses.add(
            responses.GET,
            "https://route.ls.hereapi.com/routing/7.2/calculateroute.json",
            expectedResponse,
            status=200,
        )
        response = self._api.location_near_motorway([11.0, 12.0], [22.0, 23.0], [herepy.RouteMode.car, herepy.RouteMode.fastest])
        self.assertTrue(response)
        self.assertIsInstance(response, herepy.RoutingResponse)

    @responses.activate
    def test_locationnearmotorway_withdefaultmodes_whensucceed(self):
        with codecs.open("testdata/models/routing.json", mode="r", encoding="utf-8") as f:
            expectedResponse = f.read()
        responses.add(
            responses.GET,
            "https://route.ls.hereapi.com/routing/7.2/calculateroute.json",
            expectedResponse,
            status=200,
        )
        response = self._api.location_near_motorway([11.0, 12.0], [22.0, 23.0])
        self.assertTrue(response)
        self.assertIsInstance(response, herepy.RoutingResponse)

    @responses.activate
    def test_locationnearmotorway_when_error_invalid_input_data_occurred(self):
        with open("testdata/models/routing_error_invalid_input_data.json") as f:
            expectedResponse = f.read()
        responses.add(
            responses.GET,
            "https://route.ls.hereapi.com/routing/7.2/calculateroute.json",
            expectedResponse,
            status=400,
        )
        with self.assertRaises(herepy.InvalidInputDataError):
            self._api.location_near_motorway(
                [11.0, 12.0],
                [22.0, 23.0],
                [herepy.RouteMode.bicycle, herepy.RouteMode.traffic_disabled],
            )

    @responses.activate
    def test_locationnearmotorway_when_error_invalid_credentials_occurred(self):
        with open("testdata/models/routing_error_invalid_credentials.json") as f:
            expectedResponse = f.read()
        responses.add(
            responses.GET,
            "https://route.ls.hereapi.com/routing/7.2/calculateroute.json",
            expectedResponse,
            status=401,
        )
        api = herepy.RoutingApi("wrong_api_key", "wrong_app_code")
        with self.assertRaises(herepy.InvalidCredentialsError):
            api.location_near_motorway([11.0, 12.0], [22.0, 23.0])

    @responses.activate
    def test_locationnearmotorway_when_error_no_route_found_occurred(self):
        with open("testdata/models/routing_error_no_route_found.json") as f:
            expectedResponse = f.read()
        responses.add(
            responses.GET,
            "https://route.ls.hereapi.com/routing/7.2/calculateroute.json",
            expectedResponse,
            status=400,
        )
        with self.assertRaises(herepy.NoRouteFoundError):
            self._api.location_near_motorway([11.0, 12.0], [47.013399, -10.171986])

    @responses.activate
    def test_truckroute_whensucceed(self):
        with codecs.open("testdata/models/routing.json", mode="r", encoding="utf-8") as f:
            expectedResponse = f.read()
        responses.add(
            responses.GET,
            "https://route.ls.hereapi.com/routing/7.2/calculateroute.json",
            expectedResponse,
            status=200,
        )
        response = self._api.truck_route(
            [11.0, 12.0],
            [22.0, 23.0],
            [herepy.RouteMode.truck, herepy.RouteMode.fastest],
        )
        self.assertTrue(response)
        self.assertIsInstance(response, herepy.RoutingResponse)

    @responses.activate
    def test_truckroute_route_short(self):
        with codecs.open("testdata/models/routing_truck_route_short.json", mode="r", encoding="utf-8") as f:
            expectedResponse = f.read()
        responses.add(
            responses.GET,
            "https://route.ls.hereapi.com/routing/7.2/calculateroute.json",
            expectedResponse,
            status=200,
        )
        response = self._api.truck_route([11.0, 12.0], [22.0, 23.0])
        expected_short_route = (
            "I-190; I-294 S - Tri-State Tollway; I-290 W - Eisenhower Expy W; IL-64 W - E North Ave; I-290 E - Eisenhower Expy E; I-290"
        )
        self.assertEqual(response.route_short, expected_short_route)

    @responses.activate
    def test_truckroute_withdefaultmodes_whensucceed(self):
        with codecs.open("testdata/models/routing.json", mode="r", encoding="utf-8") as f:
            expectedResponse = f.read()
        responses.add(
            responses.GET,
            "https://route.ls.hereapi.com/routing/7.2/calculateroute.json",
            expectedResponse,
            status=200,
        )
        response = self._api.truck_route([11.0, 12.0], [22.0, 23.0])
        self.assertTrue(response)
        self.assertIsInstance(response, herepy.RoutingResponse)

    @responses.activate
    def test_truckroute_when_error_invalid_input_data_occurred(self):
        with open("testdata/models/routing_error_invalid_input_data.json") as f:
            expectedResponse = f.read()
        responses.add(
            responses.GET,
            "https://route.ls.hereapi.com/routing/7.2/calculateroute.json",
            expectedResponse,
            status=400,
        )
        with self.assertRaises(herepy.InvalidInputDataError):
            self._api.truck_route(
                [11.0, 12.0],
                [22.0, 23.0],
                [herepy.RouteMode.bicycle, herepy.RouteMode.fastest],
            )

    @responses.activate
    def test_truckroute_when_error_invalid_credentials_occurred(self):
        with open("testdata/models/routing_error_invalid_credentials.json") as f:
            expectedResponse = f.read()
        responses.add(
            responses.GET,
            "https://route.ls.hereapi.com/routing/7.2/calculateroute.json",
            expectedResponse,
            status=401,
        )
        api = herepy.RoutingApi("wrong_api_key", "wrong_app_code")
        with self.assertRaises(herepy.InvalidCredentialsError):
            api.truck_route([11.0, 12.0], [22.0, 23.0])

    @responses.activate
    def test_truckroute_when_error_no_route_found_no_endpoint_occurred(self):
        with open("testdata/models/routing_error_no_route_found.json") as f:
            expectedResponse = f.read()
        responses.add(
            responses.GET,
            "https://route.ls.hereapi.com/routing/7.2/calculateroute.json",
            expectedResponse,
            status=400,
        )
        with self.assertRaises(herepy.NoRouteFoundError):
            self._api.truck_route([11.0, 12.0], [47.013399, -10.171986])

    @responses.activate
    def test_truckroute_when_error_no_route_found_graph_disconnect_occurred(self):
        with open("testdata/models/routing_error_no_route_found_truck.json") as f:
            expectedResponse = f.read()
        responses.add(
            responses.GET,
            "https://route.ls.hereapi.com/routing/7.2/calculateroute.json",
            expectedResponse,
            status=400,
        )
        with self.assertRaises(herepy.NoRouteFoundError):
            self._api.truck_route([11.0, 12.0], [33.8643661, -118.201803])

    @responses.activate
    def test_sync_matrix_whensucceed(self):
        with codecs.open("testdata/models/routing_matrix.json", mode="r", encoding="utf-8") as f:
            server_response = f.read()
        responses.add(
            responses.POST,
            "https://matrix.router.hereapi.com/v8/matrix",
            server_response,
            status=200,
        )
        avoid = Avoid(
            features=[AvoidFeature.toll_road],
            areas=[AvoidArea(north=30, south=45, west=30, east=45)],
        )
        truck = Truck(
            shipped_hazardous_goods=[
                ShippedHazardousGood.gas,
                ShippedHazardousGood.flammable,
            ],
            gross_weight=750,
            weight_per_axle=100,
            height=2000,
            width=350,
            length=10000,
            tunnel_category=TunnelCategory.c,
            axle_count=5,
            truck_type=TruckType.tractor,
            trailer_count=5,
        )
        response = self._api.sync_matrix(
            origins=[[9.933231, -84.076831]],
            destinations=[[9.934574, -84.065544]],
            matrix_type=herepy.MatrixRoutingType.circle,
            center=[9.933300, -84.066891],
            radius=10000,
            avoid=avoid,
            truck=truck,
        )
        self.assertTrue(response)
        self.assertIsInstance(response, herepy.RoutingMatrixResponse)

    @responses.activate
    def test_sync_matrix_multiple_starts(self):
        with codecs.open(
            "testdata/models/routing_matrix_multiple_starts.json",
            mode="r",
            encoding="utf-8",
        ) as f:
            server_response = f.read()
        responses.add(
            responses.POST,
            "https://matrix.router.hereapi.com/v8/matrix",
            server_response,
            status=200,
        )
        response = self._api.sync_matrix(
            origins=[[9.933231, -84.076831], [9.934574, -84.065544]],
            destinations=[[9.934574, -84.065544]],
            matrix_type=herepy.MatrixRoutingType.circle,
            center=[9.933300, -84.066891],
            radius=10000,
        )
        self.assertTrue(response)
        self.assertIsInstance(response, herepy.RoutingMatrixResponse)

    @responses.activate
    def test_sync_matrix_multiple_start_names(self):
        with codecs.open(
            "testdata/models/routing_matrix_multiple_starts.json",
            mode="r",
            encoding="utf-8",
        ) as f:
            server_response = f.read()
        responses.add(
            responses.POST,
            "https://matrix.router.hereapi.com/v8/matrix",
            server_response,
            status=200,
        )
        with open("testdata/models/geocoder.json") as f:
            expectedGeocoderResponse = f.read()
        responses.add(
            responses.GET,
            "https://geocode.search.hereapi.com/v1/geocode",
            expectedGeocoderResponse,
            status=200,
        )
        response = self._api.sync_matrix(
            origins=["Seattle", "Kentucky"],
            destinations=[[9.934574, -84.065544]],
            matrix_type=herepy.MatrixRoutingType.circle,
            center=[9.933300, -84.066891],
            radius=10000,
        )
        self.assertTrue(response)
        self.assertIsInstance(response, herepy.RoutingMatrixResponse)

    @responses.activate
    def test_sync_matrix_multiple_destinations_with_location_names(self):
        with codecs.open(
            "testdata/models/routing_matrix_multiple_destinations.json",
            mode="r",
            encoding="utf-8",
        ) as f:
            server_response = f.read()
        responses.add(
            responses.POST,
            "https://matrix.router.hereapi.com/v8/matrix",
            server_response,
            status=200,
        )
        response = self._api.sync_matrix(
            origins=[[9.933231, -84.076831]],
            destinations=[[9.934574, -84.065544], [9.612552, -84.62892]],
            matrix_type=herepy.MatrixRoutingType.circle,
            center=[9.933300, -84.066891],
            radius=10000,
        )
        self.assertTrue(response)
        self.assertIsInstance(response, herepy.RoutingMatrixResponse)

    @responses.activate
    def test_sync_matrix_multiple_destinations(self):
        with codecs.open(
            "testdata/models/routing_matrix_multiple_destinations.json",
            mode="r",
            encoding="utf-8",
        ) as f:
            server_response = f.read()
        responses.add(
            responses.POST,
            "https://matrix.router.hereapi.com/v8/matrix",
            server_response,
            status=200,
        )
        with open("testdata/models/geocoder.json") as f:
            expectedGeocoderResponse = f.read()
        responses.add(
            responses.GET,
            "https://geocode.search.hereapi.com/v1/geocode",
            expectedGeocoderResponse,
            status=200,
        )
        response = self._api.sync_matrix(
            origins=[[9.933231, -84.076831]],
            destinations=["Seattle", "Kentucky"],
            matrix_type=herepy.MatrixRoutingType.circle,
            center=[9.933300, -84.066891],
            radius=10000,
        )
        self.assertTrue(response)
        self.assertIsInstance(response, herepy.RoutingMatrixResponse)

    @responses.activate
    def test_sync_matrix_bad_request(self):
        with codecs.open(
            "testdata/models/routing_matrix_bad_request.json",
            mode="r",
            encoding="utf-8",
        ) as f:
            server_response = f.read()
        responses.add(
            responses.POST,
            "https://matrix.router.hereapi.com/v8/matrix",
            server_response,
            status=400,
        )
        with self.assertRaises(herepy.HEREError):
            self._api.sync_matrix(
                origins=[[9.933231, -84.076831]],
                destinations=[[9.934574, -84.065544]],
                matrix_type=herepy.MatrixRoutingType.circle,
                center=[9.933300, -84.066891],
                radius=10000,
                routing_mode=herepy.MatrixRoutingMode.fast,
            )

    @responses.activate
    def test_async_matrix_whensucceed(self):
        with open(
            "testdata/models/routing_async_matrix_calculation.json",
            encoding="utf-8",
        ) as f:
            server_response = f.read()
        responses.add(
            responses.POST,
            "https://matrix.router.hereapi.com/v8/matrix",
            server_response,
            status=202,
        )
        with open(
            "testdata/models/routing_async_matrix_completed.json",
            encoding="utf-8",
        ) as f:
            server_response = f.read()
        responses.add(
            responses.GET,
            "https://com.com/status",
            server_response,
            status=200,
        )
        avoid = Avoid(
            features=[AvoidFeature.toll_road],
            areas=[AvoidArea(north=30, south=45, west=30, east=45)],
        )
        truck = Truck(
            shipped_hazardous_goods=[
                ShippedHazardousGood.gas,
                ShippedHazardousGood.flammable,
            ],
            gross_weight=750,
            weight_per_axle=100,
            height=2000,
            width=350,
            length=10000,
            tunnel_category=TunnelCategory.c,
            axle_count=5,
            truck_type=TruckType.tractor,
            trailer_count=5,
        )
        response = self._api.async_matrix(
            token="token",
            origins=[[9.933231, -84.076831]],
            destinations=[[9.934574, -84.065544]],
            matrix_type=herepy.MatrixRoutingType.circle,
            center=[9.933300, -84.066891],
            radius=10000,
            avoid=avoid,
            truck=truck,
        )
        self.assertTrue(response)
        self.assertIsInstance(response, herepy.RoutingMatrixResponse)

    @responses.activate
    def test_departure_as_datetime(self):
        with codecs.open("testdata/models/routing_truck_route_short.json", mode="r", encoding="utf-8") as f:
            expectedResponse = f.read()
        responses.add(
            responses.GET,
            "https://route.ls.hereapi.com/routing/7.2/calculateroute.json",
            expectedResponse,
            status=200,
        )
        date = datetime.datetime(2013, 7, 4, 17, 0, tzinfo=datetime.timezone(datetime.timedelta(0, 7200)))
        response = self._api.truck_route([11.0, 12.0], [22.0, 23.0], departure=date)
        self.assertTrue(response)
        self.assertIsInstance(response, herepy.RoutingResponse)

    @responses.activate
    def test_departure_as_string(self):
        with codecs.open("testdata/models/routing_truck_route_short.json", mode="r", encoding="utf-8") as f:
            expectedResponse = f.read()
        responses.add(
            responses.GET,
            "https://route.ls.hereapi.com/routing/7.2/calculateroute.json",
            expectedResponse,
            status=200,
        )
        date = "2013-07-04T17:00:00+02:00"
        response = self._api.truck_route([11.0, 12.0], [22.0, 23.0], departure=date)
        self.assertTrue(response)
        self.assertIsInstance(response, herepy.RoutingResponse)

    @responses.activate
    def test_arrival_as_string(self):
        with codecs.open("testdata/models/routing_public_time_table.json", mode="r", encoding="utf-8") as f:
            expectedResponse = f.read()
        responses.add(
            responses.GET,
            "https://route.ls.hereapi.com/routing/7.2/calculateroute.json",
            expectedResponse,
            status=200,
        )
        date = "2013-07-04T17:00:00+02:00"
        response = self._api.public_transport_timetable([11.0, 12.0], [15.0, 16.0], True, arrival=date)
        self.assertTrue(response)
        self.assertIsInstance(response, herepy.RoutingResponse)

    @responses.activate
    def test_arrival_as_datetime(self):
        with codecs.open("testdata/models/routing_public_time_table.json", mode="r", encoding="utf-8") as f:
            expectedResponse = f.read()
        responses.add(
            responses.GET,
            "https://route.ls.hereapi.com/routing/7.2/calculateroute.json",
            expectedResponse,
            status=200,
        )
        date = datetime.datetime(2013, 7, 4, 17, 0, tzinfo=datetime.timezone(datetime.timedelta(0, 7200)))
        response = self._api.public_transport_timetable([11.0, 12.0], [15.0, 16.0], True, arrival=date)
        self.assertTrue(response)
        self.assertIsInstance(response, herepy.RoutingResponse)

    @responses.activate
    def test_error_arrival_and_departure_set(self):
        with codecs.open("testdata/models/routing_public_time_table.json", mode="r", encoding="utf-8") as f:
            expectedResponse = f.read()
        responses.add(
            responses.GET,
            "https://route.ls.hereapi.com/routing/7.2/calculateroute.json",
            expectedResponse,
            status=200,
        )
        with self.assertRaises(herepy.HEREError):
            self._api.public_transport_timetable(
                [11.0, 12.0],
                [15.0, 16.0],
                True,
                departure="2023-01-01T00:00:00",
                arrival="2023-01-01T00:00:00",
            )

    @responses.activate
    def test_location_by_name(self):
        with codecs.open("testdata/models/routing_truck_route_short.json", mode="r", encoding="utf-8") as f:
            expectedRoutingResponse = f.read()
        responses.add(
            responses.GET,
            "https://route.ls.hereapi.com/routing/7.2/calculateroute.json",
            expectedRoutingResponse,
            status=200,
        )
        with open("testdata/models/geocoder.json") as f:
            expectedGeocoderResponse = f.read()
        responses.add(
            responses.GET,
            "https://geocode.search.hereapi.com/v1/geocode",
            expectedGeocoderResponse,
            status=200,
        )
        response = self._api.truck_route("200 S Mathilda Sunnyvale CA", "200 S Mathilda Sunnyvale CA")
        self.assertTrue(response)
        self.assertIsInstance(response, herepy.RoutingResponse)

    @responses.activate
    def test_location_by_name_throws_WaypointNotFoundError(self):
        with codecs.open("testdata/models/routing_truck_route_short.json", mode="r", encoding="utf-8") as f:
            expectedRoutingResponse = f.read()
        responses.add(
            responses.GET,
            "https://route.ls.hereapi.com/routing/7.2/calculateroute.json",
            expectedRoutingResponse,
            status=200,
        )
        with open("testdata/models/geocoder_error.json") as f:
            expectedGeocoderResponse = f.read()
        responses.add(
            responses.GET,
            "https://geocode.search.hereapi.com/v1/geocode",
            expectedGeocoderResponse,
            status=200,
        )
        with self.assertRaises(herepy.WaypointNotFoundError):
            response = self._api.truck_route("200 S Mathilda Sunnyvale CA", "200 S Mathilda Sunnyvale CA")

    @patch("herepy.routing_api.GeocoderApi.free_form", side_effect=[None, herepy.GeocoderResponse(items=[])])
    def test_location_by_name_without_geocoder_results_raises_WaypointNotFoundError(self, _free_form):
        for location_name in ("Unknown location", "Empty result"):
            with self.subTest(location_name=location_name), self.assertRaises(herepy.WaypointNotFoundError):
                self._api._get_coordinates_for_location_name(location_name)

    @responses.activate
    def test_route_v8_success(self):
        with codecs.open("testdata/models/routing_v8_response.json", mode="r", encoding="utf-8") as f:
            expectedResponse = f.read()
        responses.add(
            responses.GET,
            "https://router.hereapi.com/v8/routes",
            expectedResponse,
            status=200,
        )
        response = self._api.route_v8(
            transport_mode=herepy.RoutingTransportMode.car,
            origin=[41.9798, -87.8801],
            destination=[41.9043, -87.9216],
            via=[[41.9339, -87.9021], [41.9379, -87.9121]],
            routing_mode=herepy.RoutingMode.fast,
            avoid={"features": ["controlledAccessHighway", "tunnel"]},
            exclude={"countries": ["TUR"]},
            units=herepy.RoutingMetric.metric,
            lang="tr-TR",
            return_fields=[herepy.RoutingApiReturnField.polyline],
            span_fields=[herepy.RoutingApiSpanField.walkAttributes],
            vehicle={"shippedHazardousGoods": ["explosive", "gas"]},
            scooter={"allowHighway": "true"},
        )
        self.assertTrue(response)
        self.assertIsInstance(response, herepy.RoutingResponseV8)

    @responses.activate
    def test_route_v8_geocodes_named_endpoints(self):
        with open("testdata/models/geocoder.json", encoding="utf-8") as f:
            geocoder_response = f.read()
        for _ in range(2):
            responses.get("https://geocode.search.hereapi.com/v1/geocode", geocoder_response)
        responses.get("https://router.hereapi.com/v8/routes", json={"routes": []})

        response = self._api.route_v8(
            transport_mode=herepy.RoutingTransportMode.car,
            origin="Berlin",
            destination="Potsdam",
        )

        self.assertIsInstance(response, herepy.RoutingResponseV8)
        self.assertEqual(len(responses.calls), 3)

    @responses.activate
    def test_route_v8_error_invalid_credentials(self):
        with open(
            "testdata/models/routing_error_invalid_credentials.json",
            encoding="utf-8",
        ) as f:
            expectedResponse = f.read()
        responses.add(
            responses.GET,
            "https://router.hereapi.com/v8/routes",
            expectedResponse,
            status=401,
        )
        api = herepy.RoutingApi("wrong_api_key", "wrong_app_code")
        with self.assertRaises(herepy.InvalidCredentialsError):
            api.route_v8(
                transport_mode=herepy.RoutingTransportMode.car,
                origin=[41.9798, -87.8801],
                destination=[41.9043, -87.9216],
                via=[[41.9339, -87.9021], [41.9379, -87.9121]],
                routing_mode=herepy.RoutingMode.fast,
                avoid={"features": ["controlledAccessHighway", "tunnel"]},
                exclude={"countries": ["TUR"]},
                units=herepy.RoutingMetric.metric,
                lang="tr-TR",
                return_fields=[herepy.RoutingApiReturnField.polyline],
                span_fields=[herepy.RoutingApiSpanField.walkAttributes],
                vehicle={"shippedHazardousGoods": ["explosive", "gas"]},
                scooter={"allowHighway": "true"},
            )

    @responses.activate
    def test_route_v8_error_malformed_request(self):
        """Usually this error occurs"""
        with codecs.open(
            "testdata/models/routing_v8_error_malformed_req.json",
            mode="r",
            encoding="utf-8",
        ) as f:
            expectedResponse = f.read()
        responses.add(
            responses.GET,
            "https://router.hereapi.com/v8/routes",
            expectedResponse,
            status=400,
        )
        with self.assertRaises(herepy.InvalidRequestError):
            self._api.route_v8(
                # Incorrect order/values of positional args
                # Assume user uses ordering/values of the v7 functions
                [41.9798, -87.8801],
                [41.9043, -87.9216],
                [
                    herepy.RouteMode.truck,
                    herepy.RouteMode.balanced,
                    herepy.RouteMode.traffic_disabled,
                ],
            )

    @responses.activate
    def test_route_v8_error_access_denied(self):
        with codecs.open(
            "testdata/models/routing_v8_error_access_denied.json",
            mode="r",
            encoding="utf-8",
        ) as f:
            expectedResponse = f.read()
        responses.add(
            responses.GET,
            "https://router.hereapi.com/v8/routes",
            expectedResponse,
            status=403,
        )
        with self.assertRaises(herepy.AccessDeniedError):
            self._api.route_v8(
                transport_mode=herepy.RoutingTransportMode.car,
                origin=[41.9798, -87.8801],
                destination=[41.9043, -87.9216],
                via=[[41.9339, -87.9021], [41.9379, -87.9121]],
                routing_mode=herepy.RoutingMode.fast,
                avoid={"features": ["controlledAccessHighway", "tunnel"]},
                exclude={"countries": ["TUR"]},
                units=herepy.RoutingMetric.metric,
                lang="tr-TR",
                return_fields=[herepy.RoutingApiReturnField.polyline],
                span_fields=[herepy.RoutingApiSpanField.walkAttributes],
                vehicle={"shippedHazardousGoods": ["explosive", "gas"]},
                scooter={"allowHighway": "true"},
            )

    @responses.activate
    def test_route_v8_multiple_via_points(self):
        responses.add(
            responses.GET,
            "https://router.hereapi.com/v8/routes",
            "{}",
            status=200,
            match=[responses.matchers.query_param_matcher({"via": ["41.9339,-87.9021"] * 11}, strict_match=False)],
        )
        response = self._api.route_v8(
            transport_mode=herepy.RoutingTransportMode.car,
            origin=[41.9798, -87.8801],
            destination=[41.9043, -87.9216],
            via=[[41.9339, -87.9021]] * 11,
        )
        self.assertTrue(response)
        self.assertIsInstance(response, herepy.RoutingResponseV8)

    @responses.activate
    def test_route_v8_url_parameters_multiple(self):
        responses.add(
            responses.GET,
            "https://router.hereapi.com/v8/routes",
            "{}",
            status=200,
            match=[
                responses.matchers.query_param_matcher(
                    {"vehicle[height]": "15000", "vehicle[width]": "3000"},
                    strict_match=False,
                )
            ],
        )
        self._api.route_v8(
            transport_mode=herepy.RoutingTransportMode.truck,
            origin=[41.9798, -87.8801],
            destination=[41.9043, -87.9216],
            vehicle={"height": ["15000"], "width": ["3000"]},
        )

    @responses.activate
    @pytest.mark.filterwarnings("ignore:'truck' parameter is deprecated")
    def test_route_v8_truck_parameter_deprecated(self):
        responses.add(
            responses.GET,
            "https://router.hereapi.com/v8/routes",
            "{}",
            status=200,
            match=[
                responses.matchers.query_param_matcher(
                    {"vehicle[height]": "15000", "vehicle[width]": "3000"},
                    strict_match=False,
                )
            ],
        )
        self._api.route_v8(
            transport_mode=herepy.RoutingTransportMode.truck,
            origin=[41.9798, -87.8801],
            destination=[41.9043, -87.9216],
            truck={"height": ["15000"], "width": ["3000"]},
        )

    @responses.activate
    def test_route_v8_headers_in_request(self):
        resp = responses.add(
            responses.GET,
            "https://router.hereapi.com/v8/routes",
            "{}",
            status=200,
        )
        self._api.route_v8(
            transport_mode=herepy.RoutingTransportMode.truck,
            origin=[41.9798, -87.8801],
            destination=[41.9043, -87.9216],
            headers={"X-BIP": "BOP"},
        )
        original_request = resp.calls[0].request
        self.assertEqual(original_request.headers.get("X-BIP"), "BOP")
