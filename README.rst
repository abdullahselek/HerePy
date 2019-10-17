HerePy
======

.. image:: https://img.shields.io/pypi/v/herepy.svg
    :target: https://pypi.python.org/pypi/herepy/

.. image:: https://img.shields.io/pypi/pyversions/herepy.svg
    :target: https://pypi.org/project/herepy

.. image:: https://readthedocs.org/projects/herepy/badge/?version=latest
    :target: http://herepy.readthedocs.org/en/latest/?badge=latest

.. image:: https://codecov.io/gh/abdullahselek/HerePy/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/abdullahselek/HerePy

.. image:: https://requires.io/github/abdullahselek/HerePy/requirements.svg?branch=master
    :target: https://requires.io/github/abdullahselek/HerePy/requirements/?branch=master

+-------------------------------------------------------------------------+----------------------------------------------------------------------------------+
|                                Linux                                    |                                       Windows                                    |
+=========================================================================+==================================================================================+
| .. image:: https://travis-ci.org/abdullahselek/HerePy.svg?branch=master | .. image:: https://ci.appveyor.com/api/projects/status/wlxrx5h8e8xyhvq2?svg=true |
|    :target: https://travis-ci.org/abdullahselek/HerePy                  |    :target: https://ci.appveyor.com/project/abdullahselek/herepy                 |
+-------------------------------------------------------------------------+----------------------------------------------------------------------------------+

Introduction
============

This library provides a pure Python interface for the `HERE API <https://developer.here.com/>`_. It works with Python versions from 2.7+ and Python 3.

`HERE <https://www.here.com/>`_ provides location based services. HERE exposes a `rest APIs <https://developer.here.com/documentation>`_ and this library is intended to make it even easier for Python programmers to use.

Installing
==========

You can install herepy using::

    $ pip install herepy

Getting the code
================

The code is hosted at https://github.com/abdullahselek/HerePy

Check out the latest development version anonymously with::

    $ git clone git://github.com/abdullahselek/HerePy.git
    $ cd HerePy

To install dependencies, run either::

    $ pip install -Ur requirements.testing.txt
    $ pip install -Ur requirements.txt

To install the minimal dependencies for production use (i.e., what is installed
with ``pip install herepy``) run::

    $ pip install -Ur requirements.txt

Running Tests
=============

The test suite can be run against a single Python version which requires ``pip install pytest`` and optionally ``pip install pytest-cov`` (these are included if you have installed dependencies from ``requirements.testing.txt``)

To run the unit tests with a single Python version::

    $ py.test -v

to also run code coverage::

    $ py.test --cov=herepy

To run the unit tests against a set of Python versions::

    $ tox

Models
------

The library utilizes models to represent various data structures returned by HERE::

    * herepy.GeocoderResponse
    * herepy.GeocoderReverseResponse
    * herepy.RoutingResponse
    * herepy.GeocoderAutoCompleteResponse
    * herepy.PlacesResponse
    * herepy.PlacesSuggestionsResponse
    * herepy.PlaceCategoriesResponse
    * herepy.PublicTransitResponse
    * herepy.RmeResponse

GeocoderApi
-----------

Is the wrapper for HERE Geocoder API, to use this wrapper and all other wrappers you need a AppId and AppCode which you
can get from `HERE Developer Portal <https://developer.here.com/>`_.

Initiation of GeocoderApi

.. code:: python

    import herepy

    geocoderApi = herepy.GeocoderApi('app_id', 'app_code')

Geocoding given search text

.. code:: python

    response = geocoderApi.free_form('200 S Mathilda Sunnyvale CA')

Geocoding given search text with in given boundingbox

.. code:: python

    response = geocoderApi.address_with_boundingbox('200 S Mathilda Sunnyvale CA',
                                                    [42.3952,-71.1056],
                                                    [42.3312,-71.0228])

Geocoding with given address details

.. code:: python

    response = geocoderApi.address_with_details(34, 'Barbaros', 'Istanbul', 'Turkey')

Geocoding with given street and city

.. code:: python

    response = geocoderApi.street_intersection('Barbaros', 'Istanbul')

GeocoderReverseApi
------------------

Is the wrapper for HERE Geocoder Reverse API, to use this wrapper and all other wrappers you need a AppId and AppCode
which you can get from `HERE Developer Portal <https://developer.here.com/>`_.

Initiation of GeocoderReverseApi

.. code:: python

    import herepy

    geocoderReverseApi = herepy.GeocoderReverseApi('app_id', 'app_code')


Retrieving address of a given point

.. code:: python

    response = geocoderReverseApi.retrieve_addresses([42.3952, -71.1056])

