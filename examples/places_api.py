#!/usr/bin/env python

from herepy import PlacesApi

places_api = PlacesApi(api_key="api_key")

# fetches a list of places based on a query string
response = places_api.onebox_search(
    coordinates=[37.7905, -122.4107], query="restaurant"
)
print(response.as_dict())

# fetches a list of places based on a query string and country code
response = places_api.search_in_country(
    coordinates=[37.7905, -122.4107], query="cafe", country_code="USA"
)
print(response.as_dict())

# a list of popular places around a location
response = places_api.places_in_circle(
    coordinates=[37.7905, -122.4107], radius=1000, query="cafe", limit=40
)
print(response.as_dict())
