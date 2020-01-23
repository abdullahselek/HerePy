#!/usr/bin/env python

"""A library that provides a Python interface to the HERE APIs"""

__author__       = 'Abdullah Selek'
__email__        = 'abdullahselek@gmail.com'
__copyright__    = 'Copyright (c) 2017 Abdullah Selek'
__license__      = 'MIT License'
__version__      = '2.1.0'
__url__          = 'https://github.com/abdullahselek/HerePy'
__download_url__ = 'https://pypi.org/pypi/herepy'
__description__  = 'A Python wrapper around the HERE APIs'


import json

from .error import HEREError

from .here_enum import (
    RouteMode,
    MatrixSummaryAttribute,
    PlacesCategory,
    PublicTransitSearchMethod,
    PublicTransitRoutingMode,
    PublicTransitModeType,
    WeatherProductType
)

from .models import (
    GeocoderResponse,
    GeocoderReverseResponse,
    RoutingResponse,
    RoutingMatrixResponse,
    GeocoderAutoCompleteResponse,
    PlacesResponse,
    PlacesSuggestionsResponse,
    PlaceCategoriesResponse,
    PublicTransitResponse,
    RmeResponse,
    TrafficIncidentResponse,
    DestinationWeatherResponse
)

from .destination_weather_api import (
    DestinationWeatherApi,
    UnauthorizedError,
    InvalidRequestError
)

from .routing_api import (
    RoutingApi,
    InvalidCredentialsError,
    InvalidInputDataError,
    WaypointNotFoundError,
    NoRouteFoundError,
    LinkIdNotFoundError,
    RouteNotReconstructedError
)

from .utils import Utils
from .geocoder_api import GeocoderApi
from .geocoder_reverse_api import GeocoderReverseApi
from .geocoder_autocomplete_api import GeocoderAutoCompleteApi
from .places_api import PlacesApi
from .public_transit_api import PublicTransitApi
from .rme_api import RmeApi
