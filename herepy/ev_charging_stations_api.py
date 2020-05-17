#!/usr/bin/env python

import sys
import json
import requests


class EVChargingStationsApi():
    """A python interface into the HERE EV Charging Stations API"""

    def __init__(self,
                 app_id: str=None,
                 app_code: str=None,
                 timeout: int=None):
        """Returns a EVChargingStationsApi instance.
        Args:
          app_id (str):
            App Id taken from HERE Developer Portal.
          app_code (str):
            API Code taken from HERE Developer Portal.
          timeout (int):
            Timeout limit for requests.
        """

        self._app_id = app_id
        self._app_code = app_code
        if timeout:
            self._timeout = timeout
        else:
            self._timeout = 20
        self._base_url = "https://ev-v2.cit.cc.api.here.com/ev/"
