#!/usr/bin/env python

import json
import re
import unittest
import herepy

class ModelsTest(unittest.TestCase):

    with open('testdata/models/geocoder.json', 'rb') as f:
        GEOCODER_SAMPLE_JSON = json.loads(f.read().decode('utf8'))

    with open('testdata/models/routing.json', 'rb') as f:
        ROUTING_SAMPLE_JSON = json.loads(f.read().decode('utf8'))

    def testGeocoderResponse(self):
        geocoderResponse = herepy.GeocoderResponse.NewFromJsonDict(self.GEOCODER_SAMPLE_JSON)    
        try:
            geocoderResponse.__repr__()
        except Exception as e:
            self.fail(e)
        self.assertTrue(geocoderResponse.AsJsonString())
        self.assertTrue(geocoderResponse.AsDict())

    def testRoutingResponse(self):
        routingResponse = herepy.RoutingResponse.NewFromJsonDict(self.ROUTING_SAMPLE_JSON)
        try:
            routingResponse.__repr__()
        except Exception as e:
            self.fail(e)
        self.assertTrue(routingResponse.AsJsonString())
        self.assertTrue(routingResponse.AsDict())
