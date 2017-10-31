#!/usr/bin/env python

import sys

from enum import Enum

class RouteMode(Enum):
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
