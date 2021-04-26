from typing import List
from herepy import AvoidFeature


class AvoidArea(object):
    """List of areas to avoid."""

    def __init__(self, avoid_type: str = "boundingBox", north: int, south: int, west: int, east: int):
        self.avoid_type = avoid_type
        self.north = north
        self.south = south
        self.west = west
        self.east = east


class Avoid(object):
    """Class that helps RoutingAPI to avoid routes that violate the properties it has."""

    def __init__(self, features: List[AvoidFeature], areas: List[AvoidArea]):
        self.features = features
        self.areas = areas
