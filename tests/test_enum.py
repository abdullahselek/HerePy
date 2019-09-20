#!/usr/bin/env python

import unittest
import herepy
import sys

from enum import Enum

class RouteModeTest(unittest.TestCase):

    def test_valueofenum(self):
        fastest = herepy.RouteMode.fastest        
        self.assertEqual(fastest.__str__(), 'fastest')
        shortest = herepy.RouteMode.shortest        
        self.assertEqual(shortest.__str__(), 'shortest')
        balanced = herepy.RouteMode.balanced        
        self.assertEqual(balanced.__str__(), 'balanced')
        car = herepy.RouteMode.car
        self.assertEqual(car.__str__(), 'car')
        car_hov = herepy.RouteMode.car_hov
        self.assertEqual(car_hov.__str__(), 'carHOV')
        traffic_disabled = herepy.RouteMode.traffic_disabled
        self.assertEqual(traffic_disabled.__str__(), 'traffic:disabled')
        enabled = herepy.RouteMode.enabled
        self.assertEqual(enabled.__str__(), 'enabled')
        pedestrian = herepy.RouteMode.pedestrian
        self.assertEqual(pedestrian.__str__(), 'pedestrian')
        publicTransport = herepy.RouteMode.publicTransport
        self.assertEqual(publicTransport.__str__(), 'publicTransport')
        truck = herepy.RouteMode.truck
        self.assertEqual(truck.__str__(), 'truck')
        traffic_default = herepy.RouteMode.traffic_default
        self.assertEqual(traffic_default.__str__(), 'traffic:default')
        traffic_enabled = herepy.RouteMode.traffic_enabled
        self.assertEqual(traffic_enabled.__str__(), 'traffic:enabled')

class PlacesCategoryTest(unittest.TestCase):

    def test_valueofenum(self):
        accomodation = herepy.PlacesCategory.accomodation
        self.assertEqual(accomodation.__str__(), 'accomodation')

class PublicTransitSearchMethodTest(unittest.TestCase):

    def test_valueofenum(self):
        fuzzy = herepy.PublicTransitSearchMethod.fuzzy
        self.assertEqual(fuzzy.__str__(), 'fuzzy')
        strict = herepy.PublicTransitSearchMethod.strict
        self.assertEqual(strict.__str__(), 'strict')

class PublicTransitRoutingTypeTest(unittest.TestCase):

    def test_valueofenum(self):
        time_tabled = herepy.PublicTransitRoutingType.time_tabled
        self.assertEqual(time_tabled.__str__(), 'tt')
        simple = herepy.PublicTransitRoutingType.simple
        self.assertEqual(simple.__str__(), 'sr')
        all = herepy.PublicTransitRoutingType.all
        self.assertEqual(all.__str__(), 'all')
