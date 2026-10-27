#!/usr/bin/env python

"""A Python interface to HERE location APIs with sync and async HTTP calls."""

__author__ = "Abdullah Selek"
__email__ = "abdullahselek.os@gmail.com"
__copyright__ = "Copyright (c) 2017 Abdullah Selek"
__license__ = "MIT License"
__version__ = "3.6.5"
__url__ = "https://github.com/abdullahselek/HerePy"
__download_url__ = "https://pypi.org/pypi/herepy"
__description__ = "A Python interface to HERE location APIs with support for synchronous and asynchronous HTTP calls."

from .destination_weather_api import DestinationWeatherApi
from .error import AccessDeniedError, HEREError, InvalidRequestError, UnauthorizedError
from .ev_charging_stations_api import EVChargingStationsApi
from .fleet_telematics_api import FleetTelematicsApi
from .geocoder_api import GeocoderApi
from .geocoder_autocomplete_api import GeocoderAutoCompleteApi
from .geocoder_reverse_api import GeocoderReverseApi
from .here_enum import (
    AerialMapTileResourceType,
    AvoidFeature,
    BaseMapTileResourceType,
    EVStationConnectorTypes,
    FlowProximityAdditionalAttributes,
    IncidentsCriticalityInt,
    IncidentsCriticalityStr,
    IsolineRoutingMode,
    IsolineRoutingOptimizationMode,
    IsolineRoutingRangeType,
    IsolineRoutingTransportMode,
    MapImageFormatType,
    MapImageResourceType,
    MapTileApiType,
    MapTileResourceType,
    MatrixRoutingMode,
    MatrixRoutingProfile,
    MatrixRoutingTransportMode,
    MatrixRoutingType,
    MatrixSummaryAttribute,
    MultiplePickupOfferType,
    PlacesCategory,
    PublicTransitModeType,
    PublicTransitRoutingMode,
    PublicTransitSearchMethod,
    RouteMode,
    RoutingApiReturnField,
    RoutingApiSpanField,
    RoutingMetric,
    RoutingMode,
    RoutingTransportMode,
    ShippedHazardousGood,
    TrafficMapTileResourceType,
    TruckType,
    TunnelCategory,
    VectorMapTileLayer,
    WeatherProductType,
)
from .isoline_routing_api import IsolineRoutingApi
from .map_image_api import MapImageApi
from .map_tile_api import MapTileApi
from .mercator_projection import MercatorProjection
from .models import (
    DestinationWeatherResponse,
    EVChargingStationsResponse,
    GeocoderAutoCompleteResponse,
    GeocoderResponse,
    GeocoderReverseResponse,
    IsolineRoutingResponse,
    PlacesResponse,
    PublicTransitResponse,
    RmeResponse,
    RoutingMatrixResponse,
    RoutingResponse,
    RoutingResponseV8,
    TrafficFlowAvailabilityResponse,
    TrafficFlowResponse,
    TrafficIncidentResponse,
    WaypointSequenceResponse,
)
from .objects import Avoid, AvoidArea, Truck
from .places_api import PlacesApi
from .platform.tour_planning_api import TourPlanningApi
from .public_transit_api import PublicTransitApi
from .rme_api import RmeApi
from .routing_api import (
    InvalidCredentialsError,
    InvalidInputDataError,
    LinkIdNotFoundError,
    NoRouteFoundError,
    RouteNotReconstructedError,
    RoutingApi,
    WaypointNotFoundError,
)
from .traffic_api import TrafficApi
from .utils import Utils
from .vector_tile_api import VectorTileApi

__all__ = [
    "DestinationWeatherApi",
    "AccessDeniedError",
    "HEREError",
    "InvalidRequestError",
    "UnauthorizedError",
    "EVChargingStationsApi",
    "FleetTelematicsApi",
    "GeocoderApi",
    "GeocoderAutoCompleteApi",
    "GeocoderReverseApi",
    "AerialMapTileResourceType",
    "AvoidFeature",
    "BaseMapTileResourceType",
    "EVStationConnectorTypes",
    "FlowProximityAdditionalAttributes",
    "IncidentsCriticalityInt",
    "IncidentsCriticalityStr",
    "IsolineRoutingMode",
    "IsolineRoutingOptimizationMode",
    "IsolineRoutingRangeType",
    "IsolineRoutingTransportMode",
    "MapImageFormatType",
    "MapImageResourceType",
    "MapTileApiType",
    "MapTileResourceType",
    "MatrixRoutingMode",
    "MatrixRoutingProfile",
    "MatrixRoutingTransportMode",
    "MatrixRoutingType",
    "MatrixSummaryAttribute",
    "MultiplePickupOfferType",
    "PlacesCategory",
    "PublicTransitModeType",
    "PublicTransitRoutingMode",
    "PublicTransitSearchMethod",
    "RouteMode",
    "RoutingApiReturnField",
    "RoutingApiSpanField",
    "RoutingMetric",
    "RoutingMode",
    "RoutingTransportMode",
    "ShippedHazardousGood",
    "TrafficMapTileResourceType",
    "TruckType",
    "TunnelCategory",
    "VectorMapTileLayer",
    "WeatherProductType",
    "IsolineRoutingApi",
    "MapImageApi",
    "MapTileApi",
    "MercatorProjection",
    "DestinationWeatherResponse",
    "EVChargingStationsResponse",
    "GeocoderAutoCompleteResponse",
    "GeocoderResponse",
    "GeocoderReverseResponse",
    "IsolineRoutingResponse",
    "PlacesResponse",
    "PublicTransitResponse",
    "RmeResponse",
    "RoutingMatrixResponse",
    "RoutingResponse",
    "RoutingResponseV8",
    "TrafficFlowAvailabilityResponse",
    "TrafficFlowResponse",
    "TrafficIncidentResponse",
    "WaypointSequenceResponse",
    "Avoid",
    "AvoidArea",
    "Truck",
    "PlacesApi",
    "TourPlanningApi",
    "PublicTransitApi",
    "RmeApi",
    "InvalidCredentialsError",
    "InvalidInputDataError",
    "LinkIdNotFoundError",
    "NoRouteFoundError",
    "RouteNotReconstructedError",
    "RoutingApi",
    "WaypointNotFoundError",
    "TrafficApi",
    "Utils",
    "VectorTileApi",
]
