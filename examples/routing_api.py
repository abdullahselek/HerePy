#!/usr/bin/env python

from herepy import RoutingApi, RouteMode, MatrixRoutingType

routing_api = RoutingApi(api_key="api_key")

# fetches a bicycle route between two points
response = routing_api.bicycle_route(
    waypoint_a=[41.9798, -87.8801], waypoint_b=[41.9043, -87.9216]
)
print(response.as_dict())

# fetches a driving route between two points
response = routing_api.car_route(
    waypoint_a=[11.0, 12.0],
    waypoint_b=[22.0, 23.0],
    modes=[RouteMode.car, RouteMode.fastest],
)
print(response.as_dict())

# fetches a pedastrian route between two points
response = routing_api.pedastrian_route(
    waypoint_a=[11.0, 12.0],
    waypoint_b=[22.0, 23.0],
    modes=[RouteMode.pedestrian, RouteMode.fastest],
)
print(response.as_dict())

# fetches a intermediate route from three points
response = routing_api.intermediate_route(
    waypoint_a=[11.0, 12.0],
    waypoint_b=[15.0, 16.0],
    waypoint_c=[22.0, 23.0],
    modes=[RouteMode.car, RouteMode.fastest],
)
print(response.as_dict())

# fetches a public transport route between two points
response = routing_api.public_transport(
    waypoint_a=[11.0, 12.0],
    waypoint_b=[15.0, 16.0],
    combine_change=True,
    modes=[RouteMode.publicTransport, RouteMode.fastest],
)
print(response.as_dict())

# fetches a public transport route between two points based on timetables
response = routing_api.public_transport_timetable(
    waypoint_a=[11.0, 12.0],
    waypoint_b=[15.0, 16.0],
    combine_change=True,
    modes=[RouteMode.publicTransport, RouteMode.fastest],
    departure="yyyy-mm-ddThh:mm:ss",
)
print(response.as_dict())

# calculates the fastest car route between two location
response = routing_api.location_near_motorway(
    waypoint_a=[11.0, 12.0],
    waypoint_b=[22.0, 23.0],
    modes=[RouteMode.car, RouteMode.fastest],
)
print(response.as_dict())

# calculates the fastest truck route between two location
response = routing_api.truck_route(
    waypoint_a=[11.0, 12.0],
    waypoint_b=[22.0, 23.0],
    modes=[RouteMode.truck, RouteMode.fastest],
)
print(response.as_dict())

# sync, fetches a matrix of route summaries between M starts and N destinations
response = routing_api.sync_matrix(
    origins=[[9.933231, -84.076831]],
    destinations=[[9.934574, -84.065544]],
    matrix_type=MatrixRoutingType.circle,
    center=[9.933300, -84.066891],
    radius=10000,
)
print(response)

# async, fetches a matrix of route summaries between M starts and N destinations
response = routing_api.async_matrix(
    origins=[[9.933231, -84.076831]],
    destinations=[[9.934574, -84.065544]],
    matrix_type=MatrixRoutingType.circle,
    center=[9.933300, -84.066891],
    radius=10000,
)
print(response)
