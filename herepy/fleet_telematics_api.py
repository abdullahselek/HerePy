#!/usr/bin/env python

import sys
import json
import requests

from herepy.here_api import HEREApi


class FleetTelematicsApi(HEREApi):
    """A python interface into the HERE Fleet Telematics API"""

    def __init__(self,
                 api_key: str=None,
		 timeout: int=None):
        """Returns a FleetTelematicsApi instance.
        Args:
          api_key (str):
            API key taken from HERE Developer Portal.
          timeout (int):
            Timeout limit for requests.
        """

        super(FleetTelematicsApi, self).__init__(api_key, timeout)
        self._base_url = 'https://wse.ls.hereapi.com/2/'

