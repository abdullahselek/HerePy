#!/usr/bin/env python

from __future__ import division

import sys
import json
import requests

from herepy.here_api import HEREApi
from herepy.utils import Utils
from herepy.error import HEREError

class PublicTransitApi(HEREApi):
    """A python interface into the HERE Public Transit API"""

    def __init__(self,
                 app_id=None,
                 app_code=None,
                 timeout=None):
        """Return a PublicTransitApi instance.
        Args:
          app_id (string): App Id taken from HERE Developer Portal.
          app_code (string): App Code taken from HERE Developer Portal.
          timeout (int): Timeout limit for requests.
        """

        super(PublicTransitApi, self).__init__(app_id, app_code, timeout)
        self._base_url = 'https://cit.transit.api.here.com/v3/stations/'
