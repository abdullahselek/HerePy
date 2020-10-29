#!/usr/bin/env python

from herepy import (
    TrafficApi,
    IncidentsCriticalityStr,
    IncidentsCriticalityInt,
    FlowProximityAdditionalAttributes,
)

traffic_api = TrafficApi(api_key="api_key")

# fetches a traffic incident information within specified area
response = traffic_api.incidents_in_bounding_box(
    top_left=[52.5311, 13.3644],
    bottom_right=[52.5114, 13.4035],
    criticality=[
        IncidentsCriticalityStr.minor,
        IncidentsCriticalityStr.major,
        IncidentsCriticalityStr.critical,
    ],
)
print(response.as_dict())

# traffic incidents for a defined route
response = traffic_api.incidents_in_corridor(
    points=[[51.5072, -0.1275], [51.50781, -0.13112], [51.51006, -0.1346]],
    width=1000,
)
print(response.as_dict())

# traffic incident information within specified area
response = traffic_api.incidents_via_proximity(
    latitude=52.5311,
    longitude=13.3644,
    radius=15000,
    criticality=[
        IncidentsCriticalityInt.critical,
        IncidentsCriticalityInt.major,
    ],
)
print(response.as_dict())

# traffic flow information using a quadkey
response = traffic_api.flow_using_quadkey(quadkey="0313131311102300")
print(response.as_dict())

# traffic flow information within specified area
response = traffic_api.flow_within_boundingbox(
    top_left=[52.5311, 13.3644], bottom_right=[52.5114, 13.4035]
)
print(response.as_dict())

# traffic flow for a circle around a defined point
response = traffic_api.flow_using_proximity(
    latitude=51.5072, longitude=-0.1275, distance=100
)
print(response.as_dict())

# traffic flow information using proximity, returning shape and functional class
response = traffic_api.flow_using_proximity_returning_additional_attributes(
    latitude=51.5072,
    longitude=-0.1275,
    distance=100,
    attributes=[
        FlowProximityAdditionalAttributes.functional_class,
        FlowProximityAdditionalAttributes.shape,
    ],
)
print(response.as_dict())

# traffic flow information in specified area with a jam factor
response = traffic_api.flow_with_minimum_jam_factor(
    top_left=[52.5311, 13.3644],
    bottom_right=[52.5114, 13.4035],
    min_jam_factor=7,
)
print(response.as_dict())

# traffic flow for a defined route
response = traffic_api.flow_in_corridor(
    points=[[51.5072, -0.1275], [51.50781, -0.13112], [51.51006, -0.1346]],
    width=1000,
)
print(response.as_dict())

# flow availability requests allow you to see what traffic flow coverage exists in the current Traffic API
response = traffic_api.flow_availability_data()
print(response.as_dict())

# traffic flow including shape and functional class information
response = traffic_api.additional_attributes(
    quadkey="0313131311102312213",
    attributes=[FlowProximityAdditionalAttributes.functional_class],
)
print(response.as_dict())
