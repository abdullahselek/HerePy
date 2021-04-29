from typing import List
from herepy import AvoidFeature, ShippedHazardousGood, TunnelCategory, TruckType


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
        """Returns a AvoidArea instance.
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
        """Returns a Avoid instance.
        Args:
          features (List[AvoidFeature]):
            List of routing features to avoid during route calculation.
          areas (List[AvoidArea]):
            List of areas to avoid.
        """

        self.features = [avoid_feature.__str__() for avoid_feature in features]
        self.areas = [
            {
                "type": avoid_area.avoid_type.__str__(),
                "north": avoid_area.north,
                "south": avoid_area.south,
                "west": avoid_area.west,
                "east": avoid_area.east,
            }
            for avoid_area in areas
        ]


class Truck(object):
    """Different truck options to use during route calculation when transportMode = truck"""

    def __init__(
        self,
        shipped_hazardous_goods: List[ShippedHazardousGood],
        gross_weight: int,
        weight_per_axle: int,
        height: int,
        width: int,
        length: int,
        tunnel_category: TunnelCategory,
        axle_count: int,
        truck_type: TruckType,
        trailer_count: int,
    ):
        """Returns a Truck instance.
        Args:
          shipped_hazardous_goods (List[ShippedHazardousGood]):
            List of hazardous materials in the vehicle.
          gross_weight (int):
            Total vehicle weight, including trailers and shipped goods, in kilograms.
          weight_per_axle (int):
            Vehicle weight per axle, in kilograms.
          height (int):
            Vehicle height, in centimeters.
          width (int):
            Vehicle width, in centimeters.
          length (int):
            Vehicle length, in centimeters.
          tunnel_category (TunnelCategory):
            Specifies the cargo tunnel restriction code. https://adrbook.com/en/2017/ADR/8.6.3
          axle_count (int):
            Total number of axles that the vehicle has.
          truck_type (TruckType):
            Specifies the type of truck.
          trailer_count (int):
            Number of trailers attached to the vehicle.
        """

        self.shipped_hazardous_goods = [
            hazardous_goods.__str__() for hazardous_goods in shipped_hazardous_goods
        ]
        self.gross_weight = gross_weight
        self.weight_per_axle = weight_per_axle
        self.height = height
        self.width = width
        self.length = length
        self.tunnel_category = tunnel_category.__str__()
        self.axle_count = axle_count
        self.truck_type = truck_type.__str__()
        self.trailer_count = trailer_count
