#!/usr/bin/env python

from __future__ import division

import sys
import json
import requests

from herepy.here_api import HEREApi
from herepy.utils import Utils
from herepy.error import HEREError
from herepy.models import (
    PlacesResponse,
    PlacesSuggestionsResponse,
    PlaceCategoriesResponse
)

class PlacesApi(HEREApi):
    """A python interface into the HERE Places (Search) API"""

    def __init__(self,
                 app_id=None,
                 app_code=None,
                 timeout=None):
        """Return a PlacesApi instance.
        Args:
          app_id (string): App Id taken from HERE Developer Portal.
          app_code (string): App Code taken from HERE Developer Portal.
          timeout (int): Timeout limit for requests.
        """

        super(PlacesApi, self).__init__(app_id, app_code, timeout)
        self._base_url = 'https://places.cit.api.here.com/places/v1/'

    def __get(self, data, path, headers=None):
        url = Utils.build_url(self._base_url + path, extra_params=data)
        if headers != None:
            response = requests.get(url, timeout=self._timeout, headers=headers)
        else:
            response = requests.get(url, timeout=self._timeout)
        json_data = json.loads(response.content.decode('utf8'))
        if json_data.get('results') != None:
            return PlacesResponse.new_from_jsondict(json_data)
        else:
            return HEREError(json_data.get('message', 'Error occured on ' + sys._getframe(1).f_code.co_name))

    def __get_suggestions(self, data):
        url = Utils.build_url(self._base_url + 'suggest', extra_params=data)
        response = requests.get(url, timeout=self._timeout)
        json_data = json.loads(response.content.decode('utf8'))
        if json_data.get('suggestions') != None:
            return PlacesSuggestionsResponse.new_from_jsondict(json_data)
        else:
            return HEREError(json_data.get('message', 'Error occured on ' + sys._getframe(1).f_code.co_name))

    def __get_categories(self, data):
        url = Utils.build_url(self._base_url + 'categories/places', extra_params=data)
        response = requests.get(url, timeout=self._timeout)
        json_data = json.loads(response.content.decode('utf8'))
        if json_data.get('items') != None:
            return PlaceCategoriesResponse.new_from_jsondict(json_data)
        else:
            return HEREError(json_data.get('message', 'Error occured on ' + sys._getframe(1).f_code.co_name))

    def onebox_search(self, coordinates, query):
        """Request a list of nearby places based on a query string
        Args:
          coordinates (array): array including latitude and longitude in order.
          query (string): search term.
        Returns:
          PlacesResponse instance or HEREError"""

        data = {'at': str.format('{0},{1}', coordinates[0], coordinates[1]),
                'q':  query,
                'app_id': self._app_id,
                'app_code': self._app_code}
        return self.__get(data, 'discover/search')

    def places_at(self, coordinates):
        """Request a list of popular places around a location
        Args:
          coordinates (array): array including latitude and longitude in order.
        Returns:
          PlacesResponse instance or HEREError"""

        data = {'at': str.format('{0},{1}', coordinates[0], coordinates[1]),
                'app_id': self._app_id,
                'app_code': self._app_code}
        return self.__get(data, 'discover/explore')

    @classmethod
    def __prepare_category_values(cls, categories):
        category_values = ""
        for category in categories:
            category_values += category.__str__() + ';'
        category_values = category_values[:-1]
        return category_values

    def category_places_at(self, coordinates, categories=None):
        """Request a list of places within a category around a location
        Args:
          coordinates (array): array including latitude and longitude in order.
          categories (array): array including PlacesCategory enums.
        Returns:
          PlacesResponse instance or HEREError"""

        if categories is None:
          raise Exception(sys._getframe(0).f_code.co_name + ' function requires category types!')

        data = {'at': str.format('{0},{1}', coordinates[0], coordinates[1]),
                'cat': self.__prepare_category_values(categories),
                'app_id': self._app_id,
                'app_code': self._app_code}
        return self.__get(data, 'discover/explore')

    def nearby_places(self, coordinates):
        """Request a list of places close to a location
        Args:
          coordinates (array): array including latitude and longitude in order.
        Returns:
          PlacesResponse instance or HEREError"""

        data = {'at': str.format('{0},{1}', coordinates[0], coordinates[1]),
                'app_id': self._app_id,
                'app_code': self._app_code}
        return self.__get(data, 'discover/here')

    def search_suggestions(self, coordinates, query):
        """Request a list of suggestions based on a partial query string
        Args:
          coordinates (array): array including latitude and longitude in order.
          query (string): search term.
        Returns:
          PlacesSuggestionsResponse instance or HEREError"""

        data = {'at': str.format('{0},{1}', coordinates[0], coordinates[1]),
                'q': query,
                'app_id': self._app_id,
                'app_code': self._app_code}
        return self.__get_suggestions(data)

    def place_categories(self, coordinates):
        """Request a list of place categories available for a given location
        Args:
          coordinates (array): array including latitude and longitude in order.
        Returns:
          PlaceCategoriesResponse instance or HEREError"""

        data = {'at': str.format('{0},{1}', coordinates[0], coordinates[1]),
                'app_id': self._app_id,
                'app_code': self._app_code}
        return self.__get_categories(data)

    def places_at_boundingbox(self, coordinates_a, coordinates_b):
        """Request a list of popular places within a specified area
        Args:
          coordinates_a (array): array including latitude and longitude in order.
          coordinates_b (array): array including latitude and longitude in order.
        Returns:
          PlacesResponse instance or HEREError"""

        data = {'in': str.format('{0},{1},{2},{3}', coordinates_a[0], coordinates_a[1], coordinates_b[0], coordinates_b[1]),
                'app_id': self._app_id,
                'app_code': self._app_code}
        return self.__get(data, 'discover/explore')

    def places_with_language(self, coordinates, language):
        """Request a list of popular places around a location using a foreign language
        Args:
          coordinates (array): array including latitude and longitude in order.
          language (string): string value for language like `en-US`
        Returns:
          PlacesResponse instance or HEREError"""

        data = {'at': str.format('{0},{1}', coordinates[0], coordinates[1]),
                'app_id': self._app_id,
                'app_code': self._app_code}
        headers = {'accept-language': language}
        return self.__get(data, 'discover/explore')
