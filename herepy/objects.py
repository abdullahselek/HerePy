from typing import List
from herepy import AvoidFeature


class AvoidArea(object):
    """List of areas to avoid."""

    def __init__(
        self,
        north: int,
        south: int,
        west: int,
        east: int,
        avoid_type: str = "boundingBox",
    ):
        """Returns a RoutingApi instance.
        Args:
          north (int):
            Latitude in WGS-84 degrees of the northern boundary of the box.
          south (int):
            Latitude in WGS-84 degrees of the southern boundary of the box.
          west (int):
            Longitude in WGS-84 degrees of the western boundary of the box.
          east (int):
            Longitude in WGS-84 degrees of the eastern boundary of the box.
          avoid_type (str):
            Type of avoid, default `boundingBox`.
        """

        self.north = north
        self.south = south
        self.west = west
        self.east = east
        self.avoid_type = avoid_type


class Avoid(object):
    """Class that helps RoutingAPI to avoid routes that violate the properties it has."""

    def __init__(self, features: List[AvoidFeature], areas: List[AvoidArea]):
        """Returns a RoutingApi instance.
        Args:
          features (List[AvoidFeature]):
            List of routing features to avoid during route calculation.
          areas (List[AvoidArea]):
            List of areas to avoid.
        """

        self.features = features
        self.areas = areas
