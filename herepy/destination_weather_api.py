#!/usr/bin/env python

from __future__ import division

import sys
import json
import requests

from herepy.here_api import HEREApi

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
