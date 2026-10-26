#!/usr/bin/env python

import codecs
import unittest

import responses
from async_test_helpers import assert_async_get_cases, assert_async_get_error_case

import herepy


class AsyncTrafficApiTest(unittest.IsolatedAsyncioTestCase):
    async def test_async_traffic_methods(self):
        api = herepy.TrafficApi("api_key")
        point_a = [52.5311, 13.3644]
        point_b = [52.5114, 13.4035]
        criticality = [herepy.IncidentsCriticalityStr.minor, herepy.IncidentsCriticalityStr.major]
        corridor_points = [[51.5072, -0.1275], [51.50781, -0.13112], [51.51006, -0.1346]]
        flow_response = herepy.TrafficFlowResponse
        incident_response = herepy.TrafficIncidentResponse
        cases = [
            ("async_incidents_in_bounding_box", (point_a, point_b, criticality), incident_response, "traffic_incidents_bounding_box.json"),
            ("async_incidents_in_corridor", (corridor_points, 1000), incident_response, "traffic_incidents_corridor.json"),
            (
                "async_incidents_via_proximity",
                (52.5311, 13.3644, 1000, [herepy.IncidentsCriticalityInt.minor]),
                incident_response,
                "traffic_incidents_proximity.json",
            ),
            ("async_flow_using_quadkey", ("1202033012",), flow_response, "traffic_api_flow.json"),
            ("async_flow_within_boundingbox", (point_a, point_b), flow_response, "traffic_api_flow.json"),
            ("async_flow_using_proximity", (52.5311, 13.3644, 1000), flow_response, "traffic_api_flow.json"),
            (
                "async_flow_using_proximity_returning_additional_attributes",
                (52.5311, 13.3644, 1000, [herepy.FlowProximityAdditionalAttributes.shape]),
                flow_response,
                "traffic_api_flow_proximity_attributes.json",
            ),
            ("async_flow_with_minimum_jam_factor", (point_a, point_b), flow_response, "traffic_api_flow_minjamfactor.json"),
            ("async_flow_in_corridor", (corridor_points, 1000), flow_response, "traffic_api_flow_corridor.json"),
            (
                "async_flow_availability_data",
                (),
                herepy.TrafficFlowAvailabilityResponse,
                "traffic_api_flow_availability.json",
            ),
            (
                "async_additional_attributes",
                ("1202033012", [herepy.FlowProximityAdditionalAttributes.shape]),
                flow_response,
                "traffic_api_flow.json",
            ),
        ]
        await assert_async_get_cases(self, api, cases, incident_response)

    async def test_async_incidents_maps_unauthorized_errors(self):
        await assert_async_get_error_case(
            self,
            herepy.TrafficApi("api_key"),
            "async_incidents_in_bounding_box",
            (
                [52.5311, 13.3644],
                [52.5114, 13.4035],
                [herepy.IncidentsCriticalityStr.minor],
            ),
            "unauthorized_error.json",
            herepy.UnauthorizedError,
        )


