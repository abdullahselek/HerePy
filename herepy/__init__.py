#!/usr/bin/env python

"""A library that provides a Python interface to the HERE APIs"""

__author__ = "Abdullah Selek"
__email__ = "abdullahselek.os@gmail.com"
__copyright__ = "Copyright (c) 2017 Abdullah Selek"
__license__ = "MIT License"
__version__ = "3.6.1"
__url__ = "https://github.com/abdullahselek/HerePy"
__download_url__ = "https://pypi.org/pypi/herepy"
__description__ = "A library that provides a Python interface to the HERE APIs"


import json

from .destination_weather_api import DestinationWeatherApi
from .error import (AccessDeniedError, HEREError, InvalidRequestError,
                    UnauthorizedError)
from .ev_charging_stations_api import EVChargingStationsApi
from .fleet_telematics_api import FleetTelematicsApi
from .geocoder_api import GeocoderApi
from .geocoder_autocomplete_api import GeocoderAutoCompleteApi
from .geocoder_reverse_api import GeocoderReverseApi
from .here_enum import (AerialMapTileResourceType, AvoidFeature,
                        BaseMapTileResourceType, EVStationConnectorTypes,
                        FlowProximityAdditionalAttributes,
                        IncidentsCriticalityInt, IncidentsCriticalityStr,
                        IsolineRoutingMode, IsolineRoutingOptimizationMode,
                        IsolineRoutingRangeType, IsolineRoutingTransportMode,
                        MapImageFormatType, MapImageResourceType,
                        MapTileApiType, MapTileResourceType, MatrixRoutingMode,
                        MatrixRoutingProfile, MatrixRoutingTransportMode,
                        MatrixRoutingType, MatrixSummaryAttribute,
                        MultiplePickupOfferType, PlacesCategory,
                        PublicTransitModeType, PublicTransitRoutingMode,
                        PublicTransitSearchMethod, RouteMode,
                        RoutingApiReturnField, RoutingApiSpanField,
                        RoutingMetric, RoutingMode, RoutingTransportMode,
                        ShippedHazardousGood, TrafficMapTileResourceType,
                        TruckType, TunnelCategory, VectorMapTileLayer,
                        WeatherProductType)
from .isoline_routing_api import IsolineRoutingApi
from .map_image_api import MapImageApi
from .map_tile_api import MapTileApi
from .mercator_projection import MercatorProjection
from .models import (DestinationWeatherResponse, EVChargingStationsResponse,
                     GeocoderAutoCompleteResponse, GeocoderResponse,
                     GeocoderReverseResponse, IsolineRoutingResponse,
                     PlacesResponse, PublicTransitResponse, RmeResponse,
                     RoutingMatrixResponse, RoutingResponse, RoutingResponseV8,
                     TrafficFlowAvailabilityResponse, TrafficFlowResponse,
                     TrafficIncidentResponse, WaypointSequenceResponse)
from .objects import Avoid, AvoidArea, AvoidFeature, Truck
from .places_api import PlacesApi
from .platform.tour_planning_api import TourPlanningApi
from .public_transit_api import PublicTransitApi
from .rme_api import RmeApi
from .routing_api import (InvalidCredentialsError, InvalidInputDataError,
                          LinkIdNotFoundError, NoRouteFoundError,
                          RouteNotReconstructedError, RoutingApi,
                          WaypointNotFoundError)
from .traffic_api import TrafficApi
from .utils import Utils
from .vector_tile_api import VectorTileApi
