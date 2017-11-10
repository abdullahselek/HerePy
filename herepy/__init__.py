#!/usr/bin/env python

"""A library that provides a Python interface to the HERE APIs"""

from __future__ import absolute_import

__author__       = 'Abdullah Selek'
__email__        = 'abdullahselek@gmail.com'
__copyright__    = 'Copyright (c) 2017 Abdullah Selek'
__license__      = 'MIT License'
__version__      = '0.3'
__url__          = 'https://github.com/abdullahselek/HerePy'
__download_url__ = 'https://pypi.python.org/pypi/herepy'
__description__  = 'A Python wrapper around the HERE APIs'


import json

from .error import HEREError

from .here_enum import (
    RouteMode,
    PlacesCategory
)

from .models import (
    GeocoderResponse,
    RoutingResponse,
    GeocoderAutoCompleteResponse,
    PlacesResponse,
    PlacesSuggestionsResponse,
    PlaceCategoriesResponse
)

from .utils import Utils
from .geocoder_api import GeocoderApi
from .routing_api import RoutingApi
from .geocoder_autocomplete_api import GeocoderAutoCompleteApi
from .places_api import PlacesApi
