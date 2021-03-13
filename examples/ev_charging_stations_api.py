#!/usr/bin/env python

from herepy import EVChargingStationsApi, EVStationConnectorTypes

evcharging_stations_api = EVChargingStationsApi(api_key="api_key")
# search for ev charging stations in a circular area
response = evcharging_stations_api.get_stations_circular_search(
    latitude=52.516667,
    longitude=13.383333,
    radius=5000,
    connectortypes=[
        EVStationConnectorTypes.small_paddle_inductive,
        EVStationConnectorTypes.large_paddle_inductive,
    ],
)
print(response.as_dict())

# request for charging stations with in given bounding box
response = evcharging_stations_api.get_stations_bounding_box(
    top_left=[52.8, 11.37309],
    bottom_right=[52.31, 13.2],
    connectortypes=[
        EVStationConnectorTypes.small_paddle_inductive,
        EVStationConnectorTypes.large_paddle_inductive,
    ],
)
print(response.as_dict())

# request for charging stations with in given corridor
response = evcharging_stations_api.get_stations_corridor(
    points=[52.51666, 13.38333, 52.13333, 11.61666, 53.56527, 10.00138],
    connectortypes=[
        EVStationConnectorTypes.small_paddle_inductive,
        EVStationConnectorTypes.large_paddle_inductive,
    ],
)
print(response.as_dict())

# Based on the results of a search for charging stations, this method
# retrieves the full/updated information about a single charging station only.
response = evcharging_stations_api.get_station_details(
    station_id="276u33db-b2c840878cfc409fa5a0aef858419037"
)
print(response.as_dict())
