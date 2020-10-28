#!/usr/bin/env python

from herepy import GeocoderReverseApi

geocoder_reverse_api = GeocoderReverseApi(api_key="api_key")

# fetches the addresses information of a point
response = geocoder_reverse_api.retrieve_addresses(prox=[41.8842, -87.6388], limit=3)
print(response.as_dict())
