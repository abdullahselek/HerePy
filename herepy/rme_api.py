#!/usr/bin/env python

import sys
import json
import requests

from herepy.here_api import HEREApi
from herepy.utils import Utils
from herepy.error import HEREError
from herepy.models import RmeResponse
from typing import List, Optional


class RmeApi(HEREApi):
    """A python interface into the RME API"""

    def __init__(self, api_key: str = None, timeout: int = None):
        """Returns a RmeApi instance.
        Args:
          api_key (str):
            API key taken from HERE Developer Portal.
          timeout (int):
            Timeout limit for requests.
        """

        super(RmeApi, self).__init__(api_key, timeout)
        self._base_url = "https://m.fleet.ls.hereapi.com/2/matchroute.json"

    def __get(self, data):
        url = Utils.build_url(self._base_url, extra_params=data)
        response = requests.get(url, timeout=self._timeout)
        try:
            json_data = json.loads(response.content.decode("utf8"))
            if json_data.get("TracePoints") != None:
                return RmeResponse.new_from_jsondict(json_data)
            else:
                raise HEREError(
                    json_data.get(
                        "Details",
                        "Error occurred on function " + sys._getframe(1).f_code.co_name,
                    )
                )
        except ValueError as err:
            raise HEREError(
                "Error occurred on function "
                + sys._getframe(1).f_code.co_name
                + " "
                + str(err)
            )

    def match_route(
        self, gpx_file_content: str, route_mode: str = "car", pde_layers: List[str] = []
    ) -> Optional[RmeResponse]:
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
          RmeResponse
        Raises:
          HEREError"""

        data = {
            "file": Utils.get_zipped_base64(gpx_file_content),
            "routemode": route_mode,
            "attributes": ",".join(pde_layers),
            "apikey": self._api_key,
        }
        return self.__get(data)
