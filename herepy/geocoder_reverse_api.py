#!/usr/bin/env python

import sys
import json
import requests

from herepy.here_api import HEREApi
from herepy.utils import Utils
from herepy.error import HEREError
from herepy.models import GeocoderReverseResponse
from typing import List

class GeocoderReverseApi(HEREApi):
    """A python interface into the HERE Geocoder Reverse API"""

    def __init__(self,
                 api_key: str=None,
                 timeout: int=None):
        """Returns a GeocoderApi instance.
        Args:
          api_key (str):
            API key taken from HERE Developer Portal.
          timeout (int):
            Timeout limit for requests.
        """

        super(GeocoderReverseApi, self).__init__(api_key, timeout)
        self._base_url = 'https://reverse.geocoder.ls.hereapi.com/6.2/reversegeocode.json'

    def __get(self, data):
        url = Utils.build_url(self._base_url, extra_params=data)
        response = requests.get(url, timeout=self._timeout)
        try:
            json_data = json.loads(response.content.decode('utf8'))
            if json_data.get('Response') != None:
                return GeocoderReverseResponse.new_from_jsondict(json_data)
            else:
                raise HEREError(json_data.get('Details', 'Error occured on function ' + sys._getframe(1).f_code.co_name))
        except ValueError as err:
            raise HEREError('Error occured on function ' + sys._getframe(1).f_code.co_name + ' ' + str(err))

    def retrieve_addresses(self, prox: List[float], radius: int=250, max_results: int=1, gen: int=9):
        """Gets the address information of a point within given radius
        Args:
          prox (lat/lon):
            latitude longitude of the point
          radius (int):
            radius of the area in meters
          max_results (int):
            maximum resuls to retrieve.
        Returns:
          GeocoderReverseResponse
        Raises:
          HEREError"""

        data = {'prox': str.format('{0},{1},{2}', prox[0], prox[1], radius),
                'mode': 'retrieveAddresses',
                'maxresults': max_results,
                'gen': gen,
                'apiKey': self._api_key}
        return self.__get(data)

