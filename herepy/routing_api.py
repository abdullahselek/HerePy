#!/usr/bin/env python

from __future__ import division

import json
import requests
import io
import warnings
import sys

try:
    # python 3
    from urllib.parse import urlparse, urlunparse, urlencode
except ImportError:
    from urlparse import urlparse, urlunparse
    from urllib import urlencode

from herepy.error import (
    HEREError
)

from herepy.models import (
    RoutingResponse
)

class RoutingApi(object):
    """A python interface into the HERE Routing API"""

    def __init__(self,
                 app_id=None,
                 app_code=None,
                 timeout=None):
        """Returns a RoutingApi instance.
        Args:
          app_id (string): App Id taken from HERE Developer Portal.
          app_code (string): App Code taken from HERE Developer Portal.
          timeout (int): Timeout limit for requests.
        """
        self.SetCredentials(app_id, app_code)
        self._baseUrl = 'https://route.cit.api.here.com/routing/7.2/calculateroute.json'
        if timeout:
            self._timeout = timeout
        else:
            self._timeout = 20

    def SetCredentials(self, 
                       app_id, 
                       app_code):
        """Setter for credentials.
        Args:
          app_id (string): App Id taken from HERE Developer Portal.
          app_code (string): App Code taken from HERE Developer Portal.
        """
        self._app_id = app_id
        self._app_code = app_code
