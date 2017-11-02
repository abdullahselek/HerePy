#!/usr/bin/env python

from enum import Enum

class RouteMode(Enum):
    """Modes which is used in routing api functions."""

    fastest = 'fastest'
    car = 'car'
    traffic_disabled = 'traffic:disabled'
    enabled = 'enabled'
    pedestrian = 'pedestrian'
    publicTransport = 'publicTransport'
    truck = 'truck'
    traffic_default = 'traffic:default'

    def __str__(self):
        return '%s' % self._value_
