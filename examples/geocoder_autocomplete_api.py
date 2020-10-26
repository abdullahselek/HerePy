#!/usr/bin/env python

from herepy import GeocoderAutoCompleteApi

geocoder_autocomplete_api = GeocoderAutoCompleteApi(api_key="api_key")

# ask for a list of suggested addresses found within a specified area
response = geocoder_autocomplete_api.address_suggestion(
    query="High", prox=[51.5035, -0.1616], radius=100
)
print(response.as_dict())

# ask for a list of suggested addresses within a single country
response = geocoder_autocomplete_api.limit_results_byaddress(
    query="Nis", country_code="USA"
)
print(response.as_dict())
