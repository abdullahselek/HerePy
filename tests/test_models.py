#!/usr/bin/env python

import json
import re
import unittest

import herepy


class ModelsTest(unittest.TestCase):

    with open("testdata/models/geocoder.json", "rb") as f:
        GEOCODER_SAMPLE_JSON = json.loads(f.read().decode("utf8"))

    with open("testdata/models/routing.json", "rb") as f:
        ROUTING_SAMPLE_JSON = json.loads(f.read().decode("utf8"))

    with open("testdata/models/matrix.json", "rb") as f:
        ROUTING_MATRIX_SAMPLE_JSON = json.loads(f.read().decode("utf8"))

    with open("testdata/models/geocoder_autocomplete.json", "rb") as f:
        GEOCODER_AUTO_COMPLETE_SAMPLE_JSON = json.loads(f.read().decode("utf8"))

    with open("testdata/models/places_api.json", "rb") as f:
        PLACES_API_SAMPLE_JSON = json.loads(f.read().decode("utf8"))

    with open("testdata/models/public_transit_api.json", "rb") as f:
        PUBLIC_TRANSIT_API_SAMPLE_JSON = json.loads(f.read().decode("utf8"))

    with open("testdata/models/traffic_api_incidents.json", "rb") as f:
        TRAFFIC_INCIDENTS_SAMPLE_JSON = json.loads(f.read().decode("utf8"))

    with open("testdata/models/destination_weather_observations.json", "rb") as f:
        DESTINATION_WEATHER_SAMPLE_JSON = json.loads(f.read().decode("utf8"))

    with open("testdata/models/traffic_api_flow.json", "rb") as f:
        TRAFFIC_FLOW_SAMPLE_JSON = json.loads(f.read().decode("utf8"))

    with open("testdata/models/traffic_api_flow_availability.json", "rb") as f:
        TRAFFIC_FLOW_AVAILABILITY_JSON = json.loads(f.read().decode("utf8"))

    with open("testdata/models/isoline_routing_distance_response.json", "rb") as f:
        ISOLINE_ROUTING_DISTANCE_JSON = json.loads(f.read().decode("utf8"))

    def test_geocoder_response(self):
        geocoderResponse = herepy.GeocoderResponse.new_from_jsondict(
            self.GEOCODER_SAMPLE_JSON
        )
        try:
            geocoderResponse.__repr__()
        except Exception as e:
            self.fail(e)
        self.assertTrue(geocoderResponse.as_json_string())
        self.assertTrue(geocoderResponse.as_dict())

    def test_routing_response(self):
        routingResponse = herepy.RoutingResponse.new_from_jsondict(
            self.ROUTING_SAMPLE_JSON
        )
        try:
            routingResponse.__repr__()
        except Exception as e:
            self.fail(e)
        self.assertTrue(routingResponse.as_json_string())
        self.assertTrue(routingResponse.as_dict())

    def test_routingapi_matrix_response(self):
        routing_matrix_response = herepy.RoutingResponse.new_from_jsondict(
            self.ROUTING_MATRIX_SAMPLE_JSON
        )
        try:
            routing_matrix_response.__repr__()
        except Exception as e:
            self.fail(e)
        self.assertTrue(routing_matrix_response.as_json_string())
        self.assertTrue(routing_matrix_response.as_dict())

    def test_geocoder_autocompleteresponse(self):
        geocoderAutoCompleteResponse = (
            herepy.GeocoderAutoCompleteResponse.new_from_jsondict(
                self.GEOCODER_AUTO_COMPLETE_SAMPLE_JSON
            )
        )
        try:
            geocoderAutoCompleteResponse.__repr__()
        except Exception as e:
            self.fail(e)
        self.assertTrue(geocoderAutoCompleteResponse.as_json_string())
        self.assertTrue(geocoderAutoCompleteResponse.as_dict())

    def test_placesapi_response(self):
        placesApiResponse = herepy.PlacesResponse.new_from_jsondict(
            self.PLACES_API_SAMPLE_JSON
        )
        try:
            placesApiResponse.__repr__()
        except Exception as e:
            self.fail(e)
        self.assertTrue(placesApiResponse.as_json_string())
        self.assertTrue(placesApiResponse.as_dict())

    def test_publictransitapi_response(self):
        publicTransitResponse = herepy.PublicTransitResponse.new_from_jsondict(
            self.PUBLIC_TRANSIT_API_SAMPLE_JSON
        )
        try:
            publicTransitResponse.__repr__()
        except Exception as e:
            self.fail(e)
        self.assertTrue(publicTransitResponse.as_json_string())
        self.assertTrue(publicTransitResponse.as_dict())

    def test_traffic_incident_response(self):
        trafficIncidentResponse = herepy.TrafficIncidentResponse.new_from_jsondict(
            self.TRAFFIC_INCIDENTS_SAMPLE_JSON
        )
        try:
            trafficIncidentResponse.__repr__()
        except Exception as e:
            self.fail(e)
        self.assertTrue(trafficIncidentResponse.as_json_string())
        self.assertTrue(trafficIncidentResponse.as_dict())

    def test_destination_weather_response(self):
        destinationWeatherResponse = (
            herepy.DestinationWeatherResponse.new_from_jsondict(
                self.DESTINATION_WEATHER_SAMPLE_JSON, {"observations": None}
            )
        )
        try:
            destinationWeatherResponse.__repr__()
        except Exception as e:
            self.fail(e)
        self.assertTrue(destinationWeatherResponse.as_json_string())
        self.assertTrue(destinationWeatherResponse.as_dict())

    def test_traffic_flow_response(self):
        trafficFlowResponse = herepy.TrafficFlowResponse.new_from_jsondict(
            self.TRAFFIC_FLOW_SAMPLE_JSON
        )
        try:
            trafficFlowResponse.__repr__()
        except Exception as e:
            self.fail(e)
        self.assertIsNotNone(trafficFlowResponse.as_json_string())
        self.assertIsNotNone(trafficFlowResponse.as_dict())

    def test_traffic_flow_availability_response(self):
        trafficFlowAvailabilityResponse = (
            herepy.TrafficFlowAvailabilityResponse.new_from_jsondict(
                self.TRAFFIC_FLOW_AVAILABILITY_JSON
            )
        )
        try:
            trafficFlowAvailabilityResponse.__repr__()
        except Exception as e:
            self.fail(e)
        self.assertIsNotNone(trafficFlowAvailabilityResponse.as_json_string())
        self.assertIsNotNone(trafficFlowAvailabilityResponse.as_dict())
        self.assertIsNotNone(
            trafficFlowAvailabilityResponse.as_dict()["Response"]["Region"]
        )

    def test_isoline_routing_response(self):
        isolineRoutingDistanceResponse = (
            herepy.IsolineRoutingResponse.new_from_jsondict(
                self.ISOLINE_ROUTING_DISTANCE_JSON
            )
        )
        try:
            isolineRoutingDistanceResponse.__repr__()
        except Exception as e:
            self.fail(e)
        self.assertIsNotNone(isolineRoutingDistanceResponse.as_json_string())
        self.assertIsNotNone(isolineRoutingDistanceResponse.as_dict())
        self.assertIsNotNone(isolineRoutingDistanceResponse.as_dict()["departure"])
        self.assertTrue(len(isolineRoutingDistanceResponse.as_dict()["isolines"]) > 0)
