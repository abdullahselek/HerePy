#!/usr/bin/env python

import sys
import json
import requests

from herepy.here_api import HEREApi


class TrafficApi(HEREApi):
    """A python interface into the HERE Traffic API"""

    def __init__(self,
                 api_key: str=None,
                 timeout: int=None):
        """Returns a TrafficApi instance.
        Args:
          api_key (str):
            API key taken from HERE Developer Portal.
          timeout (int):
            Timeout limit for requests.
        """

        super(TrafficApi, self).__init__(api_key, timeout)
        self._base_url = 'https://traffic.ls.hereapi.com/traffic/6.0'
