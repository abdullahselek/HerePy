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
        Returns:
          FleetTelematicsApi instance.
        """

        super(FleetTelematicsApi, self).__init__(api_key, timeout)
        self._base_url = 'https://wse.ls.hereapi.com/2/'


class DestinationParam(object):
    """Class that represents destination parameters used in FleetTelematicsApi."""

    def __init__(self,
                 text:str,
                 latitude: float,
                 longitude: float):
        """Initiates a new destination param instance.
        Args:
          text (str):
            String value that indicates location text.
          latitude (float):
            Latitude of coordinate.
          longitude (float):
            Longitude of coordinate.
        Returns:
          DestinationParam instance.
        """

        self.text = text
        self.latitude = latitude
        self.longitude = longitude


    def __str__(self):
        return str.format('{0};{1},{2}', self.text, self.latitude, self.longitude)
