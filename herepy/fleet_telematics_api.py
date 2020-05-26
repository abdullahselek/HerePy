#!/usr/bin/env python

import sys
import json
import requests

from typing import List

from herepy.here_api import HEREApi
from herepy.here_enum import RouteMode
from herepy.utils import Utils
from herepy.models import WaypointSequenceResponse
from herepy.error import HEREError


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


    def __create_find_sequence_parameters(self,
                                          start: DestinationParam,
                                          intermediate_destinations: List[DestinationParam],
                                          end: DestinationParam,
                                          modes: List[RouteMode]):
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


    def __get(self, base_url, data, response_cls):
        url = Utils.build_url(base_url, extra_params=data)
        response = requests.get(url, timeout=self._timeout)
        json_data = json.loads(response.content.decode('utf8'))
        if json_data.get('results') is not None:
            return response_cls.new_from_jsondict(json_data)
        else:
            raise error_from_fleet_telematics_service_error(json_data)


    def find_sequence(self,
                      start: DestinationParam,
                      intermediate_destinations: List[DestinationParam],
                      end: DestinationParam,
                      modes: List[RouteMode]):
        data = self.__create_find_sequence_parameters(start=start,
                                                      intermediate_destinations=intermediate_destinations,
                                                      end=end,
                                                      modes=modes)
        response = self.__get(self._base_url + 'findsequence.json', data, WaypointSequenceResponse)
        return response


class UnauthorizedError(HEREError):

    """Unauthorized Error Type.
    This error is returned if the specified token was invalid or no contract
    could be found for this token.
    """


def error_from_fleet_telematics_service_error(json_data: dict):
    """Return the correct subclass for sequence errors"""

    if 'Type' in json_data:
        error_type = json_data['error']
        message = json_data['error_description']

        if error_type == 'Unauthorized':
            return UnauthorizedError(message)
    # pylint: disable=W0212
    return HEREError('Error occured on ' + sys._getframe(1).f_code.co_name)
