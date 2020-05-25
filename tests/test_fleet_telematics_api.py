#!/usr/bin/env python

import os
import time
import unittest
import json
import responses
import herepy


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


    def test_create_find_sequence_parameters(self):
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
        data = self._api.create_find_sequence_parameters(start=start,
                                                         intermediate_destinations=intermediate_destinations,
                                                         end=end,
                                                         modes=modes)
        self.assertEqual(data, {'apiKey': 'api_key',
                                'start': 'WiesbadenCentralStation;50.0715,8.2434',
                                'destination1': 'FranfurtCentralStation;50.1073,8.6647',
                                'destination2': 'DarmstadtCentralStation;49.8728,8.6326',
                                'destination3': 'FrankfurtAirport;50.0505,8.5698',
                                'end': 'MainzCentralStation;50.0021,8.259',
                                'improveFor': 'time',
                                'departure': 'now',
                                'mode' : 'fastest;car;traffic:enabled;'})
