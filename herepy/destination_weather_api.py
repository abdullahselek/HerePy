#!/usr/bin/env python

from __future__ import division

import sys
import json
import requests

from herepy.here_api import HEREApi
from herepy.utils import Utils
from herepy.error import HEREError
from herepy.models import DestinationWeatherResponse
from herepy.here_enum import WeatherProductType

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

    def _product_node(self, product):
          if product == WeatherProductType.observation:
              return 'observations'
          elif product == WeatherProductType.forecast_7days:
              return 'forecasts'
          elif product == WeatherProductType.forecast_7days_simple:
              return 'dailyForecasts'
          elif product == WeatherProductType.forecast_hourly:
              return 'hourlyForecasts'
          elif product == WeatherProductType.forecast_astronomy:
              return 'astronomy'
          elif product == WeatherProductType.alerts:
              return 'alerts'
          else:
              return 'nwsAlerts'  

    def forecast_astronomy(self, destination, product=WeatherProductType.observation):
        """Request forecast for given destination.
        Args:
          destination (str):
            Destination name.
          product (str):
            A parameter identifying the type of report to obtain. Default value `observation`.
        Returns:
          DestinationWeatherResponse instance or HEREError
        """

        data = {'app_id': self._app_id,
                'app_code': self._app_code,
                'product': product.__str__(),
                'name': destination}
        url = Utils.build_url(self._base_url, extra_params=data)
        response = requests.get(url, timeout=self._timeout)
        json_data = json.loads(response.content.decode('utf8'))
        if json_data.get(self._product_node(product)) != None:
            return DestinationWeatherResponse.new_from_jsondict(json_data, param_defaults={self._product_node(product): None})
        else:
            return HEREError(json_data.get('Message', 'Error occured on ' + sys._getframe(1).f_code.co_name))
