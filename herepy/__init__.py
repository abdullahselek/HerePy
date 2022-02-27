#!/usr/bin/env python

"""A library that provides a Python interface to the HERE APIs"""

__author__ = "Abdullah Selek"
__email__ = "abdullahselek.os@gmail.com"
__copyright__ = "Copyright (c) 2017 Abdullah Selek"
__license__ = "MIT License"
__version__ = "3.5.7"
__url__ = "https://github.com/abdullahselek/HerePy"
__download_url__ = "https://pypi.org/pypi/herepy"
__description__ = "A library that provides a Python interface to the HERE APIs"


import json

from .error import HEREError, UnauthorizedError, InvalidRequestError

from .here_enum import (
    RouteMode,
    MatrixSummaryAttribute,
    PlacesCategory,
    PublicTransitSearchMethod,
    PublicTransitRoutingMode,
    PublicTransitModeType,
    WeatherProductType,
    EVStationConnectorTypes,
    MultiplePickupOfferType,
    IncidentsCriticalityStr,
    IncidentsCriticalityInt,
    FlowProximityAdditionalAttributes,
    IsolineRoutingMode,
    IsolineRoutingTransportMode,
    IsolineRoutingOptimizationMode,
    IsolineRoutingRangeType,
    MapTileApiType,
    MapTileResourceType,
    BaseMapTileResourceType,
    AerialMapTileResourceType,
    TrafficMapTileResourceType,
    VectorMapTileLayer,
    MapImageResourceType,
    MapImageFormatType,
    MatrixRoutingType,
    MatrixRoutingProfile,
    MatrixRoutingMode,
    MatrixRoutingTransportMode,
    RoutingMode,
    RoutingTransportMode,
    RoutingMetric,
    RoutingApiReturnField,
    RoutingApiSpanField,
    AvoidFeature,
    ShippedHazardousGood,
    TunnelCategory,
    TruckType,
)

from .models import (
    GeocoderResponse,
    GeocoderReverseResponse,
    RoutingResponse,
    RoutingResponseV8,
    RoutingMatrixResponse,
    GeocoderAutoCompleteResponse,
    PlacesResponse,
    PublicTransitResponse,
    RmeResponse,
    TrafficIncidentResponse,
    DestinationWeatherResponse,
    EVChargingStationsResponse,
    WaypointSequenceResponse,
    TrafficFlowResponse,
    TrafficFlowAvailabilityResponse,
    IsolineRoutingResponse,
)

from .objects import AvoidArea, AvoidFeature, Avoid, Truck

from .destination_weather_api import DestinationWeatherApi

from .routing_api import (
    RoutingApi,
    InvalidCredentialsError,
    InvalidInputDataError,
    WaypointNotFoundError,
    NoRouteFoundError,
    LinkIdNotFoundError,
    RouteNotReconstructedError,
)

from .utils import Utils
from .mercator_projection import MercatorProjection
from .geocoder_api import GeocoderApi
from .geocoder_reverse_api import GeocoderReverseApi
from .geocoder_autocomplete_api import GeocoderAutoCompleteApi
from .places_api import PlacesApi
from .public_transit_api import PublicTransitApi
from .rme_api import RmeApi
from .ev_charging_stations_api import EVChargingStationsApi
from .fleet_telematics_api import FleetTelematicsApi
from .traffic_api import TrafficApi
from .isoline_routing_api import IsolineRoutingApi
from .map_tile_api import MapTileApi
from .vector_tile_api import VectorTileApi
from .map_image_api import MapImageApi
