#!/usr/bin/env python

from herepy import (
    RoutingApi,
    RouteMode,
    MatrixRoutingType,
    MatrixSummaryAttribute,
    RoutingTransportMode,
    RoutingMode,
    RoutingApiReturnField,
    RoutingMetric,
    RoutingApiSpanField,
    AvoidArea,
    AvoidFeature,
    Avoid,
    Truck,
    ShippedHazardousGood,
    TunnelCategory,
    TruckType,
)

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
avoid = Avoid(
    features=[AvoidFeature.toll_road],
    areas=[AvoidArea(north=30, south=45, west=30, east=45)],
)
truck = Truck(
    shipped_hazardous_goods=[ShippedHazardousGood.gas],
    gross_weight=750,
    weight_per_axle=100,
    height=2000,
    width=350,
    length=10000,
    tunnel_category=TunnelCategory.c,
    axle_count=5,
    truck_type=TruckType.tractor,
    trailer_count=5,
)
response = routing_api.sync_matrix(
    origins=[[9.933231, -84.076831]],
    destinations=[[9.934574, -84.065544]],
    matrix_type=MatrixRoutingType.circle,
    center=[9.933300, -84.066891],
    radius=10000,
    avoid=avoid,
    truck=truck,
)
print(response.as_dict())

# async, fetches a matrix of route summaries between M starts and N destinations
# please check
# https://developer.here.com/documentation/identity-access-management/dev_guide/topics/sdk.html#step-1-register-your-application
# https://developer.here.com/documentation/identity-access-management/dev_guide/topics/postman.html
# to learn how to create bearer token
response = routing_api.async_matrix(
    token="TOKEN",
    origins=[[9.933231, -84.076831]],
    destinations=[[9.934574, -84.065544]],
    matrix_type=MatrixRoutingType.circle,
    center=[9.933300, -84.066891],
    radius=10000,
)
print(response.as_dict())

# async, fetches a matrix of route summaries between M starts and N destinations
avoid = Avoid(
    features=[AvoidFeature.toll_road],
    areas=[AvoidArea(north=30, south=45, west=30, east=45)],
)
truck = Truck(
    shipped_hazardous_goods=[ShippedHazardousGood.gas, ShippedHazardousGood.flammable],
    gross_weight=750,
    weight_per_axle=100,
    height=2000,
    width=350,
    length=10000,
    tunnel_category=TunnelCategory.c,
    axle_count=5,
    truck_type=TruckType.tractor,
    trailer_count=5,
)
response = routing_api.async_matrix(
    token="TOKEN",
    origins=[[9.933231, -84.076831]],
    destinations=[[9.934574, -84.065544]],
    matrix_type=MatrixRoutingType.circle,
    center=[9.933300, -84.066891],
    radius=10000,
    avoid=avoid,
    truck=truck,
    matrix_attributes=[
        MatrixSummaryAttribute.distances,
        MatrixSummaryAttribute.travel_times,
    ],
)
print(response.as_dict())

# fetch a aroute via v8
response = routing_api.route_v8(
    transport_mode=RoutingTransportMode.car,
    origin=[41.9798, -87.8801],
    destination=[41.9043, -87.9216],
    via=[[41.9339, -87.9021]],
    routing_mode=RoutingMode.fast,
    avoid={"features": ["controlledAccessHighway", "tunnel"]},
    exclude={"countries": ["TUR"]},
    units=RoutingMetric.metric,
    lang="tr-TR",
    return_fields=[RoutingApiReturnField.polyline],
    span_fields=[RoutingApiSpanField.walkAttributes],
    truck={"shippedHazardousGoods": ["explosive", "gas"]},
    scooter={"allowHighway": "true"},
)
print(response.as_dict())
