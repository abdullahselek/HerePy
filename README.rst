======
HerePy
======

.. image:: https://img.shields.io/pypi/v/herepy.svg
    :target: https://pypi.python.org/pypi/herepy/
    :alt: Downloads

.. image:: https://travis-ci.org/abdullahselek/HerePy.svg?branch=master
    :target: https://travis-ci.org/abdullahselek/HerePy
    :alt: Travis-Ci

.. image:: https://codecov.io/gh/abdullahselek/HerePy/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/abdullahselek/HerePy
    :alt: Codecov

.. image:: https://requires.io/github/abdullahselek/HerePy/requirements.svg?branch=master
    :target: https://requires.io/github/abdullahselek/HerePy/requirements/?branch=master
    :alt: Requirements Status

.. image:: https://dependencyci.com/github/abdullahselek/HerePy/badge
    :target: https://dependencyci.com/github/abdullahselek/HerePy
    :alt: Dependency Status

============
Introduction
============

This library provides a pure Python interface for the `HERE API <https://developer.here.com/>`_. It works with Python versions from 2.7+ and Python 3.

`HERE <https://www.here.com/>`_ provides location based services. HERE exposes a `rest APIs <https://developer.here.com/documentation>`_ and this library is intended to make it even easier for Python programmers to use.

==========
Installing
==========

You can install herepy using:

.. code::

    $ pip install herepy

================
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

=============
Running Tests
=============

The test suite can be run against a single Python version which requires ```pip install pytest``` and optionally ```pip install pytest-cov``` (these are included if you have installed dependencies from ```requirements.testing.txt```)

To run the unit tests with a single Python version::

    $ pytest

to also run code coverage::

    $ py.test --cov=herepy

To run the unit tests against a set of Python versions::

    $ tox

------
Models
------

The library utilizes models to represent various data structures returned by HERE:
    * herepy.GeocoderResponse
    * herepy.RoutingResponse

-----------
GeocoderApi
-----------

Is the wrapper for HERE Geoder API, to use this wrapper and all other wrappers you need a AppId and AppCode which you
can get from `HERE Developer Portal <https://developer.here.com/>`_.

Initiation of GeocoderApi

.. code::

    import herepy

    geocoderApi = herepy.GeocoderApi('app_id', 'app_code')

Geocoding given search text

.. code::

    response = geocoderApi.FreeForm('200 S Mathilda Sunnyvale CA')

Geocoding given search text with in given boundingbox

.. code::

    response = geocoderApi.AddressWithBoundingBox('200 S Mathilda Sunnyvale CA',
                                                  [42.3952,-71.1056],
                                                  [42.3312,-71.0228])

Geocoding with given address details

.. code::

    response = geocoderApi.AddressWithDetails(34, 'Barbaros', 'Istanbul', 'Turkey')

Geocoding with given street and city

.. code::

    response = geocoderApi.StreetIntersection('Barbaros', 'Istanbul')

----------
RoutingApi
----------

Initiation of GeocoderApi

.. code::

    import herepy

    routingApi = herepy.RoutingApi('app_id', 'app_code')

Calculate route for car

.. code::

    response = routingApi.CarRoute([11.0, 12.0],
                                   [22.0, 23.0],
                                   [herepy.RouteMode.car, herepy.RouteMode.fastest])

Calculate route for pedestrians

.. code::

    response = routingApi.PedastrianRoute([11.0, 12.0],
                                          [22.0, 23.0],
                                          [herepy.RouteMode.pedestrian, herepy.RouteMode.fastest])

Calculate route between three points

.. code::

    response = routingApi.IntermediateRoute([11.0, 12.0],
                                            [15.0, 16.0],
                                            [22.0, 23.0],
                                            [herepy.RouteMode.car, herepy.RouteMode.fastest])
Route for public transport

.. code::

    response = routingApi.PublicTransport([11.0, 12.0],
                                          [15.0, 16.0],
                                          [herepy.RouteMode.publicTransport, herepy.RouteMode.fastest],
                                          True)

Calculates the fastest car route between two location

.. code::

    response = routingApi.LocationNearMotorway([11.0, 12.0],
                                               [22.0, 23.0],
                                               [herepy.RouteMode.car, herepy.RouteMode.fastest])
-------
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
