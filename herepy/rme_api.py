#!/usr/bin/env python

from __future__ import division

import sys
import json
import requests

from herepy.here_api import HEREApi
from herepy.utils import Utils
from herepy.error import HEREError
from herepy.models import RmeResponse

class RmeApi(HEREApi):
    """A python interface into the RME API"""

    def __init__(self,
                 app_id=None,
                 app_code=None,
                 timeout=None):
        """Returns a RmeApi instance.
        Args:
          app_id (str):
            App Id taken from HERE Developer Portal.
          app_code (str):
            App Code taken from HERE Developer Portal.
          timeout (int):
            Timeout limit for requests.
        """

        super(RmeApi, self).__init__(app_id, app_code, timeout)
        self._base_url = 'https://rme.api.here.com/2/matchroute.json'

    def __get(self, data):
        url = Utils.build_url(self._base_url, extra_params=data)
        response = requests.get(url, timeout=self._timeout)
        try:
            json_data = json.loads(response.content.decode('utf8'))
            if json_data.get('TracePoints') != None:
                return RmeResponse.new_from_jsondict(json_data)
            else:
                return HEREError(json_data.get('Details', 'Error occured on function ' + sys._getframe(1).f_code.co_name))
        except ValueError as err:
            return HEREError('Error occured on function ' + sys._getframe(1).f_code.co_name + ' ' + str(err))

    def match_route(self, gpx_file_content, route_mode='car', pde_layers=[]):
        """Retrieves misc information about the route given in gpx file
        Args:
          gpxfile content (str):
            gpx file content as string
          routemode (str):
            route mode ('car')
          pde_layers (str list):
            PDE layers to retrieve e.g.:
              ROAD_GEOM_FCn(TUNNEL)
              SPEED_LIMITS_FCn(FROM_REF_SPEED_LIMIT,TO_REF_SPEED_LIMIT)
              ADAS_ATTRIB_FCn(SLOPES)
              
              or e.g.,

              ROAD_GEOM_FCn(*)
              SPEED_LIMITS_FCn(*)
        Returns:
          RmeResponse or HEREError instance"""

        data = {'file': Utils.get_zipped_base64(gpx_file_content),
                'route_mode': route_mode,
                'attributes': ','.join(pde_layers),
                'app_id': self._app_id,
                'app_code': self._app_code}
        return self.__get(data)

