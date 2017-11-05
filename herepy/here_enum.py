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

class PlacesCategory(Enum):
    """Categories which are used in places api functions."""

    accomodation = 'accomodation'
    administrative_areas_buildings = 'administrative-areas-buildings'
    airport = 'airport'
    atm_bank_exchange = 'atm-bank-exchange'
    coffee_tea = 'coffee-tea'
    eat_drink = 'eat-drink'
    going_out = 'going-out'
    hospital_health_care_facility = 'hospital-health-care-facility'
    leisure_outdoor = 'leisure-outdoor'
    natural_geographical = 'natural-geographical'
    petrol_station = 'petrol-station'
    restaurant = 'restaurant'
    snacks_fast_food = 'snacks-fast-food'
    sights_museums = 'sights-museums'
    shopping = 'shopping'
    toilet_rest_area = 'toilet-rest-area'
    transport = 'transport'

    def __str__(self):
        return '%s' % self._value_
