#!/usr/bin/env python

import os
import time
import unittest
import json
import responses
import herepy


class DestinationPickupParamTest(unittest.TestCase):

    def test_valueofparam(self):
        pickup_param = herepy.DestinationPickupParam(
                           latitude=50.11562, longitude=8.63121,
                           param_type=herepy.MultiplePickupOfferType.pickup, item='GRAPEFRUITS',
                           value=1000)
        param_str = pickup_param.__str__()
        self.assertEqual(param_str, '50.11562,8.63121;pickup:GRAPEFRUITS,value:1000')

        pickup_param = herepy.DestinationPickupParam(
                           latitude=50.11562, longitude=8.63121,
                           param_type=herepy.MultiplePickupOfferType.drop, item='APPLES')
        param_str = pickup_param.__str__()
        self.assertEqual(param_str, '50.11562,8.63121;drop:APPLES')


class FleetTelematicsApiTest(unittest.TestCase):

    def setUp(self):
        api = herepy.FleetTelematicsApi('api_key')
        self._api = api


    def test_initiation(self):
        self.assertIsInstance(self._api, herepy.FleetTelematicsApi)
        self.assertEqual(self._api._api_key, 'api_key')
        self.assertEqual(self._api._base_url, 'https://wse.ls.hereapi.com/2/')


    def test_destination_param(self):
        destination_param = herepy.DestinationParam(text='FranfurtCentralStation',
                                                    latitude=50.1073,
                                                    longitude=8.6647)
        param_str = destination_param.__str__()
        self.assertEqual(param_str, 'FranfurtCentralStation;50.1073,8.6647')


    @responses.activate
    def test_find_sequence_whensucceed(self):
        with open('testdata/models/fleet_telematics_find_sequence.json', 'r') as f:
            expected_response = f.read()
        responses.add(responses.GET, 'https://wse.ls.hereapi.com/2/findsequence.json',
                  expected_response, status=200)
        start = herepy.DestinationParam(text='WiesbadenCentralStation',
                                        latitude=50.0715,
                                        longitude=8.2434)
        intermediate_destinations = [herepy.DestinationParam(text='FranfurtCentralStation',
                                                             latitude=50.1073,
                                                             longitude=8.6647)]
        intermediate_destinations.append(herepy.DestinationParam(text='DarmstadtCentralStation',
                                                                 latitude=49.8728,
                                                                 longitude=8.6326))
        intermediate_destinations.append(herepy.DestinationParam(text='FrankfurtAirport',
                                                                 latitude=50.0505,
                                                                 longitude=8.5698))
        end = herepy.DestinationParam(text='MainzCentralStation',
                                      latitude=50.0021,
                                      longitude=8.259)
        modes = [herepy.RouteMode.fastest, herepy.RouteMode.car, herepy.RouteMode.traffic_enabled]
        response = self._api.find_sequence(start=start,
                                           intermediate_destinations=intermediate_destinations,
                                           end=end,
                                           modes=modes)
        self.assertTrue(response)
        self.assertIsInstance(response, herepy.WaypointSequenceResponse)


    @responses.activate
    def test_find_sequence_whenerroroccured(self):
        with open('testdata/models/fleet_telematics_unauthorized_error.json', 'r') as f:
            expected_response = f.read()
        responses.add(responses.GET, 'https://wse.ls.hereapi.com/2/findsequence.json',
                  expected_response, status=200)

        start = herepy.DestinationParam(text='WiesbadenCentralStation',
                                         latitude=50.0715,
                                         longitude=8.2434)
        intermediate_destinations = [herepy.DestinationParam(text='FranfurtCentralStation',
                                                             latitude=50.1073,
                                                             longitude=8.6647)]
        end = herepy.DestinationParam(text='MainzCentralStation',
                                      latitude=50.0021,
                                      longitude=8.259)
        modes = [herepy.RouteMode.fastest, herepy.RouteMode.car, herepy.RouteMode.traffic_enabled]

        with self.assertRaises(herepy.HEREError):
            self._api.find_sequence(start=start,
                                    intermediate_destinations=intermediate_destinations,
                                    end=end,
                                    modes=modes)


    @responses.activate
    def test_find_pickups_whensucceed(self):
        with open('testdata/models/fleet_telematics_find_pickups.json', 'r') as f:
            expected_response = f.read()
        responses.add(responses.GET, 'https://wse.ls.hereapi.com/2/findpickups.json',
                  expected_response, status=200)

        modes = [herepy.RouteMode.fastest, herepy.RouteMode.car, herepy.RouteMode.traffic_enabled]
        start = herepy.DestinationPickupParam(latitude=50.115620,
                    longitude=8.631210,
                    param_type=herepy.MultiplePickupOfferType.pickup,
                    item='GRAPEFRUITS',
                    value=1000)
        departure = '2016-10-14T07:30:00+02:00'
        capacity = 10000
        vehicle_cost = 0.29
        driver_cost = 20
        max_detour = 60
        rest_times = 'disabled'
        intermediate_destinations = [herepy.DestinationPickupParam(
            latitude=50.118578,
            longitude=8.636551,
            param_type=herepy.MultiplePickupOfferType.drop,
            item='APPLES',
            value=30
        ), herepy.DestinationPickupParam(
            latitude=50.122540,
            longitude=8.631070,
            param_type=herepy.MultiplePickupOfferType.pickup,
            item='BANANAS')
        ]
        end = herepy.DestinationParam(
            text=None,
            latitude=50.132540,
            longitude=8.649280
        )
        response = self._api.find_pickups(modes=modes,
                        start=start,
                        departure=departure,
                        capacity=capacity,
                        vehicle_cost=vehicle_cost,
                        driver_cost=driver_cost,
                        max_detour=max_detour,
                        rest_times=rest_times,
                        intermediate_destinations=intermediate_destinations,
                        end=end)
        self.assertTrue(response)
        self.assertIsInstance(response, herepy.WaypointSequenceResponse)
