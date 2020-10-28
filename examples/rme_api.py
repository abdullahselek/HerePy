#!/usr/bin/env python

import io

from herepy import RmeApi

rme_api = RmeApi(api_key="api_key")

# retrieves misc information about the route given in gpx file
with io.open("testdata/routes/sample.gpx", encoding="utf-8") as gpx_file:
    gpx_content = gpx_file.read()
response = rme_api.match_route(gpx_content, ["ADAS_ATTRIB_FCn(SLOPES)"])
print(response.as_dict())
