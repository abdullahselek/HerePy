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

    def testInitiation(self):
        self.assertIsInstance(self._api, herepy.RoutingApi)
        self.assertEqual(self._api._app_id, 'app_id')
        self.assertEqual(self._api._app_code, 'app_code')
        self.assertEqual(self._api._baseUrl, 'https://route.cit.api.here.com/routing/7.2/calculateroute.json')

    @responses.activate
    def testCarRoute_whenSucceed(self):
        with codecs.open('testdata/models/routing.json', mode='r', encoding='utf-8') as f:
            expectedResponse = f.read()
        responses.add(responses.GET, 'https://route.cit.api.here.com/routing/7.2/calculateroute.json',
                  expectedResponse, status=200)
        response = self._api.CarRoute([11.0, 12.0], [22.0, 23.0], [herepy.RouteMode.car, herepy.RouteMode.fastest])
        self.assertTrue(response)
        self.assertIsInstance(response, herepy.RoutingResponse)

    @responses.activate
    def testCarRoute_whenErrorOccured(self):
        with open('testdata/models/routing_error.json', 'r') as f:
            expectedResponse = f.read()
        responses.add(responses.GET, 'https://route.cit.api.here.com/routing/7.2/calculateroute.json',
                  expectedResponse, status=200)
        response = self._api.CarRoute([11.0, 12.0], [22.0, 23.0], [herepy.RouteMode.pedestrian, herepy.RouteMode.fastest])
        self.assertIsInstance(response, herepy.HEREError)

    @responses.activate
    def testPedastrianRoute_whenSucceed(self):
        with codecs.open('testdata/models/routing.json', mode='r', encoding='utf-8') as f:
            expectedResponse = f.read()
        responses.add(responses.GET, 'https://route.cit.api.here.com/routing/7.2/calculateroute.json',
                  expectedResponse, status=200)
        response = self._api.PedastrianRoute([11.0, 12.0], [22.0, 23.0], [herepy.RouteMode.pedestrian, herepy.RouteMode.fastest])
        self.assertTrue(response)
        self.assertIsInstance(response, herepy.RoutingResponse)

    @responses.activate
    def testPedastrianRoute_whenErrorOccured(self):
        with open('testdata/models/routing_error.json', 'r') as f:
            expectedResponse = f.read()
        responses.add(responses.GET, 'https://route.cit.api.here.com/routing/7.2/calculateroute.json',
                  expectedResponse, status=200)
        response = self._api.PedastrianRoute([11.0, 12.0], [22.0, 23.0], [herepy.RouteMode.car, herepy.RouteMode.fastest])
        self.assertIsInstance(response, herepy.HEREError)

    @responses.activate
    def testIntermediateRoute_whenSucceed(self):
        with codecs.open('testdata/models/routing.json', mode='r', encoding='utf-8') as f:
            expectedResponse = f.read()
        responses.add(responses.GET, 'https://route.cit.api.here.com/routing/7.2/calculateroute.json',
                  expectedResponse, status=200)
        response = self._api.IntermediateRoute([11.0, 12.0], [15.0, 16.0], [22.0, 23.0], [herepy.RouteMode.car, herepy.RouteMode.fastest])
        self.assertTrue(response)
        self.assertIsInstance(response, herepy.RoutingResponse)

    @responses.activate
    def testIntermediateRoute_whenErrorOccured(self):
        with open('testdata/models/routing_error.json', 'r') as f:
            expectedResponse = f.read()
        responses.add(responses.GET, 'https://route.cit.api.here.com/routing/7.2/calculateroute.json',
                  expectedResponse, status=200)
        response = self._api.IntermediateRoute([11.0, 12.0], [15.0, 16.0], [22.0, 23.0], [herepy.RouteMode.car, herepy.RouteMode.fastest])
        self.assertIsInstance(response, herepy.HEREError)

    @responses.activate
    def testPublicTransport_whenSucceed(self):
        with codecs.open('testdata/models/routing.json', mode='r', encoding='utf-8') as f:
            expectedResponse = f.read()
        responses.add(responses.GET, 'https://route.cit.api.here.com/routing/7.2/calculateroute.json',
                  expectedResponse, status=200)
        response = self._api.PublicTransport([11.0, 12.0],
                                             [15.0, 16.0],
                                             [herepy.RouteMode.publicTransport, herepy.RouteMode.fastest],
                                             True)
        self.assertTrue(response)
        self.assertIsInstance(response, herepy.RoutingResponse)

    @responses.activate
    def testPublicTransport_whenErrorOccured(self):
        with open('testdata/models/routing_error.json', 'r') as f:
            expectedResponse = f.read()
        responses.add(responses.GET, 'https://route.cit.api.here.com/routing/7.2/calculateroute.json',
                  expectedResponse, status=200)
        response = self._api.PublicTransport([11.0, 12.0],
                                             [15.0, 16.0],
                                             [herepy.RouteMode.car, herepy.RouteMode.fastest],
                                             True)
        self.assertIsInstance(response, herepy.HEREError)