RoutingApi
----------

Initiation of RoutingApi

.. code:: python

    import herepy

    routingApi = herepy.RoutingApi('app_id', 'app_code')

Calculate route for car

.. code:: python

    response = routingApi.car_route([11.0, 12.0],
                                    [22.0, 23.0],
                                    [herepy.RouteMode.car, herepy.RouteMode.fastest])

Calculate route for pedestrians

.. code:: python

    response = routingApi.pedastrian_route([11.0, 12.0],
                                           [22.0, 23.0],
                                           [herepy.RouteMode.pedestrian, herepy.RouteMode.fastest])

Calculate route between three points

.. code:: python

    response = routingApi.intermediate_route([11.0, 12.0],
                                             [15.0, 16.0],
                                             [22.0, 23.0],
                                             [herepy.RouteMode.car, herepy.RouteMode.fastest])

Route for public transport

.. code:: python

    response = routingApi.public_transport([11.0, 12.0],
                                           [15.0, 16.0],
                                           True,
                                           [herepy.RouteMode.publicTransport, herepy.RouteMode.fastest])

Calculates the fastest car route between two location

.. code:: python

    response = routingApi.location_near_motorway([11.0, 12.0],
                                                 [22.0, 23.0],
                                                 [herepy.RouteMode.car, herepy.RouteMode.fastest])

Calculates the fastest truck route between two location

.. code:: python

    response = routingApi.truck_route([11.0, 12.0],
                                      [22.0, 23.0],
                                      [herepy.RouteMode.truck, herepy.RouteMode.fastest])

Calculate an MxN cost matrix for M start points and N destinations

.. code:: python

    response = routingApi.matrix(
        start_waypoints=[[11.0, 12.0], [13.0, 14.0]],
        destination_waypoints=[[21.0, 22.0], [23.0, 24.0]],
        departure='2013-07-04T17:00:00+02',
        modes=[herepy.RouteMode.fastest, herepy.RouteMode.car])


GeocoderAutoCompleteApi
-----------------------

Initiation of GeocoderAutoCompleteApi

.. code:: python

    import herepy

    geocoderAutoCompleteApi = herepy.GeocoderAutoCompleteApi('app_id', 'app_code')

Request a list of suggested addresses found within a specified area

.. code:: python

    response = geocoderAutoCompleteApi.address_suggestion('High', [51.5035,-0.1616], 100)

Request a list of suggested addresses within a single country

.. code:: python

    response = geocoderAutoCompleteApi.limit_results_byaddress('Nis', 'USA')

Request an annotated list of suggested addresses with matching tokens highlighted

.. code:: python

    response = geocoderAutoCompleteApi.highlighting_matches('Wacker Chic', '**', '**')

PlacesApi
---------

Initiation of PlacesApi

.. code:: python

    import herepy

    placesApi = herepy.PlacesApi('app_id', 'app_code')

Request a list of nearby places based on a query string

.. code:: python

    response = placesApi.onebox_search([37.7905, -122.4107], 'restaurant')

Request a list of popular places around a location

.. code:: python

    response = placesApi.places_at([37.7905, -122.4107])

Request a list of places within a category around a location

.. code:: python

    response = placesApi.category_places_at([37.7905, -122.4107], [herepy.PlacesCategory.eat_drink])

Request a list of places close to a location

.. code:: python

    response = placesApi.nearby_places([37.7905, -122.4107])

Request a list of suggestions based on a partial query string

.. code:: python

    response = placesApi.search_suggestions([52.5159, 13.3777], 'berlin')

Request a list of place categories available for a given location

.. code:: python

    response = placesApi.place_categories([52.5159, 13.3777])

Request a list of popular places within a specified area

.. code:: python

    response = placesApi.places_at_boundingbox([-122.408, 37.793], [-122.4070, 37.7942])

Request a list of popular places around a location using a foreign language

.. code:: python

    response = placesApi.places_with_language([48.8580, 2.2945], 'en-US')

PublicTransitApi
----------------

Initiation of PublicTransitApi

.. code:: python

    import herepy

    publicTransitApi = herepy.PublicTransitApi('app_id', 'app_code')

RmeApi
------

Initiation of RmeApi

.. code:: python

    import herepy

    rmeApi = herepy.RmeApi('app_id', 'app_code')

Get information about points of a gpx file

.. code:: python

    with open('my-gpx.file') as gpx_file:
        content = gpx_file.read()
        response = rmeApi.match_route(content, ['ROAD_GEOM_FCn(*)'])

License
-------

MIT License

Copyright (c) 2017 Abdullah Selek

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
