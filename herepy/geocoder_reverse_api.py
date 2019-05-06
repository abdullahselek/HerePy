#!/usr/bin/env python

from __future__ import division

import sys
import json
import requests

from herepy.here_api import HEREApi
from herepy.utils import Utils
from herepy.error import HEREError
from herepy.models import GeocoderReverseResponse

class GeocoderReverseApi(HEREApi):
    """A python interface into the HERE Geocoder Reverse API"""

    def __init__(self,
                 app_id=None,
                 app_code=None,
                 timeout=None):
        """Returns a GeocoderApi instance.
        Args:
          app_id (str):
            App Id taken from HERE Developer Portal.
          app_code (str):
            App Code taken from HERE Developer Portal.
          timeout (int):
            Timeout limit for requests.
        """

        super(GeocoderReverseApi, self).__init__(app_id, app_code, timeout)
        self._base_url = 'https://reverse.geocoder.api.here.com/6.2/reversegeocode.json'

    def __get(self, data):
        url = Utils.build_url(self._base_url, extra_params=data)
        response = requests.get(url, timeout=self._timeout)
        try:
            json_data = json.loads(response.content.decode('utf8'))
            if json_data.get('Response') != None:
                return GeocoderReverseResponse.new_from_jsondict(json_data)
            else:
                return HEREError(json_data.get('Details', 'Error occured on function ' + sys._getframe(1).f_code.co_name))
        except ValueError as err:
            return HEREError('Error occured on function ' + sys._getframe(1).f_code.co_name + ' ' + str(err))

    def retrieve_addresses(self, prox, radius=250, max_results=1, gen=9):
        """Gets the address information of a point within given radius
        Args:
          prox (lat/lon):
            latitude longitude of the point
          radius (int):
            radius of the area in meters
          max_results (int):
            maximum resuls to retrieve.
        Returns:
          GeocoderReverseResponse or HEREError instance"""

        data = {'prox': str.format('{0},{1},{2}', prox[0], prox[1], radius),
                'mode': 'retrieveAddresses',
                'maxresults': max_results,
                'gen': gen,
                'app_id': self._app_id,
                'app_code': self._app_code}
        return self.__get(data)

