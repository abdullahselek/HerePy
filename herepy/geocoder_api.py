#!/usr/bin/env python

from __future__ import division

import json
import requests
import io
import warnings
import sys

class GeocoderApi(object):
    """A python interface into the HERE Geocoder API"""

    _API_REALM = 'HERE Geocoder API'

    def __init__(self,
                 app_id=None,
                 app_code=None):
        self.SetCredentials(app_id, app_code)
        self._baseUrl = 'https://geocoder.cit.api.here.com/6.2/geocode.json'

    def SetCredentials(self, 
                       app_id, 
                       app_code):
        self._app_id = app_id
        self._app_code = app_code
