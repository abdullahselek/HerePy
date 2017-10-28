======
HerePy
======

.. image:: https://circleci.com/gh/abdullahselek/HerePy.svg?style=svg
    :target: https://circleci.com/gh/abdullahselek/HerePy
    :alt: Circle CI

.. image:: https://codecov.io/gh/abdullahselek/HerePy/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/abdullahselek/HerePy
    :alt: Codecov

============
Introduction
============

This library provides a pure Python interface for the `HERE API <https://developer.here.com/>`_. It works with Python versions from 2.7+ and Python 3.

`HERE <https://www.here.com/>`_ provides location based services. HERE exposes a `rest APIs <https://developer.here.com/documentation>`_ and this library is intended to make it even easier for Python programmers to use.

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
with ``pip install python-twitter``) run::

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

    $ make tox
