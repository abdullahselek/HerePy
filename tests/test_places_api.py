#!/usr/bin/env python

import os
import sys
import io
import unittest
import responses
import codecs
import herepy

class PlacesApiTest(unittest.TestCase):

    def setUp(self):
        api = herepy.PlacesApi('api_key')
        self._api = api

    def test_initiation(self):
        self.assertIsInstance(self._api, herepy.PlacesApi)
        self.assertEqual(self._api._api_key, 'api_key')
        self.assertEqual(self._api._base_url, 'https://places.ls.hereapi.com/places/v1/')

    @responses.activate
    def test_onebox_search_whensucceed(self):
        with open('testdata/models/places_api.json', 'r') as f:
            expectedResponse = f.read()
        responses.add(responses.GET, 'https://places.ls.hereapi.com/places/v1/discover/search',
                  expectedResponse, status=200)
        response = self._api.onebox_search([37.7905, -122.4107], 'restaurant')
        self.assertTrue(response)
        self.assertIsInstance(response, herepy.PlacesResponse)

    @responses.activate
    def test_onebox_search_whenerroroccured(self):
        with open('testdata/models/places_api_error.json', 'r') as f:
            expectedResponse = f.read()
        responses.add(responses.GET, 'https://places.ls.hereapi.com/places/v1/discover/search',
                  expectedResponse, status=200)
        with self.assertRaises(herepy.HEREError):
            self._api.onebox_search([37.7905, -122.4107], '')

    @responses.activate
    def test_places_at_whensucceed(self):
        with open('testdata/models/places_api.json', 'r') as f:
            expectedResponse = f.read()
        responses.add(responses.GET, 'https://places.ls.hereapi.com/places/v1/discover/explore',
                  expectedResponse, status=200)
        response = self._api.places_at([37.7905, -122.4107])
        self.assertTrue(response)
        self.assertIsInstance(response, herepy.PlacesResponse)

    @responses.activate
    def test_places_at_whenerroroccured(self):
        with open('testdata/models/places_api_error.json', 'r') as f:
            expectedResponse = f.read()
        responses.add(responses.GET, 'https://places.ls.hereapi.com/places/v1/discover/explore',
                  expectedResponse, status=200)
        with self.assertRaises(herepy.HEREError):
            self._api.places_at([-9999.0, -9999.0])

    @responses.activate
    def test_category_places_at_whensucceed(self):
        with open('testdata/models/places_api.json', 'r') as f:
            expectedResponse = f.read()
        responses.add(responses.GET, 'https://places.ls.hereapi.com/places/v1/discover/explore',
                  expectedResponse, status=200)
        response = self._api.category_places_at([37.7905, -122.4107], [herepy.PlacesCategory.eat_drink])
        self.assertTrue(response)
        self.assertIsInstance(response, herepy.PlacesResponse)

    @responses.activate
    def test_category_places_at_whenerroroccured(self):
        with open('testdata/models/places_api_error.json', 'r') as f:
            expectedResponse = f.read()
        responses.add(responses.GET, 'https://places.ls.hereapi.com/places/v1/discover/explore',
                  expectedResponse, status=200)
        with self.assertRaises(herepy.HEREError):
            self._api.category_places_at([-9999.0, -9999.0], [herepy.PlacesCategory.eat_drink])

    def test_category_places_at_withoutnocategories(self):
        with self.assertRaises(Exception) as context:
            self._api.category_places_at([37.7905, -122.4107])
        self.assertTrue('category_places_at function requires category types!' in str(context.exception))

    @responses.activate
    def test_nearby_places_whensucceed(self):
        with open('testdata/models/places_api.json', 'r') as f:
            expectedResponse = f.read()
        responses.add(responses.GET, 'https://places.ls.hereapi.com/places/v1/discover/here',
                  expectedResponse, status=200)
        response = self._api.nearby_places([37.7905, -122.4107])
        self.assertTrue(response)
        self.assertIsInstance(response, herepy.PlacesResponse)

    @responses.activate
    def test_nearby_places_whenerroroccured(self):
        with open('testdata/models/places_api_error.json', 'r') as f:
            expectedResponse = f.read()
        responses.add(responses.GET, 'https://places.ls.hereapi.com/places/v1/discover/here',
                  expectedResponse, status=200)
        with self.assertRaises(herepy.HEREError):
            self._api.nearby_places([-9999.0, -9999.0])

    @responses.activate
    def test_search_suggestions_whensucceed(self):
        with io.open('testdata/models/places_api_suggestions.json', 'r', encoding='utf-8') as f:
            expectedResponse = f.read()
        responses.add(responses.GET, 'https://places.ls.hereapi.com/places/v1/suggest',
                  expectedResponse, status=200)
        response = self._api.search_suggestions([52.5159, 13.3777], 'berlin')
        self.assertTrue(response)
        self.assertIsInstance(response, herepy.PlacesSuggestionsResponse)

    @responses.activate
    def test_search_suggestions_whenerroroccured(self):
        with open('testdata/models/places_api_error.json', 'r') as f:
            expectedResponse = f.read()
        responses.add(responses.GET, 'https://places.ls.hereapi.com/places/v1/suggest',
                  expectedResponse, status=200)
        with self.assertRaises(herepy.HEREError):
            self._api.search_suggestions([-9999.0, -9999.0], '')

    @responses.activate
    def test_place_categories_whensucceed(self):
        with open('testdata/models/places_api_categories.json', 'r') as f:
            expectedResponse = f.read()
        responses.add(responses.GET, 'https://places.ls.hereapi.com/places/v1/categories/places',
                  expectedResponse, status=200)
        response = self._api.place_categories([52.5159, 13.3777])
        self.assertTrue(response)
        self.assertIsInstance(response, herepy.PlaceCategoriesResponse)

    @responses.activate
    def test_place_categories_whenerroroccured(self):
        with open('testdata/models/places_api_error.json', 'r') as f:
            expectedResponse = f.read()
        responses.add(responses.GET, 'https://places.ls.hereapi.com/places/v1/categories/places',
                  expectedResponse, status=200)
        with self.assertRaises(herepy.HEREError):
            self._api.place_categories([-9999.0, -9999.0])

    @responses.activate
    def test_places_at_boundingbox_whensucceed(self):
        with open('testdata/models/places_api.json', 'r') as f:
            expectedResponse = f.read()
        responses.add(responses.GET, 'https://places.ls.hereapi.com/places/v1/discover/explore',
                  expectedResponse, status=200)
        response = self._api.places_at_boundingbox([-122.408, 37.793], [-122.4070, 37.7942])
        self.assertTrue(response)
        self.assertIsInstance(response, herepy.PlacesResponse)

    @responses.activate
    def test_places_at_boundingbox_whenerroroccured(self):
        with open('testdata/models/places_api_error.json', 'r') as f:
            expectedResponse = f.read()
        responses.add(responses.GET, 'https://places.ls.hereapi.com/places/v1/discover/explore',
                  expectedResponse, status=200)
        with self.assertRaises(herepy.HEREError):
            self._api.places_at_boundingbox([-9999.0, -9999.0], [-9999.0, -9999.0])

    @responses.activate
    def test_places_with_language_whensucceed(self):
        with open('testdata/models/places_api.json', 'r') as f:
            expectedResponse = f.read()
        responses.add(responses.GET, 'https://places.ls.hereapi.com/places/v1/discover/explore',
                  expectedResponse, status=200)
        response = self._api.places_with_language([48.8580, 2.2945], 'en-US')
        self.assertTrue(response)
        self.assertIsInstance(response, herepy.PlacesResponse)

    @responses.activate
    def test_places_with_language_whenerroroccured(self):
        with open('testdata/models/places_api_error.json', 'r') as f:
            expectedResponse = f.read()
        responses.add(responses.GET, 'https://places.ls.hereapi.com/places/v1/discover/explore',
                  expectedResponse, status=200)
        with self.assertRaises(herepy.HEREError):
            self._api.places_with_language([-9999.0, -9999.0], '')
