#!/usr/bin/env python

import sys

from enum import Enum

class RouteMode(Enum):
    fastest = 'fastest'
    car = 'car'
    traffic = 'traffic'
    enabled = 'enabled'

    def __str__(self):
        return '%s' % self._value_
