#!/usr/bin/env python

from __future__ import division

import sys
import json
import requests

from herepy.here_api import HEREApi
from herepy.utils import Utils
from herepy.error import HEREError
from herepy.models import DestinationWeatherResponse

class DestinationWeatherApi(HEREApi):
    """A python interface into the HERE Destination Weather API"""

    def __init__(self,
                 app_id=None,
                 app_code=None,
                 timeout=None):
        """Returns a DestinationWeatherApi instance.
        Args:
          app_id (str):
            App Id taken from HERE Developer Portal.
          app_code (str):
            App Code taken from HERE Developer Portal.
          timeout (int):
            Timeout limit for requests.
        """

        super(DestinationWeatherApi, self).__init__(app_id, app_code, timeout)
        self._base_url = 'https://weather.api.here.com/weather/1.0/report.json'

    def forecast_astronomy(self, destination):
        """Request forecast for given destination.
        Args:
          destination (str):
            Destination name.
        Returns:
          DestinationWeatherResponse instance or HEREError
        """

        data = {'app_id': self._app_id,
                'app_code': self._app_code,
                'product': destination}
        url = Utils.build_url(self._base_url, extra_params=data)
        response = requests.get(url, timeout=self._timeout)
        json_data = json.loads(response.content.decode('utf8'))
        if json_data.get('astronomy') != None:
            return DestinationWeatherResponse.new_from_jsondict(json_data)
        else:
            return HEREError(json_data.get('Message', 'Error occured on ' + sys._getframe(1).f_code.co_name))
