#!/usr/bin/env python

from herepy import (
    IsolineRoutingApi,
    IsolineRoutingTransportMode,
    IsolineRoutingMode,
)

isoline_routing_api = IsolineRoutingApi(api_key="api_key")

# Returns distance based isoline routing
response = isoline_routing_api.distance_based_isoline(
    transport_mode=IsolineRoutingTransportMode.car,
    origin=[52.51578, 13.37749],
    ranges=[3000, 4000],
    routing_mode=IsolineRoutingMode.short,
)
print(response.as_dict())

# Calculates time based isoline routing
response = isoline_routing_api.time_isoline(
    transport_mode=IsolineRoutingTransportMode.car,
    origin=[52.51578, 13.37749],
    ranges=[300, 400],
)
print(response.as_dict())

# Calcualtes consumption based isoline for electric vehicles
response = isoline_routing_api.isoline_based_on_consumption(
    origin=[52.532988, 13.352852],
    ranges=[20000, 30000],
    transport_mode=IsolineRoutingTransportMode.car,
    free_flow_speed_table=[
        0.239,
        27,
        0.239,
        45,
        0.259,
        60,
        0.196,
        75,
        0.207,
        90,
        0.238,
        100,
        0.26,
        110,
        0.296,
        120,
        0.337,
        130,
        0.351,
        250,
        0.351,
    ],
    traffic_speed_table=[
        0.349,
        27,
        0.319,
        45,
        0.329,
        60,
        0.266,
        75,
        0.287,
        90,
        0.318,
        100,
        0.33,
        110,
        0.335,
        120,
        0.35,
        130,
        0.36,
        250,
        0.36,
    ],
    ascent=9,
    descent=4.3,
    auxiliary_consumption=1.8,
)
print(response.as_dict())

# Calculates isoline routing at a specific time
response = isoline_routing_api.isoline_routing_at_specific_time(
    transport_mode=IsolineRoutingTransportMode.car,
    ranges=[300, 400],
    origin=[52.51578, 13.37749],
    departure_time="2020-05-10T09:30:00",
)
print(response.as_dict())

# Calculates isoline routing for multi ranges
response = isoline_routing_api.multi_range_routing(
    transport_mode=IsolineRoutingTransportMode.car,
    ranges=[1000, 2000, 3000],
    origin=[52.51578, 13.37749],
)
print(response.as_dict())

# Calculates an isoline in the reverse direction
response = isoline_routing_api.reverse_direction_isoline(
    transport_mode=IsolineRoutingTransportMode.car,
    ranges=[1000, 2000],
    origin=[52.51578, 13.37749],
)
print(response.as_dict())
