#!/usr/bin/env python

from __future__ import division

import sys
import json
import requests

from herepy.here_api import HEREApi
from herepy.utils import Utils
from herepy.error import HEREError
from herepy.models import PlacesResponse

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
        self._base_url = 'https://places.cit.api.here.com/places/v1/discover/search'
