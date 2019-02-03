#!/usr/bin/env python

"""A library that provides a Python interface to the HERE APIs"""

from __future__ import absolute_import

__author__       = 'Abdullah Selek'
__email__        = 'abdullahselek@gmail.com'
__copyright__    = 'Copyright (c) 2017 Abdullah Selek'
__license__      = 'MIT License'
__version__      = '0.5.0'
__url__          = 'https://github.com/abdullahselek/HerePy'
__download_url__ = 'https://pypi.org/pypi/herepy'
__description__  = 'A Python wrapper around the HERE APIs'


import json

from .error import HEREError

from .here_enum import (
    RouteMode,
    PlacesCategory,
    PublicTransitSearchMethod,
    PublicTransitRoutingType
)

from .models import (
    GeocoderResponse,
    RoutingResponse,
    GeocoderAutoCompleteResponse,
    PlacesResponse,
    PlacesSuggestionsResponse,
    PlaceCategoriesResponse,
    PublicTransitResponse,
    TrafficIncidentResponse,
    DestinationWeatherResponse
)

from .utils import Utils
from .geocoder_api import GeocoderApi
from .routing_api import RoutingApi
from .geocoder_autocomplete_api import GeocoderAutoCompleteApi
from .places_api import PlacesApi
from .public_transit_api import PublicTransitApi
from .destination_weather_api import DestinationWeatherApi
