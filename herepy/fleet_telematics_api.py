#!/usr/bin/env python

import sys
import json
import requests

from typing import List

from herepy.here_api import HEREApi
from herepy.here_enum import RouteMode


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


    def create_find_sequence_parameters(self,
                                        start: DestinationParam,
                                        intermediate_destinations: List[DestinationParam],
                                        end: DestinationParam,
                                        modes: [RouteMode]):
        data = {'apiKey': self._api_key,
                'start': start.__str__()}

        count = 0
        for destination_param in intermediate_destinations:
            count += 1
            data[str.format('destination{0}', count)] = destination_param.__str__()

        data['end'] = end.__str__()
        data['improveFor'] = 'time'
        data['departure'] = 'now'

        modes_str = ''
        for route_mode in modes:
            modes_str += route_mode.__str__() + ';'

        data['mode'] = modes_str
        return data
