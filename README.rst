HerePy
======

.. image:: https://github.com/abdullahselek/HerePy/workflows/HerePy%20CI/badge.svg
    :target: https://github.com/abdullahselek/HerePy/actions

.. image:: https://img.shields.io/pypi/v/herepy.svg
    :target: https://pypi.python.org/pypi/herepy/

.. image:: https://img.shields.io/pypi/pyversions/herepy.svg
    :target: https://pypi.org/project/herepy

.. image:: https://codecov.io/gh/abdullahselek/HerePy/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/abdullahselek/HerePy

.. image:: https://pepy.tech/badge/herepy
    :target: https://pepy.tech/project/herepy

.. image:: https://img.shields.io/conda/vn/conda-forge/herepy?logo=conda-forge
    :target: https://anaconda.org/conda-forge/herepy

.. image:: https://anaconda.org/conda-forge/herepy/badges/latest_release_date.svg
    :target: https://anaconda.org/conda-forge/herepy

.. image:: https://anaconda.org/conda-forge/herepy/badges/license.svg
    :target: https://anaconda.org/conda-forge/herepy

Introduction
============

This library provides a pure Python interface for the `HERE API <https://developer.here.com/>`_. It works with Python versions 3.x.

`HERE <https://www.here.com/>`_ provides location based services. HERE exposes a `rest APIs <https://developer.here.com/documentation>`_ and this library is intended to make it even easier for Python programmers to use.

Installing
==========

You can install herepy using Python Package Index::

    $ pip install herepy

Install with conda from the Anaconda conda-forge channel::

    $ conda install -c conda-forge herepy

Install from its source repository on GitHub::

    $ pip install -e git+https://github.com/abdullahselek/HerePy#egg=herepy

Getting the code
================

The code is hosted at https://github.com/abdullahselek/HerePy

Check out the latest development version anonymously with::

    $ git clone git://github.com/abdullahselek/HerePy.git
    $ cd HerePy

To install dependencies, run either::

    $ pip install -r requirements.testing.txt
    $ pip install -r requirements.txt

To install the minimal dependencies for production use (i.e., what is installed
with ``pip install herepy``) run::

    $ pip install -r requirements.txt

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
======

The library utilizes models to represent various data structures returned by **herepy**::

    * herepy.GeocoderResponse
    * herepy.GeocoderReverseResponse
    * herepy.RoutingResponse
    * herepy.RoutingResponseV8
    * herepy.RoutingMatrixResponse
    * herepy.GeocoderAutoCompleteResponse
    * herepy.PlacesResponse
    * herepy.PublicTransitResponse
    * herepy.RmeResponse
    * herepy.TrafficIncidentResponse
    * herepy.DestinationWeatherResponse
    * herepy.EVChargingStationsResponse
    * herepy.WaypointSequenceResponse
    * herepy.TrafficFlowResponse
    * herepy.TrafficFlowAvailabilityResponse
    * herepy.IsolineRoutingResponse

API Clients
===========

Available API clients in **herepy**::

    * herepy.DestinationWeatherApi
    * herepy.EVChargingStationsApi
    * herepy.FleetTelematicsApi
    * herepy.GeocoderApi
    * herepy.GeocoderAutoCompleteApi
    * herepy.GeocoderReverseApi
    * herepy.PlacesApi
    * herepy.PublicTransitApi
    * herepy.RmeApi
    * herepy.RoutingApi
    * herepy.TrafficApi
    * herepy.IsolineRoutingApi
    * herepy.MapTileApi
    * herepy.VectorTileApi
    * herepy.MapImageApi

Documentation
=============

View the latest herepy documentation at `https://herepy.abdullahselek.com/ <https://herepy.abdullahselek.com/>`_. You can view HERE's API documentation at: `https://developer.here.com/documentation <https://developer.here.com/documentation>`_.

Using
=====

The library provides a Python wrapper around the HERE APIs with different data models. To get started, check out the examples in the ``examples/`` folder or
read the documentation at `https://herepy.abdullahselek.com/ <https://herepy.abdullahselek.com/>`_. All API clients need an API key which you can get from `HERE Developer Portal <https://developer.here.com/>`_.

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
