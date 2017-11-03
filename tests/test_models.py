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
    
    with open('testdata/models/geocoder_autocomplete.json', 'rb') as f:
        GEOCODER_AUTO_COMPLETE_SAMPLE_JSON = json.loads(f.read().decode('utf8'))

    with open('testdata/models/places_api.json', 'rb') as f:
        PLACES_API_SAMPLE_JSON = json.loads(f.read().decode('utf8'))

    def test_geocoder_response(self):
        geocoderResponse = herepy.GeocoderResponse.new_from_jsondict(self.GEOCODER_SAMPLE_JSON)    
        try:
            geocoderResponse.__repr__()
        except Exception as e:
            self.fail(e)
        self.assertTrue(geocoderResponse.as_json_string())
        self.assertTrue(geocoderResponse.as_dict())

    def test_routing_response(self):
        routingResponse = herepy.RoutingResponse.new_from_jsondict(self.ROUTING_SAMPLE_JSON)
        try:
            routingResponse.__repr__()
        except Exception as e:
            self.fail(e)
        self.assertTrue(routingResponse.as_json_string())
        self.assertTrue(routingResponse.as_dict())

    def test_geocoder_autocompleteresponse(self):
        geocoderAutoCompleteResponse = herepy.GeocoderAutoCompleteResponse.new_from_jsondict(self.GEOCODER_AUTO_COMPLETE_SAMPLE_JSON)
        try:
            geocoderAutoCompleteResponse.__repr__()
        except Exception as e:
            self.fail(e)
        self.assertTrue(geocoderAutoCompleteResponse.as_json_string())
        self.assertTrue(geocoderAutoCompleteResponse.as_dict())

    def test_placesapi_response(self):
        placesApiResponse = herepy.PlacesResponse.new_from_jsondict(self.PLACES_API_SAMPLE_JSON)
        try:
            placesApiResponse.__repr__()
        except Exception as e:
            self.fail(e)
        self.assertTrue(placesApiResponse.as_json_string())
        self.assertTrue(placesApiResponse.as_dict())
