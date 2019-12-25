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

class PublicTransitModeTypeTest(unittest.TestCase):

    def test_valueofenum(self):
        high_speed_train = herepy.PublicTransitModeType.high_speed_train
        self.assertEqual(high_speed_train.__str__(), "0")
        intercity_train = herepy.PublicTransitModeType.intercity_train
        self.assertEqual(intercity_train.__str__(), "1")
        inter_regional_train = herepy.PublicTransitModeType.inter_regional_train
        self.assertEqual(inter_regional_train.__str__(), "2")
        regional_train = herepy.PublicTransitModeType.regional_train
        self.assertEqual(regional_train.__str__(), "3")
        city_train = herepy.PublicTransitModeType.city_train
        self.assertEqual(city_train.__str__(), "4")
        bus = herepy.PublicTransitModeType.bus
        self.assertEqual(bus.__str__(), "5")
        ferry = herepy.PublicTransitModeType.ferry
        self.assertEqual(ferry.__str__(), "6")
        subway = herepy.PublicTransitModeType.subway
        self.assertEqual(subway.__str__(), "7")
        light_rail = herepy.PublicTransitModeType.light_rail
        self.assertEqual(light_rail.__str__(), "8")
        private_bus = herepy.PublicTransitModeType.private_bus
        self.assertEqual(private_bus.__str__(), "9")
        inclined = herepy.PublicTransitModeType.inclined
        self.assertEqual(inclined.__str__(), "10")
        aerial = herepy.PublicTransitModeType.aerial
        self.assertEqual(aerial.__str__(), "11")
        bus_rapid = herepy.PublicTransitModeType.bus_rapid
        self.assertEqual(bus_rapid.__str__(), "12")
        monorail = herepy.PublicTransitModeType.monorail
        self.assertEqual(monorail.__str__(), "13")
        flight = herepy.PublicTransitModeType.flight
        self.assertEqual(flight.__str__(), "14")
        walk = herepy.PublicTransitModeType.walk
        self.assertEqual(walk.__str__(), "20")

class PublicTransitRoutingModeTest(unittest.TestCase):

    def test_valueofenum(self):
        schedule = herepy.PublicTransitRoutingMode.schedule
        self.assertEqual(schedule.__str__(), 'schedule')
        realtime = herepy.PublicTransitRoutingMode.realtime
        self.assertEqual(realtime.__str__(), 'realtime')
