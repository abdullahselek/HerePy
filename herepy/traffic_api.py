#!/usr/bin/env python

import sys
import json
import requests

from herepy.here_api import HEREApi
from herepy.utils import Utils
from herepy.error import HEREError, UnauthorizedError, InvalidRequestError
from herepy.models import TrafficIncidentResponse


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


    def _get(self, data):
        url = Utils.build_url(self._base_url, extra_params=data)
        response = requests.get(url, timeout=self._timeout)
        json_data = json.loads(response.content.decode('utf8'))
        if json_data.get('TRAFFICITEMS') != None:
            return TrafficIncidentResponse.new_from_jsondict(
                json_data, param_defaults={'TRAFFICITEMS': None}
            )
        else:
            error = self._get_error_from_response(json_data)
            raise error


    def _get_error_from_response(self, json_data):
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
