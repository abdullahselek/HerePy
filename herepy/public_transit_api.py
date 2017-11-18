#!/usr/bin/env python

from __future__ import division

import sys
import json
import requests

from herepy.here_api import HEREApi
from herepy.utils import Utils
from herepy.error import HEREError
from herepy.models import PublicTransitResponse

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

    def __get(self, data):
        url = Utils.build_url(self._base_url, extra_params=data)
        response = requests.get(url, timeout=self._timeout)
        json_data = json.loads(response.content.decode('utf8'))
        if json_data.get('Res') != None:
            return PublicTransitResponse.new_from_jsondict(json_data)
        else:
            return HEREError(json_data.get('details', 'Error occured on ' + sys._getframe(1).f_code.co_name))
