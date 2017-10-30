#!/usr/bin/env python

import unittest
import herepy
import sys

from enum import Enum

class RouteModeTest(unittest.TestCase):

    def testValueOfEnum(self):
        fastest = herepy.RouteMode.fastest        
        self.assertEqual(fastest.__str__(), 'fastest')
        car = herepy.RouteMode.car
        self.assertEqual(car.__str__(), 'car')
        traffic_disabled = herepy.RouteMode.traffic_disabled
        self.assertEqual(traffic_disabled.__str__(), 'traffic:disabled')
        enabled = herepy.RouteMode.enabled
        self.assertEqual(enabled.__str__(), 'enabled')
        pedestrian = herepy.RouteMode.pedestrian
        self.assertEqual(pedestrian.__str__(), 'pedestrian')
        publicTransport = herepy.RouteMode.publicTransport
        self.assertEqual(publicTransport.__str__(), 'publicTransport')
