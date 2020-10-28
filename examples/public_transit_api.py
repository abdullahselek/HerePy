#!/usr/bin/env python

from herepy import PublicTransitApi, PublicTransitSearchMethod

public_transit_api = PublicTransitApi(api_key="api_key")

# a list of public transit stations based on name
response = public_transit_api.find_stations_by_name(
    center=[40.7505, -73.9910],
    name="union",
    max_count=10,
    method=PublicTransitSearchMethod.fuzzy,
    radius=5000,
)
print(response.as_dict())
