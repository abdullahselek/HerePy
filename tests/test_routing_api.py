#!/usr/bin/env python

import os
import sys
import unittest
import responses
import codecs
import herepy

class RoutingApiTest(unittest.TestCase):

    def setUp(self):
        api = herepy.RoutingApi('app_id', 'app_code')
        self._api = api

    def test_initiation(self):
        self.assertIsInstance(self._api, herepy.RoutingApi)
        self.assertEqual(self._api._app_id, 'app_id')
        self.assertEqual(self._api._app_code, 'app_code')

    @responses.activate
    def test_bicycleroute_withdefaultmodes_whensucceed(self):
        with codecs.open('testdata/models/routing_bicycle.json', mode='r', encoding='utf-8') as f:
            expectedResponse = f.read()
        responses.add(responses.GET, 'https://route.cit.api.here.com/routing/7.2/calculateroute.json',
                  expectedResponse, status=200)
        response = self._api.bicycle_route([41.9798, -87.8801], [41.9043, -87.9216])
        self.assertTrue(response)
        self.assertIsInstance(response, herepy.RoutingResponse)

    @responses.activate
    def test_bicycleroute_route_short(self):
        with codecs.open('testdata/models/routing_bicycle.json', mode='r', encoding='utf-8') as f:
            expectedResponse = f.read()
        responses.add(responses.GET, 'https://route.cit.api.here.com/routing/7.2/calculateroute.json',
                  expectedResponse, status=200)
        response = self._api.bicycle_route([41.9798, -87.8801], [41.9043, -87.9216])
        expected_short_route = (
            "Mannheim Rd; W Belmont Ave; Cullerton St; N Landen Dr; "
            "E Fullerton Ave; N Wolf Rd; W North Ave; N Clinton Ave; "
            "E Third St; N Caroline Ave"
        )
        self.assertEqual(response.route_short, expected_short_route)

    @responses.activate
    def test_carroute_whensucceed(self):
        with codecs.open('testdata/models/routing.json', mode='r', encoding='utf-8') as f:
            expectedResponse = f.read()
        responses.add(responses.GET, 'https://route.cit.api.here.com/routing/7.2/calculateroute.json',
                  expectedResponse, status=200)
        response = self._api.car_route([11.0, 12.0], [22.0, 23.0], [herepy.RouteMode.car, herepy.RouteMode.fastest])
        self.assertTrue(response)
        self.assertIsInstance(response, herepy.RoutingResponse)

    @responses.activate
    def test_carroute_route_short(self):
        with codecs.open('testdata/models/routing_car_route_short.json', mode='r', encoding='utf-8') as f:
            expectedResponse = f.read()
        responses.add(responses.GET, 'https://route.cit.api.here.com/routing/7.2/calculateroute.json',
                  expectedResponse, status=200)
        response = self._api.car_route([38.9, -77.04833], [39.0, -77.1])
        expected_short_route = (
            "US-29 - K St NW; US-29 - Whitehurst Fwy; "
            "I-495 N - Capital Beltway; MD-187 S - Old Georgetown Rd"
        )
        self.assertEqual(response.route_short, expected_short_route)

    @responses.activate
    def test_carroute_withdefaultmodes_whensucceed(self):
        with codecs.open('testdata/models/routing.json', mode='r', encoding='utf-8') as f:
            expectedResponse = f.read()
        responses.add(responses.GET, 'https://route.cit.api.here.com/routing/7.2/calculateroute.json',
                  expectedResponse, status=200)
        response = self._api.car_route([11.0, 12.0], [22.0, 23.0])
        self.assertTrue(response)
        self.assertIsInstance(response, herepy.RoutingResponse)

    @responses.activate
    def test_carroute_when_error_invalid_input_data_occured(self):
        with open('testdata/models/routing_error_invalid_input_data.json', 'r') as f:
            expectedResponse = f.read()
        responses.add(responses.GET, 'https://route.cit.api.here.com/routing/7.2/calculateroute.json',
                  expectedResponse, status=200)
        with self.assertRaises(herepy.InvalidInputDataError):
            self._api.car_route([11.0, 12.0], [22.0, 23.0], [herepy.RouteMode.pedestrian, herepy.RouteMode.fastest])

    @responses.activate
    def test_carroute_when_error_invalid_credentials_occured(self):
        with open('testdata/models/routing_error_invalid_credentials.json', 'r') as f:
            expectedResponse = f.read()
        responses.add(responses.GET, 'https://route.cit.api.here.com/routing/7.2/calculateroute.json',
                  expectedResponse, status=200)
        api = herepy.RoutingApi('wrong_app_id', 'wrong_app_code')
        with self.assertRaises(herepy.InvalidCredentialsError):
            api.car_route([11.0, 12.0], [22.0, 23.0])

    @responses.activate
    def test_carroute_when_error_no_route_found_occured(self):
        with open('testdata/models/routing_error_no_route_found.json', 'r') as f:
            expectedResponse = f.read()
        responses.add(responses.GET, 'https://route.cit.api.here.com/routing/7.2/calculateroute.json',
                  expectedResponse, status=200)
        with self.assertRaises(herepy.NoRouteFoundError):
            self._api.car_route([11.0, 12.0], [47.013399, -10.171986])

    @responses.activate
    def test_pedastrianroute_whensucceed(self):
        with codecs.open('testdata/models/routing_pedestrian.json', mode='r', encoding='utf-8') as f:
            expectedResponse = f.read()
        responses.add(responses.GET, 'https://route.cit.api.here.com/routing/7.2/calculateroute.json',
                  expectedResponse, status=200)
        response = self._api.pedastrian_route([11.0, 12.0], [22.0, 23.0], [herepy.RouteMode.pedestrian, herepy.RouteMode.fastest])
        self.assertTrue(response)
        self.assertIsInstance(response, herepy.RoutingResponse)

    @responses.activate
    def test_pedastrianroute_withdefaultmodes_whensucceed(self):
        with codecs.open('testdata/models/routing_pedestrian.json', mode='r', encoding='utf-8') as f:
            expectedResponse = f.read()
        responses.add(responses.GET, 'https://route.cit.api.here.com/routing/7.2/calculateroute.json',
                  expectedResponse, status=200)
        response = self._api.pedastrian_route([11.0, 12.0], [22.0, 23.0])
        self.assertTrue(response)
        self.assertIsInstance(response, herepy.RoutingResponse)

    @responses.activate
    def test_pedastrianroute_when_error_invalid_input_data_occured(self):
        with open('testdata/models/routing_error_invalid_input_data.json', 'r') as f:
            expectedResponse = f.read()
        responses.add(responses.GET, 'https://route.cit.api.here.com/routing/7.2/calculateroute.json',
                  expectedResponse, status=200)
        with self.assertRaises(herepy.InvalidInputDataError):
            self._api.pedastrian_route([11.0, 12.0], [22.0, 23.0], [herepy.RouteMode.car, herepy.RouteMode.fastest])

    @responses.activate
    def test_pedastrianroute_when_error_invalid_credentials_occured(self):
        with open('testdata/models/routing_error_invalid_credentials.json', 'r') as f:
            expectedResponse = f.read()
        responses.add(responses.GET, 'https://route.cit.api.here.com/routing/7.2/calculateroute.json',
                  expectedResponse, status=200)
        api = herepy.RoutingApi('wrong_app_id', 'wrong_app_code')
        with self.assertRaises(herepy.InvalidCredentialsError):
            api.pedastrian_route([11.0, 12.0], [22.0, 23.0])

    @responses.activate
    def test_pedastrianroute_when_error_no_route_found_occured(self):
        with open('testdata/models/routing_error_no_route_found.json', 'r') as f:
            expectedResponse = f.read()
        responses.add(responses.GET, 'https://route.cit.api.here.com/routing/7.2/calculateroute.json',
                  expectedResponse, status=200)
        with self.assertRaises(herepy.NoRouteFoundError):
            self._api.pedastrian_route([11.0, 12.0], [47.013399, -10.171986])

    @responses.activate
    def test_pedastrianroute_route_short(self):
        with codecs.open('testdata/models/routing_pedestrian.json', mode='r', encoding='utf-8') as f:
            expectedResponse = f.read()
        responses.add(responses.GET, 'https://route.cit.api.here.com/routing/7.2/calculateroute.json',
                  expectedResponse, status=200)
        response = self._api.pedastrian_route([11.0, 12.0], [22.0, 23.0], [herepy.RouteMode.pedestrian, herepy.RouteMode.fastest])
        expected_short_route = (
            "Mannheim Rd; W Belmont Ave; Cullerton St; E Fullerton Ave; "
            "La Porte Ave; E Palmer Ave; N Railroad Ave; W North Ave; "
            "E North Ave; E Third St"
        )
        self.assertEqual(response.route_short, expected_short_route)

    @responses.activate
    def test_intermediateroute_whensucceed(self):
        with codecs.open('testdata/models/routing.json', mode='r', encoding='utf-8') as f:
            expectedResponse = f.read()
        responses.add(responses.GET, 'https://route.cit.api.here.com/routing/7.2/calculateroute.json',
                  expectedResponse, status=200)
        response = self._api.intermediate_route([11.0, 12.0], [15.0, 16.0], [22.0, 23.0], [herepy.RouteMode.car, herepy.RouteMode.fastest])
        self.assertTrue(response)
        self.assertIsInstance(response, herepy.RoutingResponse)

    @responses.activate
    def test_intermediateroute_withdefaultmodes_whensucceed(self):
        with codecs.open('testdata/models/routing.json', mode='r', encoding='utf-8') as f:
            expectedResponse = f.read()
        responses.add(responses.GET, 'https://route.cit.api.here.com/routing/7.2/calculateroute.json',
                  expectedResponse, status=200)
        response = self._api.intermediate_route([11.0, 12.0], [15.0, 16.0], [22.0, 23.0])
        self.assertTrue(response)
        self.assertIsInstance(response, herepy.RoutingResponse)

    @responses.activate
    def test_intermediateroute_when_error_invalid_input_data_occured(self):
        with open('testdata/models/routing_error_invalid_input_data.json', 'r') as f:
            expectedResponse = f.read()
        responses.add(responses.GET, 'https://route.cit.api.here.com/routing/7.2/calculateroute.json',
                  expectedResponse, status=200)
        with self.assertRaises(herepy.InvalidInputDataError):
            self._api.intermediate_route([11.0, 12.0], [15.0, 16.0], [22.0, 23.0], [herepy.RouteMode.car, herepy.RouteMode.fastest])

    @responses.activate
    def test_intermediateroute_when_error_invalid_credentials_occured(self):
        with open('testdata/models/routing_error_invalid_credentials.json', 'r') as f:
            expectedResponse = f.read()
        responses.add(responses.GET, 'https://route.cit.api.here.com/routing/7.2/calculateroute.json',
                  expectedResponse, status=200)
        api = herepy.RoutingApi('wrong_app_id', 'wrong_app_code')
        with self.assertRaises(herepy.InvalidCredentialsError):
            api.intermediate_route([11.0, 12.0], [15.0, 16.0], [22.0, 23.0])

    @responses.activate
    def test_intermediateroute_when_error_no_route_found_occured(self):
        with open('testdata/models/routing_error_no_route_found.json', 'r') as f:
            expectedResponse = f.read()
        responses.add(responses.GET, 'https://route.cit.api.here.com/routing/7.2/calculateroute.json',
                  expectedResponse, status=200)
        with self.assertRaises(herepy.NoRouteFoundError):
            self._api.intermediate_route([11.0, 12.0], [47.013399, -10.171986], [22.0, 23.0])

    @responses.activate
    def test_publictransport_whensucceed(self):
        with codecs.open('testdata/models/routing_public.json', mode='r', encoding='utf-8') as f:
            expectedResponse = f.read()
        responses.add(responses.GET, 'https://route.cit.api.here.com/routing/7.2/calculateroute.json',
                  expectedResponse, status=200)
        response = self._api.public_transport([11.0, 12.0],
                                              [15.0, 16.0],
                                              True,
                                              [herepy.RouteMode.publicTransport, herepy.RouteMode.fastest])
        self.assertTrue(response)
        self.assertIsInstance(response, herepy.RoutingResponse)

    @responses.activate
    def test_publictransport_route_short(self):
        with codecs.open('testdata/models/routing_public.json', mode='r', encoding='utf-8') as f:
            expectedResponse = f.read()
        responses.add(responses.GET, 'https://route.cit.api.here.com/routing/7.2/calculateroute.json',
                  expectedResponse, status=200)
        response = self._api.public_transport([11.0, 12.0],
                                              [15.0, 16.0],
                                              True)
        expected_short_route = (
            "332 - Palmer/Schiller; 332 - Cargo Rd./Delta Cargo; " "332 - Palmer/Schiller"
        )
        self.assertEqual(response.route_short, expected_short_route)

    @responses.activate
    def test_publictransport_withdefaultmodes_whensucceed(self):
        with codecs.open('testdata/models/routing_public.json', mode='r', encoding='utf-8') as f:
            expectedResponse = f.read()
        responses.add(responses.GET, 'https://route.cit.api.here.com/routing/7.2/calculateroute.json',
                  expectedResponse, status=200)
        response = self._api.public_transport([11.0, 12.0],
                                              [15.0, 16.0],
                                              True)
        self.assertTrue(response)
        self.assertIsInstance(response, herepy.RoutingResponse)

    @responses.activate
    def test_publictransport_when_error_invalid_input_data_occured(self):
        with open('testdata/models/routing_error_invalid_input_data.json', 'r') as f:
            expectedResponse = f.read()
        responses.add(responses.GET, 'https://route.cit.api.here.com/routing/7.2/calculateroute.json',
                  expectedResponse, status=200)
        with self.assertRaises(herepy.InvalidInputDataError):
            self._api.public_transport([11.0, 12.0],
                                       [15.0, 16.0],
                                       True,
                                       [herepy.RouteMode.car, herepy.RouteMode.fastest])

    @responses.activate
    def test_publictransport_when_error_invalid_credentials_occured(self):
        with open('testdata/models/routing_error_invalid_credentials.json', 'r') as f:
            expectedResponse = f.read()
        responses.add(responses.GET, 'https://route.cit.api.here.com/routing/7.2/calculateroute.json',
                  expectedResponse, status=200)
        api = herepy.RoutingApi('wrong_app_id', 'wrong_app_code')
        with self.assertRaises(herepy.InvalidCredentialsError):
            api.public_transport([11.0, 12.0],
                                 [15.0, 16.0],
                                 True)

    @responses.activate
    def test_publictransport_when_error_no_route_found_occured(self):
        with open('testdata/models/routing_error_no_route_found.json', 'r') as f:
            expectedResponse = f.read()
        responses.add(responses.GET, 'https://route.cit.api.here.com/routing/7.2/calculateroute.json',
                  expectedResponse, status=200)
        with self.assertRaises(herepy.NoRouteFoundError):
            self._api.public_transport([11.0, 12.0], [47.013399, -10.171986], True)

    @responses.activate
    def test_publictransporttimetable_withdefaultmodes_whensucceed(self):
        with codecs.open('testdata/models/routing_public_time_table.json', mode='r', encoding='utf-8') as f:
            expectedResponse = f.read()
        responses.add(responses.GET, 'https://route.cit.api.here.com/routing/7.2/calculateroute.json',
                  expectedResponse, status=200)
        response = self._api.public_transport_timetable([11.0, 12.0],
                                              [15.0, 16.0],
                                              True)
        self.assertTrue(response)
        self.assertIsInstance(response, herepy.RoutingResponse)

    @responses.activate
    def test_publictransporttimetable_route_short(self):
        with codecs.open('testdata/models/routing_public_time_table.json', mode='r', encoding='utf-8') as f:
            expectedResponse = f.read()
        responses.add(responses.GET, 'https://route.cit.api.here.com/routing/7.2/calculateroute.json',
                  expectedResponse, status=200)
        response = self._api.public_transport_timetable([11.0, 12.0],
                                              [15.0, 16.0],
                                              True)
        expected_short_route = (
            "330 - Archer/Harlem (Terminal); 309 - Elmhurst Metra Station"
        )
        self.assertEqual(response.route_short, expected_short_route)

    @responses.activate
    def test_locationnearmotorway_whensucceed(self):
        with codecs.open('testdata/models/routing.json', mode='r', encoding='utf-8') as f:
            expectedResponse = f.read()
        responses.add(responses.GET, 'https://route.cit.api.here.com/routing/7.2/calculateroute.json',
                  expectedResponse, status=200)
        response = self._api.location_near_motorway([11.0, 12.0],
                                                    [22.0, 23.0],
                                                    [herepy.RouteMode.car, herepy.RouteMode.fastest])
        self.assertTrue(response)
        self.assertIsInstance(response, herepy.RoutingResponse)

    @responses.activate
    def test_locationnearmotorway_withdefaultmodes_whensucceed(self):
        with codecs.open('testdata/models/routing.json', mode='r', encoding='utf-8') as f:
            expectedResponse = f.read()
        responses.add(responses.GET, 'https://route.cit.api.here.com/routing/7.2/calculateroute.json',
                  expectedResponse, status=200)
        response = self._api.location_near_motorway([11.0, 12.0],
                                                    [22.0, 23.0])
        self.assertTrue(response)
        self.assertIsInstance(response, herepy.RoutingResponse)

    @responses.activate
    def test_locationnearmotorway_when_error_invalid_input_data_occured(self):
        with open('testdata/models/routing_error_invalid_input_data.json', 'r') as f:
            expectedResponse = f.read()
        responses.add(responses.GET, 'https://route.cit.api.here.com/routing/7.2/calculateroute.json',
                  expectedResponse, status=200)
        with self.assertRaises(herepy.InvalidInputDataError):
            self._api.location_near_motorway([11.0, 12.0],
                                             [22.0, 23.0],
                                             [herepy.RouteMode.pedestrian, herepy.RouteMode.fastest])

    @responses.activate
    def test_locationnearmotorway_when_error_invalid_credentials_occured(self):
        with open('testdata/models/routing_error_invalid_credentials.json', 'r') as f:
            expectedResponse = f.read()
        responses.add(responses.GET, 'https://route.cit.api.here.com/routing/7.2/calculateroute.json',
                  expectedResponse, status=200)
        api = herepy.RoutingApi('wrong_app_id', 'wrong_app_code')
        with self.assertRaises(herepy.InvalidCredentialsError):
            api.location_near_motorway([11.0, 12.0], [22.0, 23.0])

    @responses.activate
    def test_locationnearmotorway_when_error_no_route_found_occured(self):
        with open('testdata/models/routing_error_no_route_found.json', 'r') as f:
            expectedResponse = f.read()
        responses.add(responses.GET, 'https://route.cit.api.here.com/routing/7.2/calculateroute.json',
                  expectedResponse, status=200)
        with self.assertRaises(herepy.NoRouteFoundError):
            self._api.location_near_motorway([11.0, 12.0], [47.013399, -10.171986])

    @responses.activate
    def test_truckroute_whensucceed(self):
        with codecs.open('testdata/models/routing.json', mode='r', encoding='utf-8') as f:
            expectedResponse = f.read()
        responses.add(responses.GET, 'https://route.cit.api.here.com/routing/7.2/calculateroute.json',
                  expectedResponse, status=200)
        response = self._api.truck_route([11.0, 12.0],
                                         [22.0, 23.0],
                                         [herepy.RouteMode.truck, herepy.RouteMode.fastest])
        self.assertTrue(response)
        self.assertIsInstance(response, herepy.RoutingResponse)

    @responses.activate
    def test_truckroute_route_short(self):
        with codecs.open('testdata/models/routing_truck_route_short.json', mode='r', encoding='utf-8') as f:
            expectedResponse = f.read()
        responses.add(responses.GET, 'https://route.cit.api.here.com/routing/7.2/calculateroute.json',
                  expectedResponse, status=200)
        response = self._api.truck_route([11.0, 12.0],
                                         [22.0, 23.0])
        expected_short_route = (
            "I-190; I-294 S - Tri-State Tollway; I-290 W - Eisenhower Expy W; "
            "IL-64 W - E North Ave; I-290 E - Eisenhower Expy E; I-290"
        )
        self.assertEqual(response.route_short, expected_short_route)

    @responses.activate
    def test_truckroute_withdefaultmodes_whensucceed(self):
        with codecs.open('testdata/models/routing.json', mode='r', encoding='utf-8') as f:
            expectedResponse = f.read()
        responses.add(responses.GET, 'https://route.cit.api.here.com/routing/7.2/calculateroute.json',
                  expectedResponse, status=200)
        response = self._api.truck_route([11.0, 12.0],
                                         [22.0, 23.0])
        self.assertTrue(response)
        self.assertIsInstance(response, herepy.RoutingResponse)

    @responses.activate
    def test_truckroute_when_error_invalid_input_data_occured(self):
        with open('testdata/models/routing_error_invalid_input_data.json', 'r') as f:
            expectedResponse = f.read()
        responses.add(responses.GET, 'https://route.cit.api.here.com/routing/7.2/calculateroute.json',
                  expectedResponse, status=200)
        with self.assertRaises(herepy.InvalidInputDataError):
            self._api.truck_route([11.0, 12.0],
                                  [22.0, 23.0],
                                  [herepy.RouteMode.pedestrian, herepy.RouteMode.fastest])

    @responses.activate
    def test_truckroute_when_error_invalid_credentials_occured(self):
        with open('testdata/models/routing_error_invalid_credentials.json', 'r') as f:
            expectedResponse = f.read()
        responses.add(responses.GET, 'https://route.cit.api.here.com/routing/7.2/calculateroute.json',
                  expectedResponse, status=200)
        api = herepy.RoutingApi('wrong_app_id', 'wrong_app_code')
        with self.assertRaises(herepy.InvalidCredentialsError):
            api.truck_route([11.0, 12.0], [22.0, 23.0])

    @responses.activate
    def test_truckroute_when_error_no_route_found_occured(self):
        with open('testdata/models/routing_error_no_route_found.json', 'r') as f:
            expectedResponse = f.read()
        responses.add(responses.GET, 'https://route.cit.api.here.com/routing/7.2/calculateroute.json',
                  expectedResponse, status=200)
        with self.assertRaises(herepy.NoRouteFoundError):
            self._api.truck_route([11.0, 12.0], [47.013399, -10.171986])

    @responses.activate
    def test_matrix_whensucceed(self):
        with codecs.open('testdata/models/routing_matrix.json', mode='r', encoding='utf-8') as f:
            server_response = f.read()
        responses.add(responses.GET, 'https://matrix.route.api.here.com/routing/7.2/calculatematrix.json',
                      server_response, status=200)
        response = self._api.matrix(
            start_waypoints=[[9.933231, -84.076831]],
            destination_waypoints=[[9.934574, -84.065544]])
        self.assertTrue(response)
        self.assertIsInstance(response, herepy.RoutingMatrixResponse)

    @responses.activate
    def test_matrix_multiple_starts(self):
        with codecs.open('testdata/models/routing_matrix_multiple_starts.json', mode='r', encoding='utf-8') as f:
            server_response = f.read()
        responses.add(responses.GET, 'https://matrix.route.api.here.com/routing/7.2/calculatematrix.json',
                      server_response, status=200)
        response = self._api.matrix(
            start_waypoints=[[9.933231, -84.076831], [9.934574, -84.065544]],
            destination_waypoints=[[9.934574, -84.065544]])
        self.assertTrue(response)
        self.assertIsInstance(response, herepy.RoutingMatrixResponse)

    @responses.activate
    def test_matrix_multiple_destinations(self):
        with codecs.open('testdata/models/routing_matrix_multiple_destinations.json', mode='r', encoding='utf-8') as f:
            server_response = f.read()
        responses.add(responses.GET, 'https://matrix.route.api.here.com/routing/7.2/calculatematrix.json',
                      server_response, status=200)
        response = self._api.matrix(
            start_waypoints=[[9.933231, -84.076831]],
            destination_waypoints=[[9.934574, -84.065544], [9.612552, -84.62892]])
        self.assertTrue(response)
        self.assertIsInstance(response, herepy.RoutingMatrixResponse)

    @responses.activate
    def test_matrix_bad_request(self):
        with codecs.open('testdata/models/routing_matrix_bad_request.json', mode='r', encoding='utf-8') as f:
            server_response = f.read()
        responses.add(responses.GET, 'https://matrix.route.api.here.com/routing/7.2/calculatematrix.json',
                      server_response, status=400)
        with self.assertRaises(herepy.InvalidInputDataError):
            self._api.matrix(
                start_waypoints=[[9.933231, -84.076831]],
                destination_waypoints=[[9.934574, -84.065544]],
                modes=[herepy.RouteMode.pedestrian, herepy.RouteMode.car])
