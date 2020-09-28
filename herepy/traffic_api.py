#!/usr/bin/env python

import sys
import json
import requests

from herepy.here_api import HEREApi
from herepy.utils import Utils
from herepy.error import HEREError, UnauthorizedError, InvalidRequestError
from herepy.models import TrafficIncidentResponse
from herepy.here_enum import IncidentsCriticality

from typing import List, Optional


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
        self._base_url = 'https://traffic.ls.hereapi.com/traffic/6.0/'


    def __get(self, url, data):
        url = Utils.build_url(url, extra_params=data)
        response = requests.get(url, timeout=self._timeout)
        json_data = json.loads(response.content.decode('utf8'))
        if json_data.get('TRAFFICITEMS') != None:
            return TrafficIncidentResponse.new_from_jsondict(
                json_data, param_defaults={'TRAFFICITEMS': None}
            )
        else:
            error = self.__get_error_from_response(json_data)
            raise error


    def __get_error_from_response(self, json_data):
        if "error" in json_data:
            if json_data["error"] == "Unauthorized":
                return UnauthorizedError(json_data["error_description"])
        error_type = json_data.get("Type")
        error_message = json_data.get(
            "Message", "Error occured on " + sys._getframe(1).f_code.co_name
        )
        if error_type == "Invalid Request":
            return InvalidRequestError(error_message)
        else:
            return HEREError(error_message)


    def __prepare_criticality_values(self, criticality_enums: [IncidentsCriticality]):
        criticality_values = ""
        for criticality in criticality_enums:
            criticality_values += criticality.__str__() + ','
        criticality_values = criticality_values[:-1]
        return criticality_values


    def incidents_in_bounding_box(self, top_left: List[float],
                    bottom_right: List[float], criticality: [IncidentsCriticality]) -> Optional[TrafficIncidentResponse]:
        """Request traffic incident information within specified area.
        Args:
          top_left (array):
            array including latitude and longitude in order.
          bottom_right (array):
            array including latitude and longitude in order.
          criticality (array):
            List of IncidentsCriticality.
        Returns:
          TrafficIncidentResponse
        Raises:
          HEREError"""

        data = {'bbox': str.format('{0},{1};{2},{3}', top_left[0], top_left[1], bottom_right[0], bottom_right[1]),
                'apiKey': self._api_key,
                'criticality': self.__prepare_criticality_values(criticality_enums=criticality)}
        return self.__get(self._base_url + 'incidents.json', data)