class TrafficApiTest(unittest.TestCase):
    def setUp(self):
        api = herepy.TrafficApi("api_key")
        self._api = api

    def test_initiation(self):
        self.assertIsInstance(self._api, herepy.TrafficApi)
        self.assertEqual(self._api._api_key, "api_key")

    @responses.activate
    def test_incidents_in_bounding_box_success(self):
        with codecs.open(
            "testdata/models/traffic_incidents_bounding_box.json",
            mode="r",
            encoding="utf-8",
        ) as f:
            expectedResponse = f.read()
        responses.add(
            responses.GET,
            "https://traffic.ls.hereapi.com/traffic/6.1/incidents.json",
            expectedResponse,
            status=200,
        )
        response = self._api.incidents_in_bounding_box(
            top_left=[52.5311, 13.3644],
            bottom_right=[52.5114, 13.4035],
            criticality=[
                herepy.IncidentsCriticalityStr.minor,
                herepy.IncidentsCriticalityStr.major,
                herepy.IncidentsCriticalityStr.critical,
            ],
        )
        self.assertTrue(response)
        self.assertIsInstance(response, herepy.TrafficIncidentResponse)
        self.assertIsNotNone(response.as_dict())

    @responses.activate
    def test_incidents_in_bounding_box_fails(self):
        with codecs.open("testdata/models/unauthorized_error.json", mode="r", encoding="utf-8") as f:
            expectedResponse = f.read()
        responses.add(
            responses.GET,
            "https://traffic.ls.hereapi.com/traffic/6.1/incidents.json",
            expectedResponse,
            status=200,
        )
        with self.assertRaises(herepy.UnauthorizedError):
            self._api.incidents_in_bounding_box(
                top_left=[52.5311, 13.3644],
                bottom_right=[52.5114, 13.4035],
                criticality=[herepy.IncidentsCriticalityStr.minor],
            )

    @responses.activate
    def test_incidents_in_bounding_box_maps_invalid_request_error(self):
        responses.get(
            "https://traffic.ls.hereapi.com/traffic/6.1/incidents.json",
            json={"Type": "Invalid Request", "Message": "invalid bounding box"},
        )

        with self.assertRaisesRegex(herepy.InvalidRequestError, "invalid bounding box"):
            self._api.incidents_in_bounding_box(
                top_left=[52.5311, 13.3644],
                bottom_right=[52.5114, 13.4035],
                criticality=[herepy.IncidentsCriticalityStr.minor],
            )

    @responses.activate
    def test_incidents_in_corridor_success(self):
        with codecs.open(
            "testdata/models/traffic_incidents_corridor.json",
            mode="r",
            encoding="utf-8",
        ) as f:
            expectedResponse = f.read()
        responses.add(
            responses.GET,
            "https://traffic.ls.hereapi.com/traffic/6.1/incidents.json",
            expectedResponse,
            status=200,
        )
        response = self._api.incidents_in_corridor(
            points=[[51.5072, -0.1275], [51.50781, -0.13112], [51.51006, -0.1346]],
            width=1000,
        )
        self.assertTrue(response)
        self.assertIsInstance(response, herepy.TrafficIncidentResponse)
        self.assertIsNotNone(response.as_dict())

    @responses.activate
    def test_incidents_in_corridor_fails(self):
        with codecs.open("testdata/models/unauthorized_error.json", mode="r", encoding="utf-8") as f:
            expectedResponse = f.read()
        responses.add(
            responses.GET,
            "https://traffic.ls.hereapi.com/traffic/6.1/incidents.json",
            expectedResponse,
            status=200,
        )
        with self.assertRaises(herepy.UnauthorizedError):
            self._api.incidents_in_corridor(points=[[51.5072, -0.1275], [51.50781, -0.13112]], width=1000)

    @responses.activate
    def test_incidents_via_proximity_success(self):
        with codecs.open(
            "testdata/models/traffic_incidents_proximity.json",
            mode="r",
            encoding="utf-8",
        ) as f:
            expectedResponse = f.read()
        responses.add(
            responses.GET,
            "https://traffic.ls.hereapi.com/traffic/6.1/incidents.json",
            expectedResponse,
            status=200,
        )
        response = self._api.incidents_via_proximity(
            latitude=52.5311,
            longitude=13.3644,
            radius=15000,
            criticality=[
                herepy.IncidentsCriticalityInt.critical,
                herepy.IncidentsCriticalityInt.major,
            ],
        )
        self.assertTrue(response)
        self.assertIsInstance(response, herepy.TrafficIncidentResponse)
        self.assertIsNotNone(response.as_dict())

    @responses.activate
    def test_incidents_via_proximity_fails(self):
        with codecs.open("testdata/models/unauthorized_error.json", mode="r", encoding="utf-8") as f:
            expectedResponse = f.read()
        responses.add(
            responses.GET,
            "https://traffic.ls.hereapi.com/traffic/6.1/incidents.json",
            expectedResponse,
            status=200,
        )
        with self.assertRaises(herepy.UnauthorizedError):
            self._api.incidents_via_proximity(
                latitude=52.5311,
                longitude=13.3644,
                radius=15000,
                criticality=[
                    herepy.IncidentsCriticalityInt.critical,
                    herepy.IncidentsCriticalityInt.major,
                ],
            )

    @responses.activate
    def test_flow_using_quadkey_success(self):
        with codecs.open(
            "testdata/models/traffic_api_flow.json",
            mode="r",
            encoding="utf-8",
        ) as f:
            expectedResponse = f.read()
        responses.add(
            responses.GET,
            "https://traffic.ls.hereapi.com/traffic/6.1/flow.json",
            expectedResponse,
            status=200,
        )
        response = self._api.flow_using_quadkey(quadkey="0313131311102300")
        self.assertTrue(response)
        self.assertIsInstance(response, herepy.TrafficFlowResponse)
        self.assertIsNotNone(response.as_dict())

    @responses.activate
    def test_flow_using_quadkey_fails(self):
        with codecs.open("testdata/models/unauthorized_error.json", mode="r", encoding="utf-8") as f:
            expectedResponse = f.read()
        responses.add(
            responses.GET,
            "https://traffic.ls.hereapi.com/traffic/6.1/flow.json",
            expectedResponse,
            status=200,
        )
        with self.assertRaises(herepy.UnauthorizedError):
            self._api.flow_using_quadkey(quadkey="0313131311102300")

    @responses.activate
    def test_flow_within_boundingbox_success(self):
        with codecs.open(
            "testdata/models/traffic_api_flow.json",
            mode="r",
            encoding="utf-8",
        ) as f:
            expectedResponse = f.read()
        responses.add(
            responses.GET,
            "https://traffic.ls.hereapi.com/traffic/6.1/flow.json",
            expectedResponse,
            status=200,
        )
        response = self._api.flow_within_boundingbox(top_left=[52.5311, 13.3644], bottom_right=[52.5114, 13.4035])
        self.assertTrue(response)
        self.assertIsInstance(response, herepy.TrafficFlowResponse)
        self.assertIsNotNone(response.as_dict())

    @responses.activate
    def test_flow_within_boundingbox_fails(self):
        with codecs.open("testdata/models/unauthorized_error.json", mode="r", encoding="utf-8") as f:
            expectedResponse = f.read()
        responses.add(
            responses.GET,
            "https://traffic.ls.hereapi.com/traffic/6.1/flow.json",
            expectedResponse,
            status=200,
        )
        with self.assertRaises(herepy.UnauthorizedError):
            self._api.flow_within_boundingbox(top_left=[52.5311, 13.3644], bottom_right=[52.5114, 13.4035])

    @responses.activate
    def test_flow_using_proximity_success(self):
        with codecs.open(
            "testdata/models/traffic_api_flow_proximity.json",
            mode="r",
            encoding="utf-8",
        ) as f:
            expectedResponse = f.read()
        responses.add(
            responses.GET,
            "https://traffic.ls.hereapi.com/traffic/6.1/flow.json",
            expectedResponse,
            status=200,
        )
        response = self._api.flow_using_proximity(latitude=51.5072, longitude=-0.1275, distance=100)
        self.assertTrue(response)
        self.assertIsInstance(response, herepy.TrafficFlowResponse)
        self.assertIsNotNone(response.as_dict())

    @responses.activate
    def test_flow_using_proximity_fails(self):
        with codecs.open("testdata/models/unauthorized_error.json", mode="r", encoding="utf-8") as f:
            expectedResponse = f.read()
        responses.add(
            responses.GET,
            "https://traffic.ls.hereapi.com/traffic/6.1/flow.json",
            expectedResponse,
            status=200,
        )
        with self.assertRaises(herepy.UnauthorizedError):
            self._api.flow_using_proximity(latitude=51.5072, longitude=-0.1275, distance=100)

    @responses.activate
    def test_flow_using_proximity_returning_additional_attributes_success(self):
        with codecs.open(
            "testdata/models/traffic_api_flow_proximity_attributes.json",
            mode="r",
            encoding="utf-8",
        ) as f:
            expectedResponse = f.read()
        responses.add(
            responses.GET,
            "https://traffic.ls.hereapi.com/traffic/6.1/flow.json",
            expectedResponse,
            status=200,
        )
        response = self._api.flow_using_proximity_returning_additional_attributes(
            latitude=51.5072,
            longitude=-0.1275,
            distance=100,
            attributes=[
                herepy.here_enum.FlowProximityAdditionalAttributes.functional_class,
                herepy.here_enum.FlowProximityAdditionalAttributes.shape,
            ],
        )
        self.assertTrue(response)
        self.assertIsInstance(response, herepy.TrafficFlowResponse)
        self.assertIsNotNone(response.as_dict())

    @responses.activate
    def test_flow_using_proximity_returning_additional_attributes_fails(self):
        with codecs.open("testdata/models/unauthorized_error.json", mode="r", encoding="utf-8") as f:
            expectedResponse = f.read()
        responses.add(
            responses.GET,
            "https://traffic.ls.hereapi.com/traffic/6.1/flow.json",
            expectedResponse,
            status=200,
        )
        with self.assertRaises(herepy.UnauthorizedError):
            self._api.flow_using_proximity_returning_additional_attributes(
                latitude=51.5072,
                longitude=-0.1275,
                distance=100,
                attributes=[
                    herepy.here_enum.FlowProximityAdditionalAttributes.functional_class,
                    herepy.here_enum.FlowProximityAdditionalAttributes.shape,
                ],
            )

    @responses.activate
    def test_flow_with_minimum_jam_factor_success(self):
        with codecs.open(
            "testdata/models/traffic_api_flow_minjamfactor.json",
            mode="r",
            encoding="utf-8",
        ) as f:
            expectedResponse = f.read()
        responses.add(
            responses.GET,
            "https://traffic.ls.hereapi.com/traffic/6.1/flow.json",
            expectedResponse,
            status=200,
        )
        response = self._api.flow_with_minimum_jam_factor(
            top_left=[52.5311, 13.3644],
            bottom_right=[52.5114, 13.4035],
            min_jam_factor=7,
        )
        self.assertTrue(response)
        self.assertIsInstance(response, herepy.TrafficFlowResponse)
        self.assertIsNotNone(response.as_dict())

    @responses.activate
    def test_flow_with_minimum_jam_factor_fails(self):
        with codecs.open("testdata/models/unauthorized_error.json", mode="r", encoding="utf-8") as f:
            expectedResponse = f.read()
        responses.add(
            responses.GET,
            "https://traffic.ls.hereapi.com/traffic/6.1/flow.json",
            expectedResponse,
            status=200,
        )
        with self.assertRaises(herepy.UnauthorizedError):
            self._api.flow_with_minimum_jam_factor(
                top_left=[52.5311, 13.3644],
                bottom_right=[52.5114, 13.4035],
                min_jam_factor=7,
            )

    @responses.activate
    def test_flow_in_corridor_success(self):
        with codecs.open(
            "testdata/models/traffic_api_flow_corridor.json",
            mode="r",
            encoding="utf-8",
        ) as f:
            expectedResponse = f.read()
        responses.add(
            responses.GET,
            "https://traffic.ls.hereapi.com/traffic/6.1/flow.json",
            expectedResponse,
            status=200,
        )
        response = self._api.flow_in_corridor(
            points=[[51.5072, -0.1275], [51.50781, -0.13112], [51.51006, -0.1346]],
            width=1000,
        )
        self.assertTrue(response)
        self.assertIsInstance(response, herepy.TrafficFlowResponse)
        self.assertIsNotNone(response.as_dict())

    @responses.activate
    def test_flow_in_corridor_fails(self):
        with codecs.open("testdata/models/unauthorized_error.json", mode="r", encoding="utf-8") as f:
            expectedResponse = f.read()
        responses.add(
            responses.GET,
            "https://traffic.ls.hereapi.com/traffic/6.1/flow.json",
            expectedResponse,
            status=200,
        )
        with self.assertRaises(herepy.UnauthorizedError):
            self._api.flow_in_corridor(points=[[51.5072, -0.1275], [51.50781, -0.13112]], width=1000)

    @responses.activate
    def test_flow_availability_data_success(self):
        with codecs.open(
            "testdata/models/traffic_api_flow_availability.json",
            mode="r",
            encoding="utf-8",
        ) as f:
            expectedResponse = f.read()
        responses.add(
            responses.GET,
            "https://traffic.ls.hereapi.com/traffic/6.1/flowavailability.json",
            expectedResponse,
            status=200,
        )
        response = self._api.flow_availability_data()
        self.assertTrue(response)
        self.assertIsInstance(response, herepy.TrafficFlowAvailabilityResponse)
        self.assertIsNotNone(response.as_dict())

    @responses.activate
    def test_flow_availability_data_fails(self):
        with codecs.open("testdata/models/unauthorized_error.json", mode="r", encoding="utf-8") as f:
            expectedResponse = f.read()
        responses.add(
            responses.GET,
            "https://traffic.ls.hereapi.com/traffic/6.1/flowavailability.json",
            expectedResponse,
            status=200,
        )
        with self.assertRaises(herepy.UnauthorizedError):
            self._api.flow_availability_data()

    @responses.activate
    def test_additional_attributes_success(self):
        with codecs.open(
            "testdata/models/traffic_api_additional_attributes.json",
            mode="r",
            encoding="utf-8",
        ) as f:
            expectedResponse = f.read()
        responses.add(
            responses.GET,
            "https://traffic.ls.hereapi.com/traffic/6.1/flow.json",
            expectedResponse,
            status=200,
        )
        response = self._api.additional_attributes(
            quadkey="0313131311102312213",
            attributes=[herepy.FlowProximityAdditionalAttributes.functional_class],
        )
        self.assertTrue(response)
        self.assertIsInstance(response, herepy.TrafficFlowResponse)
        self.assertIsNotNone(response.as_dict())

    @responses.activate
    def test_additional_attributes_fails(self):
        with codecs.open("testdata/models/unauthorized_error.json", mode="r", encoding="utf-8") as f:
            expectedResponse = f.read()
        responses.add(
            responses.GET,
            "https://traffic.ls.hereapi.com/traffic/6.1/flow.json",
            expectedResponse,
            status=200,
        )
        with self.assertRaises(herepy.UnauthorizedError):
            self._api.additional_attributes(
                quadkey="0313131311102312213",
                attributes=[herepy.FlowProximityAdditionalAttributes.functional_class],
            )
