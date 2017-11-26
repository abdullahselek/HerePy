#!/usr/bin/env python

import os
import sys
import io
import unittest
import responses
import codecs
import herepy

class PublicTransitApiTest(unittest.TestCase):

    def setUp(self):
        api = herepy.PublicTransitApi('app_id', 'app_code')
        self._api = api

    def test_initiation(self):
        self.assertIsInstance(self._api, herepy.PublicTransitApi)
        self.assertEqual(self._api._app_id, 'app_id')
        self.assertEqual(self._api._app_code, 'app_code')
        self.assertEqual(self._api._base_url, 'https://cit.transit.api.here.com/v3/')

    @responses.activate
    def test_find_stations_by_name_whensucceed(self):
        with open('testdata/models/public_transit_api.json', 'r') as f:
            expectedResponse = f.read()
        responses.add(responses.GET, 'https://cit.transit.api.here.com/v3/stations/by_name.json',
                  expectedResponse, status=200)
        response = self._api.find_stations_by_name([40.7505, -73.9910],
                                                   'union',
                                                   10,
                                                   herepy.PublicTransitSearchMethod.fuzzy,
                                                   5000)
        self.assertTrue(response)
        self.assertIsInstance(response, herepy.PublicTransitResponse)

    @responses.activate
    def test_find_stations_by_name_whenerroroccured(self):
        with open('testdata/models/public_transit_api_error.json', 'r') as f:
            expectedResponse = f.read()
        responses.add(responses.GET, 'https://cit.transit.api.here.com/v3/stations/by_name.json',
                  expectedResponse, status=200)
        response = self._api.find_stations_by_name([40.7505, -73.9910],
                                                   '')
        self.assertIsInstance(response, herepy.HEREError)

    @responses.activate
    def test_find_stations_nearby_whensucceed(self):
        with io.open('testdata/models/public_transit_api_nearby.json', 'r', encoding='utf-8') as f:
            expectedResponse = f.read()
        responses.add(responses.GET, 'https://cit.transit.api.here.com/v3/stations/by_geocoord.json',
                  expectedResponse, status=200)
        response = self._api.find_stations_nearby([55.7541, 37.6200], 350, 3)
        self.assertTrue(response)
        self.assertIsInstance(response, herepy.PublicTransitResponse)

    @responses.activate
    def test_find_stations_nearby_whenerroroccured(self):
        with open('testdata/models/public_transit_api_error.json', 'r') as f:
            expectedResponse = f.read()
        responses.add(responses.GET, 'https://cit.transit.api.here.com/v3/stations/by_geocoord.json',
                  expectedResponse, status=200)
        response = self._api.find_stations_nearby([-9999, -9999])
        self.assertIsInstance(response, herepy.HEREError)

    @responses.activate
    def test_find_stations_by_id_whensucceed(self):
        with io.open('testdata/models/public_transit_api_by_id.json', 'r', encoding='utf-8') as f:
            expectedResponse = f.read()
        responses.add(responses.GET, 'https://cit.transit.api.here.com/v3/stations/by_ids.json',
                  expectedResponse, status=200)
        response = self._api.find_stations_by_id([720390022, 720390000], 'en')
        self.assertTrue(response)
        self.assertIsInstance(response, herepy.PublicTransitResponse)

    @responses.activate
    def test_find_stations_by_id_whenerroroccured(self):
        with open('testdata/models/public_transit_api_error.json', 'r') as f:
            expectedResponse = f.read()
        responses.add(responses.GET, 'https://cit.transit.api.here.com/v3/stations/by_ids.json',
                  expectedResponse, status=200)
        response = self._api.find_stations_by_id([-99999], 'tr')
        self.assertIsInstance(response, herepy.HEREError)

    @responses.activate
    def test_find_transit_coverage_in_cities_whensucceed(self):
        with io.open('testdata/models/public_transit_api_coverage_cities.json', 'r', encoding='utf-8') as f:
            expectedResponse = f.read()
        responses.add(responses.GET, 'https://cit.transit.api.here.com/v3/coverage/city.json',
                  expectedResponse, status=200)
        response = self._api.find_transit_coverage_in_cities([42.3580, -71.0636], 'USA', 50000)
        self.assertTrue(response)
        self.assertIsInstance(response, herepy.PublicTransitResponse)

    @responses.activate
    def test_find_transit_coverage_in_cities_whenerroroccured(self):
        with open('testdata/models/public_transit_api_error.json', 'r') as f:
            expectedResponse = f.read()
        responses.add(responses.GET, 'https://cit.transit.api.here.com/v3/coverage/city.json',
                  expectedResponse, status=200)
        response = self._api.find_transit_coverage_in_cities([-9999, -9999], '', 100)
        self.assertIsInstance(response, herepy.HEREError)

    @responses.activate
    def test_next_nearby_departures_of_station_whensucceed(self):
        with io.open('testdata/models/public_transit_api_next_nearby_departures.json', 'r', encoding='utf-8') as f:
            expectedResponse = f.read()
        responses.add(responses.GET, 'https://cit.transit.api.here.com/v3/board.json',
                  expectedResponse, status=200)
        response = self._api.next_nearby_departures_of_station(402000653, '2017-11-21T11:10:00')
        self.assertTrue(response)
        self.assertIsInstance(response, herepy.PublicTransitResponse)

    @responses.activate
    def test_next_nearby_departures_of_station_whenerroroccured(self):
        with open('testdata/models/public_transit_api_error.json', 'r') as f:
            expectedResponse = f.read()
        responses.add(responses.GET, 'https://cit.transit.api.here.com/v3/board.json',
                  expectedResponse, status=200)
        response = self._api.next_nearby_departures_of_station(-1, '')
        self.assertIsInstance(response, herepy.HEREError)

    @responses.activate
    def test_next_departures_from_location_whensucceed(self):
        with io.open('testdata/models/public_transit_api_next_departures_location.json', 'r', encoding='utf-8') as f:
            expectedResponse = f.read()
        responses.add(responses.GET, 'https://cit.transit.api.here.com/v3/multiboard/by_geocoord.json',
                  expectedResponse, status=200)
        response = self._api.next_departures_from_location([51.4477, -0.1669], '2017-11-21T07:30:00')
        self.assertTrue(response)
        self.assertIsInstance(response, herepy.PublicTransitResponse)

    @responses.activate
    def test_next_departures_from_location_whenerroroccured(self):
        with open('testdata/models/public_transit_api_error.json', 'r') as f:
            expectedResponse = f.read()
        responses.add(responses.GET, 'https://cit.transit.api.here.com/v3/multiboard/by_geocoord.json',
                  expectedResponse, status=200)
        response = self._api.next_departures_from_location([-9999, -9999], '')
        self.assertIsInstance(response, herepy.HEREError)

    @responses.activate
    def test_next_departures_for_stations_whensucceed(self):
        with io.open('testdata/models/public_transit_api_next_departures_for_stations.json', 'r', encoding='utf-8') as f:
            expectedResponse = f.read()
        responses.add(responses.GET, 'https://cit.transit.api.here.com/v3/multiboard/by_stn_ids.json',
                  expectedResponse, status=200)
        response = self._api.next_departures_for_stations([402000656, 402000653, 402061786], '2017-11-22T07:30:00')
        self.assertTrue(response)
        self.assertIsInstance(response, herepy.PublicTransitResponse)

    @responses.activate
    def test_next_departures_for_stations_whenerroroccured(self):
        with open('testdata/models/public_transit_api_error.json', 'r') as f:
            expectedResponse = f.read()
        responses.add(responses.GET, 'https://cit.transit.api.here.com/v3/multiboard/by_stn_ids.json',
                  expectedResponse, status=200)
        response = self._api.next_departures_for_stations([-99999, -99999, -99999], '')
        self.assertIsInstance(response, herepy.HEREError)

    @responses.activate
    def test_calculate_route_whensucceed(self):
        with io.open('testdata/models/public_transit_calculate_route.json', 'r', encoding='utf-8') as f:
            expectedResponse = f.read()
        responses.add(responses.GET, 'https://cit.transit.api.here.com/v3/route.json',
                  expectedResponse, status=200)
        response = self._api.calculate_route([41.9773, -87.9019], [41.8961, -87.6552], '2017-11-22T07:30:00', herepy.PublicTransitRoutingType.time_tabled)
        self.assertTrue(response)
        self.assertIsInstance(response, herepy.PublicTransitResponse)

    @responses.activate
    def test_calculate_route_whenerroroccured(self):
        with open('testdata/models/public_transit_api_error.json', 'r') as f:
            expectedResponse = f.read()
        responses.add(responses.GET, 'https://cit.transit.api.here.com/v3/route.json',
                  expectedResponse, status=200)
        response = self._api.calculate_route([-9999, -9999], [-9999, -9999], '2017-11-22T07:30:00', herepy.PublicTransitRoutingType.time_tabled)
        self.assertIsInstance(response, herepy.HEREError)

    @responses.activate
    def test_calculate_route_time_whensucceed(self):
        with io.open('testdata/models/public_transit_api_calculate_route_time.json', 'r', encoding='utf-8') as f:
            expectedResponse = f.read()
        responses.add(responses.GET, 'https://cit.transit.api.here.com/v3/route.json',
                  expectedResponse, status=200)
        response = self._api.calculate_route_time([41.9773, -87.9019],
                                                  [41.8961, -87.6552],
                                                  '2017-11-22T07:30:00',
                                                  1,
                                                  herepy.PublicTransitRoutingType.time_tabled)
        self.assertTrue(response)
        self.assertIsInstance(response, herepy.PublicTransitResponse)

    @responses.activate
    def test_calculate_route_time_whenerroroccured(self):
        with open('testdata/models/public_transit_api_error.json', 'r') as f:
            expectedResponse = f.read()
        responses.add(responses.GET, 'https://cit.transit.api.here.com/v3/route.json',
                  expectedResponse, status=200)
        response = self._api.calculate_route_time([-9999, -9999],
                                                  [-9999, -9999],
                                                  '2017-11-22T07:30:00',
                                                  1,
                                                  herepy.PublicTransitRoutingType.time_tabled)
        self.assertIsInstance(response, herepy.HEREError)

    @responses.activate
    def test_transit_route_shows_line_graph_whensucceed(self):
        with io.open('testdata/models/public_transit_api_calculate_route_time.json', 'r', encoding='utf-8') as f:
            expectedResponse = f.read()
        responses.add(responses.GET, 'https://cit.transit.api.here.com/v3/route.json',
                  expectedResponse, status=200)
        response = self._api.transit_route_shows_line_graph([41.9773, -87.9019],
                                                            [41.8961, -87.6552],
                                                            '2017-11-22T07:30:00',)
        self.assertTrue(response)
        self.assertIsInstance(response, herepy.PublicTransitResponse)

    @responses.activate
    def test_transit_route_shows_line_graph_whenerroroccured(self):
        with open('testdata/models/public_transit_api_error.json', 'r') as f:
            expectedResponse = f.read()
        responses.add(responses.GET, 'https://cit.transit.api.here.com/v3/route.json',
                  expectedResponse, status=200)
        response = self._api.transit_route_shows_line_graph([-9999, -9999],
                                                            [-9999, -9999],
                                                            '2017-11-22T07:30:00')
        self.assertIsInstance(response, herepy.HEREError)

    @responses.activate
    def test_coverage_witin_a_city_whensucceed(self):
        with io.open('testdata/models/public_transit_city_coverage.json', 'r', encoding='utf-8') as f:
            expectedResponse = f.read()
        responses.add(responses.GET, 'https://cit.transit.api.here.com/v3/coverage/search.json',
                  expectedResponse, status=200)
        response = self._api.coverage_witin_a_city('chicago', 10, 1, 0, 'en')
        self.assertTrue(response)
        self.assertIsInstance(response, herepy.PublicTransitResponse)

    @responses.activate
    def test_coverage_witin_a_city_whenerroroccured(self):
        with open('testdata/models/public_transit_api_error.json', 'r') as f:
            expectedResponse = f.read()
        responses.add(responses.GET, 'https://cit.transit.api.here.com/v3/coverage/search.json',
                  expectedResponse, status=200)
        response = self._api.coverage_witin_a_city('', 10, 1, 0)
        self.assertIsInstance(response, herepy.HEREError)